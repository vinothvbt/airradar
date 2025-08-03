#!/usr/bin/env python3
"""
WiFi Security Radar Suite - Main Launcher
Choose between the navigation-enhanced interface or penetration testing radar
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap


class WiFiRadarLauncher(QDialog):
    """Main launcher for WiFi Security Radar Suite"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("WiFi Security Radar Suite")
        self.setFixedSize(700, 500)
        self.selected_program = None
        self._setup_ui()
        self._apply_theme()

    def _setup_ui(self):
        """Setup the launcher UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(25)
        layout.setContentsMargins(40, 40, 40, 40)

        # Title
        title = QLabel("WiFi Security Radar Suite v5.0")
        title.setFont(QFont("JetBrains Mono", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("Professional WiFi Security Analysis Tools")
        subtitle.setFont(QFont("JetBrains Mono", 12))
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        # Description
        description = QLabel("""
Choose your preferred interface:

• Navigation Enhanced: Modern interface with comprehensive theming and view modes
• Penetration Testing: Modern radar v4.0 with advanced visualization and analysis
        """)
        description.setFont(QFont("JetBrains Mono", 10))
        description.setAlignment(Qt.AlignCenter)
        layout.addWidget(description)

        # Program selection buttons
        programs_layout = QHBoxLayout()

        # Navigation Enhanced Button
        nav_btn = QPushButton(
            "Navigation Enhanced\n\n• Modern navigation bar\n• Multiple view modes\n• Professional theming\n• Comprehensive analysis")
        nav_btn.setFont(QFont("JetBrains Mono", 10))
        nav_btn.clicked.connect(lambda: self._launch_program('nav'))
        nav_btn.setMinimumHeight(120)
        programs_layout.addWidget(nav_btn)

        # Penetration Testing Button
        pentest_btn = QPushButton(
            "Penetration Testing\n\n• Specialized radar display\n• Vulnerability assessment\n• Attack vector analysis\n• Security evaluation")
        pentest_btn.setFont(QFont("JetBrains Mono", 10))
        pentest_btn.clicked.connect(lambda: self._launch_program('pentest'))
        pentest_btn.setMinimumHeight(120)
        programs_layout.addWidget(pentest_btn)

        layout.addLayout(programs_layout)

        # Exit button
        exit_btn = QPushButton("Exit")
        exit_btn.setFont(QFont("JetBrains Mono", 11, QFont.Bold))
        exit_btn.clicked.connect(self.reject)
        layout.addWidget(exit_btn)

        # Info
        info = QLabel(
            "Note: Both tools require root privileges for WiFi scanning")
        info.setFont(QFont("JetBrains Mono", 9))
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)

    def _apply_theme(self):
        """Apply consistent hacker theme"""
        self.setStyleSheet("""
            QDialog {
                background-color: #0A0A0A;
                color: #00FF00;
                font-family: 'JetBrains Mono', monospace;
            }
            QLabel {
                color: #00FF00;
                font-family: 'JetBrains Mono', monospace;
            }
            QPushButton {
                background-color: #1E1E1E;
                color: #00FF00;
                border: 2px solid #333;
                padding: 15px 25px;
                border-radius: 8px;
                font-family: 'JetBrains Mono', monospace;
                font-weight: bold;
                min-width: 250px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #00FF00;
                color: #000000;
                border: 2px solid #00AA00;
            }
            QPushButton:pressed {
                background-color: #00AA00;
                color: #000000;
            }
        """)

    def _launch_program(self, program_type):
        """Launch the selected program"""
        self.selected_program = program_type
        self.accept()


def main():
    """Main launcher function"""
    app = QApplication(sys.argv)

    # Set application properties
    app.setApplicationName("WiFi Security Radar Suite")
    app.setApplicationVersion("5.0.0")

    # Check root privileges
    if os.geteuid() != 0:
        from PyQt5.QtWidgets import QMessageBox
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Root Privileges Required")
        msg.setText(
            "This application requires root privileges for WiFi scanning.\n\nPlease run with sudo:\nsudo python3 main_launcher.py")
        msg.exec_()
        return 1

    # Show launcher dialog
    launcher = WiFiRadarLauncher()
    if launcher.exec_() == QDialog.Accepted:
        try:
            if launcher.selected_program == 'nav':
                # Launch navigation enhanced version
                from wifi_radar_nav_enhanced import NavigationRadarWindow
                window = NavigationRadarWindow()
                window.show()
                return app.exec_()

            elif launcher.selected_program == 'pentest':
                # Launch modern penetration testing version
                from wifi_pentest_radar_modern import WiFiPentestRadarModern
                window = WiFiPentestRadarModern()
                window.show()
                return app.exec_()

        except ImportError as e:
            from PyQt5.QtWidgets import QMessageBox
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Import Error")
            msg.setText(f"Failed to import WiFi Radar module:\n\n{str(e)}")
            msg.exec_()
            return 1
        except Exception as e:
            from PyQt5.QtWidgets import QMessageBox
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Launch Error")
            msg.setText(f"Failed to launch WiFi Radar:\n\n{str(e)}")
            msg.exec_()
            return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
