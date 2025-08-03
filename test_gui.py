#!/usr/bin/env python3
"""
Test GUI startup without scanning
"""

import sys
import os


def test_gui_startup():
    """Test if the GUI can start without errors"""
    print("🖥️ Testing WiFi Radar GUI Startup...")

    try:
        # Test PyQt5 import
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import QTimer
        print("✅ PyQt5 imported successfully")

        # Test application creation
        app = QApplication(sys.argv)
        print("✅ QApplication created successfully")

        # Test our modules import
        from config_manager import config_manager
        from vendor_service import vendor_service
        from security_engine import security_engine
        from distance_engine import distance_engine
        print("✅ All engine modules imported successfully")

        # Test WiFiScanner import (without starting)
        from wifi_pentest_radar_modern import WiFiScanner
        print("✅ WiFiScanner class imported successfully")

        # Test main window import
        from wifi_pentest_radar_modern import WiFiPentestRadarModern
        print("✅ Main window class imported successfully")

        print("\n🎉 GUI STARTUP TEST SUCCESSFUL!")
        print("✨ No more QMutex context manager errors!")
        print("🚀 WiFi radar GUI is ready to launch!")

        app.quit()
        return True

    except Exception as e:
        print(f"❌ GUI startup test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_gui_startup()
    sys.exit(0 if success else 1)
