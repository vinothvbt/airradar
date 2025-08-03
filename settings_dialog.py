#!/usr/bin/env python3
"""
Advanced Settings Dialog for WiFi Penetration Testing Radar
Provides configuration for monitoring, adapters, and scanning parameters
"""

import os
import subprocess
import json
from typing import List, Dict, Any
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QTabWidget,
    QGroupBox, QLabel, QComboBox, QSpinBox, QCheckBox, QPushButton,
    QSlider, QLineEdit, QTextEdit, QMessageBox, QProgressBar,
    QSplitter, QFrame, QScrollArea, QButtonGroup, QRadioButton
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QIcon

class WiFiAdapterDetector(QThread):
    """Thread to detect available WiFi adapters and their capabilities"""
    adapters_found = pyqtSignal(list)
    detection_progress = pyqtSignal(str)
    
    def run(self):
        """Detect WiFi adapters and their monitor mode capabilities"""
        adapters = []
        
        try:
            self.detection_progress.emit("Scanning for WiFi adapters...")
            
            # Get network interfaces
            result = subprocess.run(['iwconfig'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                current_adapter = None
                
                for line in lines:
                    if line and not line.startswith(' '):
                        # New adapter line
                        parts = line.split()
                        if len(parts) >= 2 and 'IEEE 802.11' in line:
                            adapter_name = parts[0]
                            self.detection_progress.emit(f"Found WiFi adapter: {adapter_name}")
                            
                            # Check monitor mode capability
                            monitor_capable = self._check_monitor_mode_support(adapter_name)
                            
                            # Get adapter info
                            adapter_info = self._get_adapter_info(adapter_name)
                            
                            adapters.append({
                                'name': adapter_name,
                                'monitor_capable': monitor_capable,
                                'driver': adapter_info.get('driver', 'Unknown'),
                                'chipset': adapter_info.get('chipset', 'Unknown'),
                                'status': adapter_info.get('status', 'Unknown')
                            })
            
            self.detection_progress.emit("Adapter detection complete")
            
        except Exception as e:
            self.detection_progress.emit(f"Error detecting adapters: {str(e)}")
            
        self.adapters_found.emit(adapters)
    
    def _check_monitor_mode_support(self, adapter: str) -> bool:
        """Check if adapter supports monitor mode"""
        try:
            # Check supported modes
            result = subprocess.run(['iw', adapter, 'info'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0 and 'monitor' in result.stdout.lower():
                return True
                
            # Alternative check with iwconfig
            result = subprocess.run(['iwconfig', adapter], capture_output=True, text=True, timeout=5)
            return result.returncode == 0
            
        except:
            return False
    
    def _get_adapter_info(self, adapter: str) -> Dict[str, str]:
        """Get detailed adapter information"""
        info = {}
        
        try:
            # Get driver info
            driver_path = f"/sys/class/net/{adapter}/device/driver"
            if os.path.exists(driver_path):
                driver_link = os.readlink(driver_path)
                info['driver'] = os.path.basename(driver_link)
            
            # Get interface status
            result = subprocess.run(['ip', 'link', 'show', adapter], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                if 'UP' in result.stdout:
                    info['status'] = 'UP'
                else:
                    info['status'] = 'DOWN'
            
            # Try to get chipset info
            result = subprocess.run(['lsusb'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                # This is a simplified approach - real chipset detection is more complex
                info['chipset'] = 'USB WiFi' if 'Wireless' in result.stdout else 'Unknown'
                
        except:
            pass
            
        return info

class MonitorModeManager(QThread):
    """Thread to manage monitor mode enabling/disabling"""
    mode_changed = pyqtSignal(str, bool, str)  # adapter, success, message
    
    def __init__(self, adapter: str, enable: bool):
        super().__init__()
        self.adapter = adapter
        self.enable = enable
    
    def run(self):
        """Enable or disable monitor mode"""
        try:
            if self.enable:
                self._enable_monitor_mode()
            else:
                self._disable_monitor_mode()
        except Exception as e:
            self.mode_changed.emit(self.adapter, False, f"Error: {str(e)}")
    
    def _enable_monitor_mode(self):
        """Enable monitor mode on adapter"""
        try:
            # Take interface down
            result = subprocess.run(['sudo', 'ip', 'link', 'set', self.adapter, 'down'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                raise Exception(f"Failed to bring down interface: {result.stderr}")
            
            # Set monitor mode
            result = subprocess.run(['sudo', 'iw', self.adapter, 'set', 'type', 'monitor'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                raise Exception(f"Failed to set monitor mode: {result.stderr}")
            
            # Bring interface up
            result = subprocess.run(['sudo', 'ip', 'link', 'set', self.adapter, 'up'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                raise Exception(f"Failed to bring up interface: {result.stderr}")
            
            self.mode_changed.emit(self.adapter, True, "Monitor mode enabled successfully")
            
        except Exception as e:
            self.mode_changed.emit(self.adapter, False, str(e))
    
    def _disable_monitor_mode(self):
        """Disable monitor mode and return to managed mode"""
        try:
            # Take interface down
            subprocess.run(['sudo', 'ip', 'link', 'set', self.adapter, 'down'], 
                          capture_output=True, text=True, timeout=10)
            
            # Set managed mode
            subprocess.run(['sudo', 'iw', self.adapter, 'set', 'type', 'managed'], 
                          capture_output=True, text=True, timeout=10)
            
            # Bring interface up
            subprocess.run(['sudo', 'ip', 'link', 'set', self.adapter, 'up'], 
                          capture_output=True, text=True, timeout=10)
            
            self.mode_changed.emit(self.adapter, True, "Monitor mode disabled, returned to managed mode")
            
        except Exception as e:
            self.mode_changed.emit(self.adapter, False, str(e))

class AdvancedSettingsDialog(QDialog):
    """Advanced settings dialog with comprehensive configuration options"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("WiFi Radar - Advanced Settings")
        self.setFixedSize(800, 600)
        self.adapters = []
        self.settings = self._load_settings()
        self._setup_ui()
        self._detect_adapters()
        
    def _setup_ui(self):
        """Setup the settings dialog UI"""
        layout = QVBoxLayout()
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Add tabs
        self.tab_widget.addTab(self._create_adapter_tab(), "WiFi Adapters")
        self.tab_widget.addTab(self._create_scanning_tab(), "Scanning Settings")
        self.tab_widget.addTab(self._create_advanced_tab(), "Advanced Options")
        self.tab_widget.addTab(self._create_monitoring_tab(), "Monitor Mode")
        
        layout.addWidget(self.tab_widget)
        
        # Button bar
        button_layout = QHBoxLayout()
        
        self.detect_btn = QPushButton("🔍 Detect Adapters")
        self.detect_btn.clicked.connect(self._detect_adapters)
        button_layout.addWidget(self.detect_btn)
        
        button_layout.addStretch()
        
        self.save_btn = QPushButton("💾 Save Settings")
        self.save_btn.clicked.connect(self._save_settings)
        button_layout.addWidget(self.save_btn)
        
        self.apply_btn = QPushButton("✅ Apply")
        self.apply_btn.clicked.connect(self._apply_settings)
        button_layout.addWidget(self.apply_btn)
        
        self.cancel_btn = QPushButton("❌ Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
        
        # Status bar
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("padding: 5px; background-color: #2b2b2b; color: #00d4aa;")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
        
        # Apply dark theme
        self._apply_dark_theme()
    
    def _create_adapter_tab(self) -> QFrame:
        """Create WiFi adapter configuration tab"""
        frame = QFrame()
        layout = QVBoxLayout()
        
        # Adapter selection group
        adapter_group = QGroupBox("WiFi Adapter Selection")
        adapter_layout = QGridLayout()
        
        adapter_layout.addWidget(QLabel("Primary Adapter:"), 0, 0)
        self.primary_adapter = QComboBox()
        self.primary_adapter.addItem("Auto-detect")
        adapter_layout.addWidget(self.primary_adapter, 0, 1)
        
        self.refresh_adapters_btn = QPushButton("🔄 Refresh")
        self.refresh_adapters_btn.clicked.connect(self._detect_adapters)
        adapter_layout.addWidget(self.refresh_adapters_btn, 0, 2)
        
        adapter_layout.addWidget(QLabel("Secondary Adapter:"), 1, 0)
        self.secondary_adapter = QComboBox()
        self.secondary_adapter.addItem("None")
        adapter_layout.addWidget(self.secondary_adapter, 1, 1)
        
        self.dual_adapter_mode = QCheckBox("Enable Dual Adapter Mode")
        adapter_layout.addWidget(self.dual_adapter_mode, 1, 2)
        
        adapter_group.setLayout(adapter_layout)
        layout.addWidget(adapter_group)
        
        # Adapter information display
        info_group = QGroupBox("Adapter Information")
        info_layout = QVBoxLayout()
        
        self.adapter_info = QTextEdit()
        self.adapter_info.setReadOnly(True)
        self.adapter_info.setMaximumHeight(200)
        self.adapter_info.setPlainText("No adapters detected. Click 'Detect Adapters' to scan.")
        info_layout.addWidget(self.adapter_info)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Detection progress
        self.detection_progress = QProgressBar()
        self.detection_progress.setVisible(False)
        layout.addWidget(self.detection_progress)
        
        layout.addStretch()
        frame.setLayout(layout)
        return frame
    
    def _create_scanning_tab(self) -> QFrame:
        """Create scanning configuration tab"""
        frame = QFrame()
        layout = QVBoxLayout()
        
        # Range settings
        range_group = QGroupBox("Range and Detection Settings")
        range_layout = QGridLayout()
        
        range_layout.addWidget(QLabel("Maximum Range (meters):"), 0, 0)
        self.max_range = QSpinBox()
        self.max_range.setRange(50, 2000)
        self.max_range.setValue(500)
        self.max_range.setSuffix(" m")
        range_layout.addWidget(self.max_range, 0, 1)
        
        range_layout.addWidget(QLabel("Scan Interval (seconds):"), 1, 0)
        self.scan_interval = QSpinBox()
        self.scan_interval.setRange(1, 60)
        self.scan_interval.setValue(3)
        self.scan_interval.setSuffix(" sec")
        range_layout.addWidget(self.scan_interval, 1, 1)
        
        range_layout.addWidget(QLabel("Channel Hopping Speed:"), 2, 0)
        self.channel_speed = QComboBox()
        self.channel_speed.addItems(["Fast", "Medium", "Slow", "Manual"])
        range_layout.addWidget(self.channel_speed, 2, 1)
        
        range_layout.addWidget(QLabel("Signal Threshold (dBm):"), 3, 0)
        self.signal_threshold = QSpinBox()
        self.signal_threshold.setRange(-100, -30)
        self.signal_threshold.setValue(-80)
        self.signal_threshold.setSuffix(" dBm")
        range_layout.addWidget(self.signal_threshold, 3, 1)
        
        range_group.setLayout(range_layout)
        layout.addWidget(range_group)
        
        # Channel selection
        channel_group = QGroupBox("Channel Configuration")
        channel_layout = QVBoxLayout()
        
        # 2.4GHz channels
        ghz24_layout = QHBoxLayout()
        ghz24_layout.addWidget(QLabel("2.4GHz Channels:"))
        self.channels_24ghz = QCheckBox("1-14 (Auto)")
        self.channels_24ghz.setChecked(True)
        ghz24_layout.addWidget(self.channels_24ghz)
        ghz24_layout.addStretch()
        channel_layout.addLayout(ghz24_layout)
        
        # 5GHz channels
        ghz5_layout = QHBoxLayout()
        ghz5_layout.addWidget(QLabel("5GHz Channels:"))
        self.channels_5ghz = QCheckBox("36-165 (Auto)")
        self.channels_5ghz.setChecked(True)
        ghz5_layout.addWidget(self.channels_5ghz)
        ghz5_layout.addStretch()
        channel_layout.addLayout(ghz5_layout)
        
        channel_group.setLayout(channel_layout)
        layout.addWidget(channel_group)
        
        layout.addStretch()
        frame.setLayout(layout)
        return frame
    
    def _create_advanced_tab(self) -> QFrame:
        """Create advanced options tab"""
        frame = QFrame()
        layout = QVBoxLayout()
        
        # Performance settings
        perf_group = QGroupBox("Performance Settings")
        perf_layout = QGridLayout()
        
        perf_layout.addWidget(QLabel("Thread Pool Size:"), 0, 0)
        self.thread_pool_size = QSpinBox()
        self.thread_pool_size.setRange(1, 16)
        self.thread_pool_size.setValue(4)
        perf_layout.addWidget(self.thread_pool_size, 0, 1)
        
        perf_layout.addWidget(QLabel("Buffer Size (packets):"), 1, 0)
        self.buffer_size = QSpinBox()
        self.buffer_size.setRange(100, 10000)
        self.buffer_size.setValue(1000)
        perf_layout.addWidget(self.buffer_size, 1, 1)
        
        self.gpu_acceleration = QCheckBox("Enable GPU Acceleration")
        perf_layout.addWidget(self.gpu_acceleration, 2, 0, 1, 2)
        
        perf_group.setLayout(perf_layout)
        layout.addWidget(perf_group)
        
        # Logging settings
        log_group = QGroupBox("Logging and Debug")
        log_layout = QGridLayout()
        
        log_layout.addWidget(QLabel("Log Level:"), 0, 0)
        self.log_level = QComboBox()
        self.log_level.addItems(["DEBUG", "INFO", "WARNING", "ERROR"])
        self.log_level.setCurrentText("INFO")
        log_layout.addWidget(self.log_level, 0, 1)
        
        self.enable_packet_logging = QCheckBox("Enable Packet Logging")
        log_layout.addWidget(self.enable_packet_logging, 1, 0, 1, 2)
        
        self.save_raw_data = QCheckBox("Save Raw Capture Data")
        log_layout.addWidget(self.save_raw_data, 2, 0, 1, 2)
        
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)
        
        # Security settings
        security_group = QGroupBox("Security Analysis")
        security_layout = QVBoxLayout()
        
        self.enable_deep_analysis = QCheckBox("Enable Deep Vulnerability Analysis")
        self.enable_deep_analysis.setChecked(True)
        security_layout.addWidget(self.enable_deep_analysis)
        
        self.auto_exploit_detection = QCheckBox("Automatic Exploit Detection")
        security_layout.addWidget(self.auto_exploit_detection)
        
        self.realtime_alerts = QCheckBox("Real-time Security Alerts")
        self.realtime_alerts.setChecked(True)
        security_layout.addWidget(self.realtime_alerts)
        
        security_group.setLayout(security_layout)
        layout.addWidget(security_group)
        
        layout.addStretch()
        frame.setLayout(layout)
        return frame
    
    def _create_monitoring_tab(self) -> QFrame:
        """Create monitor mode management tab"""
        frame = QFrame()
        layout = QVBoxLayout()
        
        # Monitor mode control
        monitor_group = QGroupBox("Monitor Mode Control")
        monitor_layout = QGridLayout()
        
        monitor_layout.addWidget(QLabel("Target Adapter:"), 0, 0)
        self.monitor_adapter = QComboBox()
        monitor_layout.addWidget(self.monitor_adapter, 0, 1)
        
        self.enable_monitor_btn = QPushButton("🔴 Enable Monitor Mode")
        self.enable_monitor_btn.clicked.connect(self._enable_monitor_mode)
        monitor_layout.addWidget(self.enable_monitor_btn, 0, 2)
        
        self.disable_monitor_btn = QPushButton("🟢 Disable Monitor Mode")
        self.disable_monitor_btn.clicked.connect(self._disable_monitor_mode)
        monitor_layout.addWidget(self.disable_monitor_btn, 1, 2)
        
        self.auto_monitor = QCheckBox("Auto-enable monitor mode on scan start")
        monitor_layout.addWidget(self.auto_monitor, 2, 0, 1, 3)
        
        monitor_group.setLayout(monitor_layout)
        layout.addWidget(monitor_group)
        
        # Monitor status
        status_group = QGroupBox("Monitor Status")
        status_layout = QVBoxLayout()
        
        self.monitor_status = QTextEdit()
        self.monitor_status.setReadOnly(True)
        self.monitor_status.setMaximumHeight(150)
        self.monitor_status.setPlainText("Monitor mode status will appear here...")
        status_layout.addWidget(self.monitor_status)
        
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)
        
        # Interface verification
        verify_group = QGroupBox("Interface Verification")
        verify_layout = QVBoxLayout()
        
        verify_btn = QPushButton("🔍 Verify All Interfaces")
        verify_btn.clicked.connect(self._verify_interfaces)
        verify_layout.addWidget(verify_btn)
        
        self.verification_results = QTextEdit()
        self.verification_results.setReadOnly(True)
        self.verification_results.setMaximumHeight(100)
        verify_layout.addWidget(self.verification_results)
        
        verify_group.setLayout(verify_layout)
        layout.addWidget(verify_group)
        
        layout.addStretch()
        frame.setLayout(layout)
        return frame
    
    def _detect_adapters(self):
        """Detect available WiFi adapters"""
        self.status_label.setText("Detecting WiFi adapters...")
        self.detection_progress.setVisible(True)
        self.detection_progress.setRange(0, 0)  # Indeterminate progress
        
        # Clear existing items (except first)
        self.primary_adapter.clear()
        self.secondary_adapter.clear()
        self.monitor_adapter.clear()
        
        self.primary_adapter.addItem("Auto-detect")
        self.secondary_adapter.addItem("None")
        self.monitor_adapter.addItem("Select adapter...")
        
        # Start adapter detection thread
        self.detector = WiFiAdapterDetector()
        self.detector.adapters_found.connect(self._on_adapters_found)
        self.detector.detection_progress.connect(self._on_detection_progress)
        self.detector.start()
    
    def _on_detection_progress(self, message: str):
        """Handle detection progress updates"""
        self.status_label.setText(message)
    
    def _on_adapters_found(self, adapters: List[Dict[str, Any]]):
        """Handle detected adapters"""
        self.adapters = adapters
        self.detection_progress.setVisible(False)
        
        if not adapters:
            self.status_label.setText("No WiFi adapters found")
            self.adapter_info.setPlainText("No WiFi adapters detected. Please ensure you have WiFi hardware installed.")
            return
        
        # Populate combo boxes
        for adapter in adapters:
            name = adapter['name']
            self.primary_adapter.addItem(name)
            self.secondary_adapter.addItem(name)
            self.monitor_adapter.addItem(name)
        
        # Update adapter info display
        info_text = f"Found {len(adapters)} WiFi adapter(s):\n\n"
        for adapter in adapters:
            monitor_support = "✅ Yes" if adapter['monitor_capable'] else "❌ No"
            info_text += f"🔹 {adapter['name']}\n"
            info_text += f"   Driver: {adapter['driver']}\n"
            info_text += f"   Chipset: {adapter['chipset']}\n"
            info_text += f"   Status: {adapter['status']}\n"
            info_text += f"   Monitor Mode: {monitor_support}\n\n"
        
        self.adapter_info.setPlainText(info_text)
        self.status_label.setText(f"Found {len(adapters)} WiFi adapter(s)")
    
    def _enable_monitor_mode(self):
        """Enable monitor mode on selected adapter"""
        adapter = self.monitor_adapter.currentText()
        if adapter == "Select adapter...":
            QMessageBox.warning(self, "Warning", "Please select an adapter first")
            return
        
        self.monitor_status.append(f"Enabling monitor mode on {adapter}...")
        self.enable_monitor_btn.setEnabled(False)
        
        self.monitor_manager = MonitorModeManager(adapter, True)
        self.monitor_manager.mode_changed.connect(self._on_monitor_mode_changed)
        self.monitor_manager.start()
    
    def _disable_monitor_mode(self):
        """Disable monitor mode on selected adapter"""
        adapter = self.monitor_adapter.currentText()
        if adapter == "Select adapter...":
            QMessageBox.warning(self, "Warning", "Please select an adapter first")
            return
        
        self.monitor_status.append(f"Disabling monitor mode on {adapter}...")
        self.disable_monitor_btn.setEnabled(False)
        
        self.monitor_manager = MonitorModeManager(adapter, False)
        self.monitor_manager.mode_changed.connect(self._on_monitor_mode_changed)
        self.monitor_manager.start()
    
    def _on_monitor_mode_changed(self, adapter: str, success: bool, message: str):
        """Handle monitor mode change result"""
        if success:
            self.monitor_status.append(f"✅ {message}")
        else:
            self.monitor_status.append(f"❌ {message}")
        
        self.enable_monitor_btn.setEnabled(True)
        self.disable_monitor_btn.setEnabled(True)
    
    def _verify_interfaces(self):
        """Verify all network interfaces"""
        self.verification_results.clear()
        self.verification_results.append("Verifying network interfaces...\n")
        
        try:
            # Run iwconfig to check wireless interfaces
            result = subprocess.run(['iwconfig'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.verification_results.append("✅ iwconfig command successful")
                self.verification_results.append(result.stdout)
            else:
                self.verification_results.append("❌ iwconfig command failed")
                
        except Exception as e:
            self.verification_results.append(f"❌ Error running verification: {str(e)}")
    
    def _load_settings(self) -> Dict[str, Any]:
        """Load settings from file"""
        try:
            with open('settings.json', 'r') as f:
                return json.load(f)
        except:
            return {
                'primary_adapter': 'Auto-detect',
                'secondary_adapter': 'None',
                'max_range': 500,
                'scan_interval': 3,
                'signal_threshold': -80,
                'dual_adapter_mode': False,
                'auto_monitor': False,
                'enable_deep_analysis': True,
                'realtime_alerts': True
            }
    
    def _save_settings(self):
        """Save current settings to file"""
        settings = {
            'primary_adapter': self.primary_adapter.currentText(),
            'secondary_adapter': self.secondary_adapter.currentText(),
            'max_range': self.max_range.value(),
            'scan_interval': self.scan_interval.value(),
            'signal_threshold': self.signal_threshold.value(),
            'dual_adapter_mode': self.dual_adapter_mode.isChecked(),
            'auto_monitor': self.auto_monitor.isChecked(),
            'enable_deep_analysis': self.enable_deep_analysis.isChecked(),
            'realtime_alerts': self.realtime_alerts.isChecked(),
            'thread_pool_size': self.thread_pool_size.value(),
            'buffer_size': self.buffer_size.value(),
            'log_level': self.log_level.currentText(),
            'channels_24ghz': self.channels_24ghz.isChecked(),
            'channels_5ghz': self.channels_5ghz.isChecked()
        }
        
        try:
            with open('settings.json', 'w') as f:
                json.dump(settings, indent=2, fp=f)
            self.status_label.setText("Settings saved successfully")
            QMessageBox.information(self, "Success", "Settings saved successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save settings: {str(e)}")
    
    def _apply_settings(self):
        """Apply current settings without saving"""
        self.settings = {
            'primary_adapter': self.primary_adapter.currentText(),
            'secondary_adapter': self.secondary_adapter.currentText(),
            'max_range': self.max_range.value(),
            'scan_interval': self.scan_interval.value(),
            'signal_threshold': self.signal_threshold.value(),
            'dual_adapter_mode': self.dual_adapter_mode.isChecked(),
            'auto_monitor': self.auto_monitor.isChecked(),
            'enable_deep_analysis': self.enable_deep_analysis.isChecked(),
            'realtime_alerts': self.realtime_alerts.isChecked()
        }
        self.status_label.setText("Settings applied")
        self.accept()
    
    def _apply_dark_theme(self):
        """Apply dark theme to dialog"""
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a1a;
                color: #ffffff;
            }
            QTabWidget::pane {
                border: 1px solid #404040;
                background-color: #2b2b2b;
            }
            QTabBar::tab {
                background-color: #404040;
                color: #ffffff;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #00d4aa;
                color: #000000;
            }
            QGroupBox {
                border: 2px solid #404040;
                border-radius: 8px;
                margin-top: 16px;
                padding-top: 8px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px;
                color: #00d4aa;
            }
            QPushButton {
                background-color: #00d4aa;
                color: #000000;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #00b894;
            }
            QPushButton:pressed {
                background-color: #008f75;
            }
            QComboBox, QSpinBox, QLineEdit {
                background-color: #404040;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 6px;
                border-radius: 4px;
            }
            QTextEdit {
                background-color: #2b2b2b;
                color: #ffffff;
                border: 1px solid #404040;
                border-radius: 4px;
            }
            QCheckBox {
                color: #ffffff;
            }
            QCheckBox::indicator:checked {
                background-color: #00d4aa;
                border: 1px solid #00d4aa;
            }
        """)

    def get_settings(self) -> Dict[str, Any]:
        """Get current settings"""
        return self.settings
