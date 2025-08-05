#!/usr/bin/env python3
"""
WiFi Security Radar Suite - Plugin-Based Main Launcher
Enhanced with modular plugin system for extensible WiFi monitoring tools
"""

import sys
import os
from pathlib import Path
from typing import Dict, Optional
from PyQt5.QtWidgets import (QApplication, QDialog, QVBoxLayout, QPushButton, 
                             QLabel, QHBoxLayout, QMessageBox, QListWidget, 
                             QListWidgetItem, QTextEdit, QSplitter, QGroupBox)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap

# Import plugin system
try:
    from core.plugin_manager import plugin_manager
    from core.plugin_base import PluginMetadata
    PLUGIN_SYSTEM_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Plugin system not available: {e}")
    PLUGIN_SYSTEM_AVAILABLE = False

# Import animation system if available
try:
    from ui_animations import animation_manager, EnhancedWidget, StatusIndicator
    ANIMATIONS_AVAILABLE = True
except ImportError:
    print("Warning: Animation framework not available, using basic UI")
    ANIMATIONS_AVAILABLE = False
    
    # Fallback classes
    class EnhancedWidget:
        pass
    class StatusIndicator:
        def __init__(self, parent=None):
            pass
        def set_status(self, status):
            pass
        def move(self, x, y):
            pass


class EnhancedButton(QPushButton):
    """Enhanced button with micro-interactions"""
    
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMouseTracking(True)
        if ANIMATIONS_AVAILABLE:
            self._setup_animations()
    
    def _setup_animations(self):
        """Setup button animations"""
        self.pulse_timer = QTimer()
        self.pulse_timer.timeout.connect(self._pulse_effect)
    
    def _pulse_effect(self):
        """Create subtle pulse effect"""
        if ANIMATIONS_AVAILABLE:
            animation = animation_manager.create_scale_animation(
                self, duration=300, start_scale=1.0, end_scale=1.02
            )
            
            def reverse_pulse():
                reverse_anim = animation_manager.create_scale_animation(
                    self, duration=300, start_scale=1.02, end_scale=1.0
                )
                reverse_anim.start()
            
            animation.finished.connect(reverse_pulse)
            animation.start()
    
    def enterEvent(self, event):
        """Enhanced hover enter with glow effect"""
        super().enterEvent(event)
        
        if ANIMATIONS_AVAILABLE:
            # Scale up slightly
            scale_anim = animation_manager.create_scale_animation(
                self, duration=200, end_scale=1.05
            )
            scale_anim.start()
    
    def leaveEvent(self, event):
        """Enhanced hover leave"""
        super().leaveEvent(event)
        
        if ANIMATIONS_AVAILABLE:
            # Scale back down
            scale_anim = animation_manager.create_scale_animation(
                self, duration=200, start_scale=1.05, end_scale=1.0
            )
            scale_anim.start()


class PluginListWidget(QListWidget):
    """Custom widget for displaying available plugins"""
    
    plugin_selected = pyqtSignal(str)  # Plugin name
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(200)
        self.itemClicked.connect(self._on_item_clicked)
        self._plugins_info: Dict[str, PluginMetadata] = {}
    
    def _on_item_clicked(self, item):
        """Handle plugin item clicked"""
        plugin_name = item.data(Qt.UserRole)
        if plugin_name:
            self.plugin_selected.emit(plugin_name)
    
    def populate_plugins(self, plugins_info: Dict[str, PluginMetadata]):
        """Populate the list with available plugins"""
        self.clear()
        self._plugins_info = plugins_info
        
        for name, metadata in plugins_info.items():
            item = QListWidgetItem()
            item.setText(f"{metadata.name} v{metadata.version}")
            item.setData(Qt.UserRole, name)
            item.setToolTip(metadata.description)
            self.addItem(item)
    
    def get_selected_plugin(self) -> Optional[str]:
        """Get the currently selected plugin name"""
        current_item = self.currentItem()
        if current_item:
            return current_item.data(Qt.UserRole)
        return None


class PluginDetailsWidget(QTextEdit):
    """Widget for displaying plugin details"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setMaximumHeight(150)
        self._current_plugin: Optional[PluginMetadata] = None
    
    def show_plugin_details(self, plugin_name: str, metadata: PluginMetadata):
        """Show details for a specific plugin"""
        self._current_plugin = metadata
        
        details = f"""<h3>{metadata.name} v{metadata.version}</h3>
<p><strong>Description:</strong> {metadata.description}</p>
<p><strong>Author:</strong> {metadata.author}</p>
<p><strong>Requires Root:</strong> {'Yes' if metadata.requires_root else 'No'}</p>
<p><strong>Capabilities:</strong> {', '.join(metadata.capabilities)}</p>
<p><strong>Dependencies:</strong> {', '.join(metadata.dependencies) if metadata.dependencies else 'None'}</p>"""
        
        self.setHtml(details)
    
    def clear_details(self):
        """Clear plugin details"""
        self._current_plugin = None
        self.clear()


class WiFiRadarPluginLauncher(QDialog):
    """Plugin-based launcher for WiFi Security Radar Suite"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WiFi Security Radar Suite - Plugin Launcher")
        self.setFixedSize(900, 650)
        self.selected_plugin = None
        self._plugins_info: Dict[str, PluginMetadata] = {}
        
        if ANIMATIONS_AVAILABLE:
            self.status_indicator = StatusIndicator(self)
        
        self._setup_ui()
        self._apply_theme()
        self._discover_plugins()
        
        if ANIMATIONS_AVAILABLE:
            self._setup_animations()
    
    def _setup_animations(self):
        """Setup entrance animations"""
        # Fade in animation
        fade_anim = animation_manager.create_fade_animation(self, duration=500)
        fade_anim.start()
        
        # Update status indicator
        self.status_indicator.set_status("connected")
        self.status_indicator.move(10, 10)
    
    def _setup_ui(self):
        """Setup the launcher UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title section
        title_layout = QVBoxLayout()
        
        title = QLabel("WiFi Security Radar Suite v5.0")
        title.setFont(QFont("JetBrains Mono", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title)
        
        subtitle = QLabel("Plugin-Based WiFi Security Analysis Tools")
        subtitle.setFont(QFont("JetBrains Mono", 12))
        subtitle.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(subtitle)
        
        layout.addLayout(title_layout)
        
        # Main content area
        content_splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Plugin list
        left_panel = QGroupBox("Available Plugins")
        left_layout = QVBoxLayout(left_panel)
        
        self.plugin_list = PluginListWidget()
        self.plugin_list.plugin_selected.connect(self._on_plugin_selected)
        left_layout.addWidget(self.plugin_list)
        
        # Plugin action buttons
        button_layout = QHBoxLayout()
        
        self.launch_btn = EnhancedButton("Launch Plugin")
        self.launch_btn.setFont(QFont("JetBrains Mono", 10, QFont.Bold))
        self.launch_btn.clicked.connect(self._launch_selected_plugin)
        self.launch_btn.setEnabled(False)
        button_layout.addWidget(self.launch_btn)
        
        self.refresh_btn = EnhancedButton("Refresh")
        self.refresh_btn.setFont(QFont("JetBrains Mono", 10))
        self.refresh_btn.clicked.connect(self._discover_plugins)
        button_layout.addWidget(self.refresh_btn)
        
        left_layout.addLayout(button_layout)
        content_splitter.addWidget(left_panel)
        
        # Right panel - Plugin details
        right_panel = QGroupBox("Plugin Details")
        right_layout = QVBoxLayout(right_panel)
        
        self.plugin_details = PluginDetailsWidget()
        right_layout.addWidget(self.plugin_details)
        
        # Plugin status
        self.status_label = QLabel("No plugin selected")
        self.status_label.setFont(QFont("JetBrains Mono", 9))
        right_layout.addWidget(self.status_label)
        
        content_splitter.addWidget(right_panel)
        content_splitter.setSizes([400, 500])
        
        layout.addWidget(content_splitter)
        
        # Bottom buttons
        bottom_layout = QHBoxLayout()
        
        self.exit_btn = EnhancedButton("Exit")
        self.exit_btn.setFont(QFont("JetBrains Mono", 11, QFont.Bold))
        self.exit_btn.clicked.connect(self._exit_with_animation)
        bottom_layout.addWidget(self.exit_btn)
        
        layout.addLayout(bottom_layout)
        
        # Info
        info = QLabel("Note: Most tools require root privileges for WiFi scanning")
        info.setFont(QFont("JetBrains Mono", 9))
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)
    
    def _apply_theme(self):
        """Apply consistent hacker theme with enhanced styling"""
        self.setStyleSheet("""
            QDialog {
                background-color: #0A0A0A;
                color: #00FF00;
                font-family: 'JetBrains Mono', monospace;
                border: 2px solid #333;
                border-radius: 12px;
            }
            QLabel {
                color: #00FF00;
                font-family: 'JetBrains Mono', monospace;
            }
            QPushButton {
                background-color: #1E1E1E;
                color: #00FF00;
                border: 2px solid #333;
                padding: 12px 20px;
                border-radius: 8px;
                font-family: 'JetBrains Mono', monospace;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #00FF00;
                color: #000000;
                border: 2px solid #00AA00;
                box-shadow: 0 0 15px rgba(0, 255, 0, 0.5);
            }
            QPushButton:pressed {
                background-color: #00AA00;
                color: #000000;
            }
            QPushButton:disabled {
                background-color: #333;
                color: #666;
                border: 2px solid #555;
            }
            QGroupBox {
                border: 2px solid #333;
                border-radius: 8px;
                margin-top: 10px;
                color: #00FF00;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QListWidget {
                background-color: #1E1E1E;
                color: #00FF00;
                border: 2px solid #333;
                border-radius: 6px;
                font-family: 'JetBrains Mono', monospace;
                selection-background-color: #00FF00;
                selection-color: #000000;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #333;
            }
            QListWidget::item:hover {
                background-color: #333;
            }
            QTextEdit {
                background-color: #1E1E1E;
                color: #00FF00;
                border: 2px solid #333;
                border-radius: 6px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 10px;
            }
        """)
    
    def _discover_plugins(self):
        """Discover and load available plugins"""
        if not PLUGIN_SYSTEM_AVAILABLE:
            self._show_fallback_options()
            return
        
        self.status_label.setText("Discovering plugins...")
        QApplication.processEvents()
        
        try:
            # Discover plugins
            plugin_count = plugin_manager.discover_plugins()
            
            # Get plugin information
            self._plugins_info = plugin_manager.get_available_plugins()
            
            # Populate the plugin list
            self.plugin_list.populate_plugins(self._plugins_info)
            
            if plugin_count > 0:
                self.status_label.setText(f"Found {plugin_count} plugins")
            else:
                self.status_label.setText("No plugins found")
                self._show_fallback_options()
                
        except Exception as e:
            self.status_label.setText(f"Error discovering plugins: {e}")
            self._show_fallback_options()
    
    def _show_fallback_options(self):
        """Show fallback options when plugin system is not available"""
        # Add fallback options to the list
        fallback_plugins = {
            "navigation_enhanced": PluginMetadata(
                name="Navigation Enhanced Radar (Direct)",
                version="4.0.0",
                description="Direct launch of navigation enhanced interface",
                author="WiFi Security Tools",
                requires_root=True,
                capabilities=["wifi_scanning", "navigation", "theming"],
                dependencies=["PyQt5"]
            ),
            "penetration_testing": PluginMetadata(
                name="Penetration Testing Radar (Direct)",
                version="4.0.0", 
                description="Direct launch of penetration testing radar",
                author="WiFi Security Tools",
                requires_root=True,
                capabilities=["wifi_scanning", "vulnerability_assessment"],
                dependencies=["PyQt5"]
            )
        }
        
        self.plugin_list.populate_plugins(fallback_plugins)
        self._plugins_info = fallback_plugins
        self.status_label.setText("Using fallback mode (plugin system unavailable)")
    
    def _on_plugin_selected(self, plugin_name: str):
        """Handle plugin selection"""
        if plugin_name in self._plugins_info:
            metadata = self._plugins_info[plugin_name]
            self.plugin_details.show_plugin_details(plugin_name, metadata)
            self.selected_plugin = plugin_name
            self.launch_btn.setEnabled(True)
            self.status_label.setText(f"Selected: {metadata.name}")
        else:
            self.plugin_details.clear_details()
            self.selected_plugin = None
            self.launch_btn.setEnabled(False)
            self.status_label.setText("Invalid plugin selection")
    
    def _launch_selected_plugin(self):
        """Launch the selected plugin"""
        if not self.selected_plugin:
            return
        
        self.status_label.setText("Launching plugin...")
        QApplication.processEvents()
        
        try:
            if PLUGIN_SYSTEM_AVAILABLE and self.selected_plugin in plugin_manager.get_available_plugins():
                # Use plugin system
                plugin_instance = plugin_manager.load_plugin(self.selected_plugin)
                if plugin_instance:
                    window = plugin_instance.create_main_window()
                    window.show()
                    self.accept()
                else:
                    self.status_label.setText("Failed to load plugin")
            else:
                # Use fallback direct launch
                self._launch_fallback_tool()
                
        except Exception as e:
            QMessageBox.critical(self, "Launch Error", 
                               f"Failed to launch plugin:\n\n{str(e)}")
            self.status_label.setText("Launch failed")
    
    def _launch_fallback_tool(self):
        """Launch tool using fallback method"""
        try:
            if self.selected_plugin == "navigation_enhanced":
                from wifi_radar_nav_enhanced import NavigationRadarWindow
                window = NavigationRadarWindow()
                window.show()
                self.accept()
                
            elif self.selected_plugin == "penetration_testing":
                from wifi_pentest_radar_modern import WiFiPentestRadarModern
                window = WiFiPentestRadarModern()
                window.show()
                self.accept()
            else:
                raise ValueError(f"Unknown plugin: {self.selected_plugin}")
                
        except ImportError as e:
            QMessageBox.critical(self, "Import Error",
                               f"Failed to import required module:\n\n{str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Launch Error",
                               f"Failed to launch tool:\n\n{str(e)}")
    
    def _exit_with_animation(self):
        """Exit with smooth animation"""
        if ANIMATIONS_AVAILABLE:
            fade_anim = animation_manager.create_fade_animation(
                self, duration=300, start_opacity=1.0, end_opacity=0.0
            )
            fade_anim.finished.connect(self.reject)
            fade_anim.start()
        else:
            self.reject()


def main():
    """Main launcher function"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("WiFi Security Radar Suite")
    app.setApplicationVersion("5.0.0")
    
    # Check root privileges
    if os.geteuid() != 0:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Root Privileges Required")
        msg.setText("This application requires root privileges for WiFi scanning.\n\nPlease run with sudo:\nsudo python3 main_launcher_plugin.py")
        msg.exec_()
        return 1
    
    # Show launcher dialog
    launcher = WiFiRadarPluginLauncher()
    if launcher.exec_() == QDialog.Accepted:
        return app.exec_()
    
    return 0


if __name__ == '__main__':
    sys.exit(main())