#!/usr/bin/env python3
"""
Export Module for WiFi Security Radar Suite
Provides data export functionality in multiple formats (CSV, JSON, HTML reports)
"""

import json
import csv
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
import html

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
    QPushButton, QFileDialog, QTextEdit, QGroupBox, QCheckBox,
    QProgressBar, QMessageBox, QLineEdit
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont


@dataclass
class ExportData:
    """Data structure for export operations"""
    networks: List[Dict[str, Any]]
    scan_metadata: Dict[str, Any]
    timestamp: str
    format_version: str = "1.0"


class DataExporter:
    """Core data export functionality"""
    
    @staticmethod
    def export_to_csv(data: ExportData, filepath: str) -> bool:
        """Export data to CSV format"""
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                if not data.networks:
                    return False
                    
                # Get all possible fieldnames from all networks
                fieldnames = set()
                for network in data.networks:
                    fieldnames.update(network.keys())
                fieldnames = sorted(list(fieldnames))
                
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                # Write header
                writer.writeheader()
                
                # Write network data
                for network in data.networks:
                    # Clean data for CSV
                    clean_network = {}
                    for key, value in network.items():
                        if isinstance(value, (list, dict)):
                            clean_network[key] = json.dumps(value)
                        else:
                            clean_network[key] = str(value) if value is not None else ""
                    writer.writerow(clean_network)
                    
                return True
                
        except Exception as e:
            print(f"CSV export error: {e}")
            return False
    
    @staticmethod
    def export_to_json(data: ExportData, filepath: str, pretty: bool = True) -> bool:
        """Export data to JSON format"""
        try:
            export_dict = asdict(data)
            
            with open(filepath, 'w', encoding='utf-8') as jsonfile:
                if pretty:
                    json.dump(export_dict, jsonfile, indent=2, ensure_ascii=False, default=str)
                else:
                    json.dump(export_dict, jsonfile, ensure_ascii=False, default=str)
                    
            return True
            
        except Exception as e:
            print(f"JSON export error: {e}")
            return False
    
    @staticmethod
    def export_to_html(data: ExportData, filepath: str) -> bool:
        """Export data to HTML report format"""
        try:
            html_content = DataExporter._generate_html_report(data)
            
            with open(filepath, 'w', encoding='utf-8') as htmlfile:
                htmlfile.write(html_content)
                
            return True
            
        except Exception as e:
            print(f"HTML export error: {e}")
            return False
    
    @staticmethod
    def _generate_html_report(data: ExportData) -> str:
        """Generate comprehensive HTML report"""
        
        # Calculate statistics
        total_networks = len(data.networks)
        security_stats = {}
        signal_stats = []
        
        for network in data.networks:
            # Security statistics
            security = network.get('security', 'Unknown')
            security_stats[security] = security_stats.get(security, 0) + 1
            
            # Signal statistics
            signal = network.get('signal', 0)
            if isinstance(signal, (int, float)):
                signal_stats.append(signal)
        
        avg_signal = sum(signal_stats) / len(signal_stats) if signal_stats else 0
        strongest_signal = max(signal_stats) if signal_stats else 0
        weakest_signal = min(signal_stats) if signal_stats else 0
        
        # Generate HTML
        html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WiFi Security Radar Report</title>
    <style>
        body {{
            font-family: 'Courier New', monospace;
            background-color: #0a0a0a;
            color: #00ff00;
            margin: 0;
            padding: 20px;
            line-height: 1.6;
        }}
        .header {{
            text-align: center;
            border-bottom: 2px solid #00ff00;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            color: #00ff00;
            font-size: 2.5em;
            margin: 0;
            text-shadow: 0 0 10px #00ff00;
        }}
        .header p {{
            font-size: 1.2em;
            margin: 10px 0;
            opacity: 0.8;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .summary-box {{
            background-color: #1a1a1a;
            border: 2px solid #333;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
        }}
        .summary-box h3 {{
            color: #00ff00;
            margin-top: 0;
            font-size: 1.3em;
        }}
        .summary-box .value {{
            font-size: 2em;
            font-weight: bold;
            color: #00ff00;
            text-shadow: 0 0 5px #00ff00;
        }}
        .networks-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background-color: #1a1a1a;
        }}
        .networks-table th, .networks-table td {{
            border: 1px solid #333;
            padding: 12px;
            text-align: left;
        }}
        .networks-table th {{
            background-color: #2a2a2a;
            color: #00ff00;
            font-weight: bold;
            position: sticky;
            top: 0;
        }}
        .networks-table tr:nth-child(even) {{
            background-color: #151515;
        }}
        .networks-table tr:hover {{
            background-color: #2a2a2a;
        }}
        .security-critical {{ color: #ff1744; font-weight: bold; }}
        .security-high {{ color: #ff6d00; font-weight: bold; }}
        .security-medium {{ color: #ff9800; font-weight: bold; }}
        .security-low {{ color: #ffeb3b; font-weight: bold; }}
        .security-minimal {{ color: #4caf50; font-weight: bold; }}
        .signal-excellent {{ color: #4caf50; }}
        .signal-good {{ color: #8bc34a; }}
        .signal-fair {{ color: #ffeb3b; }}
        .signal-poor {{ color: #ff9800; }}
        .signal-very-poor {{ color: #f44336; }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #333;
            opacity: 0.7;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📡 WiFi Security Radar Report</h1>
        <p>Generated on {data.timestamp}</p>
        <p>Scan Results: {total_networks} networks detected</p>
    </div>

    <div class="summary">
        <div class="summary-box">
            <h3>Total Networks</h3>
            <div class="value">{total_networks}</div>
        </div>
        <div class="summary-box">
            <h3>Average Signal</h3>
            <div class="value">{avg_signal:.1f} dBm</div>
        </div>
        <div class="summary-box">
            <h3>Strongest Signal</h3>
            <div class="value">{strongest_signal:.1f} dBm</div>
        </div>
        <div class="summary-box">
            <h3>Weakest Signal</h3>
            <div class="value">{weakest_signal:.1f} dBm</div>
        </div>
    </div>

    <div class="summary">
        <div class="summary-box">
            <h3>Security Distribution</h3>
            <div style="text-align: left; font-size: 0.9em;">
"""
        
        # Add security statistics
        for security, count in security_stats.items():
            percentage = (count / total_networks * 100) if total_networks > 0 else 0
            html_template += f"                {html.escape(security)}: {count} ({percentage:.1f}%)<br>\n"
        
        html_template += """            </div>
        </div>
    </div>

    <h2>📋 Detailed Network Information</h2>
    <table class="networks-table">
        <thead>
            <tr>
                <th>SSID</th>
                <th>BSSID</th>
                <th>Security</th>
                <th>Signal (dBm)</th>
                <th>Channel</th>
                <th>Frequency</th>
                <th>Vendor</th>
                <th>Last Seen</th>
            </tr>
        </thead>
        <tbody>
"""
        
        # Add network rows
        for network in data.networks:
            ssid = html.escape(str(network.get('ssid', 'Hidden')))
            bssid = html.escape(str(network.get('bssid', 'Unknown')))
            security = html.escape(str(network.get('security', 'Unknown')))
            signal = network.get('signal', 0)
            channel = network.get('channel', 'Unknown')
            frequency = network.get('frequency', 'Unknown')
            vendor = html.escape(str(network.get('vendor', 'Unknown')))
            last_seen = network.get('last_seen', 'Unknown')
            
            # Security class
            security_class = ""
            if 'OPEN' in security.upper():
                security_class = "security-critical"
            elif 'WEP' in security.upper():
                security_class = "security-critical"
            elif 'WPA3' in security.upper():
                security_class = "security-minimal"
            elif 'WPA2' in security.upper():
                security_class = "security-low"
            elif 'WPA' in security.upper():
                security_class = "security-medium"
            
            # Signal class
            signal_class = ""
            if isinstance(signal, (int, float)):
                if signal >= -50:
                    signal_class = "signal-excellent"
                elif signal >= -60:
                    signal_class = "signal-good"
                elif signal >= -70:
                    signal_class = "signal-fair"
                elif signal >= -80:
                    signal_class = "signal-poor"
                else:
                    signal_class = "signal-very-poor"
            
            html_template += f"""            <tr>
                <td>{ssid}</td>
                <td style="font-family: monospace;">{bssid}</td>
                <td class="{security_class}">{security}</td>
                <td class="{signal_class}">{signal}</td>
                <td>{channel}</td>
                <td>{frequency}</td>
                <td>{vendor}</td>
                <td>{last_seen}</td>
            </tr>
"""
        
        html_template += """        </tbody>
    </table>

    <div class="footer">
        <p>Generated by WiFi Security Radar Suite v5.0</p>
        <p>🔒 For authorized security testing purposes only</p>
    </div>
</body>
</html>"""
        
        return html_template


class ExportDialog(QDialog):
    """Dialog for configuring and performing data export"""
    
    export_completed = pyqtSignal(bool, str)  # success, message
    
    def __init__(self, networks_data, parent=None):
        super().__init__(parent)
        self.networks_data = networks_data
        self.setWindowTitle("Export WiFi Data")
        self.setFixedSize(500, 400)
        self._setup_ui()
        self._apply_theme()
        
    def _setup_ui(self):
        """Setup export dialog UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Export WiFi Scan Data")
        title.setFont(QFont("JetBrains Mono", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Format selection
        format_group = QGroupBox("Export Format")
        format_layout = QVBoxLayout(format_group)
        
        self.format_combo = QComboBox()
        self.format_combo.addItems([
            "CSV (Comma Separated Values)",
            "JSON (JavaScript Object Notation)", 
            "HTML Report (Web Page)"
        ])
        format_layout.addWidget(self.format_combo)
        
        layout.addWidget(format_group)
        
        # Options
        options_group = QGroupBox("Export Options")
        options_layout = QVBoxLayout(options_group)
        
        self.include_metadata_cb = QCheckBox("Include scan metadata")
        self.include_metadata_cb.setChecked(True)
        options_layout.addWidget(self.include_metadata_cb)
        
        self.pretty_format_cb = QCheckBox("Pretty formatting (JSON)")
        self.pretty_format_cb.setChecked(True)
        options_layout.addWidget(self.pretty_format_cb)
        
        layout.addWidget(options_group)
        
        # File selection
        file_group = QGroupBox("Output File")
        file_layout = QVBoxLayout(file_group)
        
        file_selection_layout = QHBoxLayout()
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setPlaceholderText("Select output file...")
        file_selection_layout.addWidget(self.file_path_edit)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self._browse_file)
        file_selection_layout.addWidget(browse_btn)
        
        file_layout.addLayout(file_selection_layout)
        layout.addWidget(file_group)
        
        # Preview
        preview_group = QGroupBox("Data Preview")
        preview_layout = QVBoxLayout(preview_group)
        
        self.preview_text = QTextEdit()
        self.preview_text.setMaximumHeight(100)
        self.preview_text.setReadOnly(True)
        self._update_preview()
        preview_layout.addWidget(self.preview_text)
        
        layout.addWidget(preview_group)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        export_btn = QPushButton("Export Data")
        export_btn.clicked.connect(self._export_data)
        buttons_layout.addWidget(export_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        layout.addLayout(buttons_layout)
        
        # Connect signals
        self.format_combo.currentTextChanged.connect(self._format_changed)
        
    def _apply_theme(self):
        """Apply consistent hacker theme"""
        self.setStyleSheet("""
            QDialog {
                background-color: #0a0a0a;
                color: #00ff00;
                font-family: 'JetBrains Mono', monospace;
            }
            QLabel {
                color: #00ff00;
                font-weight: bold;
            }
            QGroupBox {
                font-weight: bold;
                color: #00ff00;
                border: 2px solid #333;
                border-radius: 8px;
                margin-top: 8px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QComboBox, QLineEdit {
                background-color: #1a1a1a;
                color: #00ff00;
                border: 2px solid #555;
                padding: 6px;
                border-radius: 4px;
            }
            QComboBox:focus, QLineEdit:focus {
                border: 2px solid #00ff00;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                border: none;
                width: 12px;
                height: 12px;
            }
            QCheckBox {
                color: #00ff00;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #555;
                background-color: #1a1a1a;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #00ff00;
                background-color: #00ff00;
            }
            QTextEdit {
                background-color: #1a1a1a;
                color: #00ff00;
                border: 2px solid #555;
                font-family: 'Courier New', monospace;
                font-size: 10px;
            }
            QPushButton {
                background-color: #2a2a2a;
                color: #00ff00;
                border: 2px solid #555;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #00ff00;
                color: #000000;
                border: 2px solid #00aa00;
            }
            QPushButton:pressed {
                background-color: #00aa00;
                color: #000000;
            }
            QProgressBar {
                border: 2px solid #555;
                background-color: #1a1a1a;
                text-align: center;
                color: #00ff00;
                border-radius: 4px;
            }
            QProgressBar::chunk {
                background-color: #00ff00;
                border-radius: 2px;
            }
        """)
        
    def _browse_file(self):
        """Browse for output file"""
        format_text = self.format_combo.currentText()
        
        if "CSV" in format_text:
            file_filter = "CSV Files (*.csv)"
            default_ext = ".csv"
        elif "JSON" in format_text:
            file_filter = "JSON Files (*.json)"
            default_ext = ".json"
        elif "HTML" in format_text:
            file_filter = "HTML Files (*.html)"
            default_ext = ".html"
        else:
            file_filter = "All Files (*)"
            default_ext = ""
            
        default_name = f"wifi_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}{default_ext}"
        
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Export WiFi Data", default_name, file_filter
        )
        
        if filepath:
            self.file_path_edit.setText(filepath)
            
    def _format_changed(self, format_text):
        """Handle format selection change"""
        self._update_preview()
        
        # Update file extension if path exists
        current_path = self.file_path_edit.text()
        if current_path:
            base_path = os.path.splitext(current_path)[0]
            if "CSV" in format_text:
                self.file_path_edit.setText(base_path + ".csv")
            elif "JSON" in format_text:
                self.file_path_edit.setText(base_path + ".json")
            elif "HTML" in format_text:
                self.file_path_edit.setText(base_path + ".html")
                
    def _update_preview(self):
        """Update data preview"""
        if not self.networks_data:
            self.preview_text.setText("No data available for export.")
            return
            
        preview_text = f"Networks to export: {len(self.networks_data)}\n"
        preview_text += f"Sample data (first network):\n"
        
        if self.networks_data:
            sample_network = self.networks_data[0]
            for key, value in list(sample_network.items())[:5]:  # Show first 5 fields
                preview_text += f"  {key}: {value}\n"
            if len(sample_network) > 5:
                preview_text += f"  ... and {len(sample_network) - 5} more fields\n"
                
        self.preview_text.setText(preview_text)
        
    def _export_data(self):
        """Perform the data export"""
        if not self.file_path_edit.text():
            QMessageBox.warning(self, "Error", "Please select an output file.")
            return
            
        if not self.networks_data:
            QMessageBox.warning(self, "Error", "No data available for export.")
            return
            
        # Show progress
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate
        
        # Prepare export data
        export_data = ExportData(
            networks=self.networks_data,
            scan_metadata={
                "total_networks": len(self.networks_data),
                "export_timestamp": datetime.now().isoformat(),
                "format_version": "1.0",
                "exported_by": "WiFi Security Radar Suite v5.0"
            } if self.include_metadata_cb.isChecked() else {},
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        # Perform export
        filepath = self.file_path_edit.text()
        format_text = self.format_combo.currentText()
        success = False
        
        try:
            if "CSV" in format_text:
                success = DataExporter.export_to_csv(export_data, filepath)
            elif "JSON" in format_text:
                pretty = self.pretty_format_cb.isChecked()
                success = DataExporter.export_to_json(export_data, filepath, pretty)
            elif "HTML" in format_text:
                success = DataExporter.export_to_html(export_data, filepath)
                
            if success:
                message = f"Data successfully exported to:\n{filepath}"
                QMessageBox.information(self, "Export Complete", message)
                self.export_completed.emit(True, filepath)
                self.accept()
            else:
                QMessageBox.critical(self, "Export Failed", "Failed to export data. Please check the file path and permissions.")
                self.export_completed.emit(False, "Export failed")
                
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"An error occurred during export:\n{str(e)}")
            self.export_completed.emit(False, str(e))
        finally:
            self.progress_bar.setVisible(False)


# Export functionality for integration
__all__ = [
    'ExportData',
    'DataExporter', 
    'ExportDialog'
]


if __name__ == "__main__":
    # Test the export dialog
    from PyQt5.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    # Sample data for testing
    sample_networks = [
        {
            'ssid': 'TestNetwork1',
            'bssid': '00:11:22:33:44:55',
            'security': 'WPA2',
            'signal': -45,
            'channel': 6,
            'frequency': '2.437 GHz',
            'vendor': 'Test Vendor',
            'last_seen': '2024-01-01 12:00:00'
        },
        {
            'ssid': 'OpenNetwork',
            'bssid': '66:77:88:99:AA:BB',
            'security': 'Open',
            'signal': -65,
            'channel': 11,
            'frequency': '2.462 GHz',
            'vendor': 'Another Vendor',
            'last_seen': '2024-01-01 12:05:00'
        }
    ]
    
    dialog = ExportDialog(sample_networks)
    dialog.show()
    
    sys.exit(app.exec_())