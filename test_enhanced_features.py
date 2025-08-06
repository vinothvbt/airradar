#!/usr/bin/env python3
"""
Test Suite for Enhanced GUI Features
Tests all new features: real-time graphs, export, accessibility, i18n, themes
"""

import sys
import os
import tempfile
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer

def test_imports():
    """Test that all new modules can be imported"""
    print("🧪 Testing module imports...")
    
    try:
        from realtime_graphs import RealtimeGraphsPanel, SignalStrengthGraph
        print("✅ Real-time graphs module imported")
    except ImportError as e:
        print(f"❌ Real-time graphs import failed: {e}")
        return False
        
    try:
        from export_module import ExportDialog, DataExporter
        print("✅ Export module imported")
    except ImportError as e:
        print(f"❌ Export module import failed: {e}")
        return False
        
    try:
        from accessibility import AccessibilityManager, AccessibilityDialog
        print("✅ Accessibility module imported")
    except ImportError as e:
        print(f"❌ Accessibility module import failed: {e}")
        return False
        
    try:
        from internationalization import TranslationManager, LanguageDialog
        print("✅ Internationalization module imported")
    except ImportError as e:
        print(f"❌ Internationalization module import failed: {e}")
        return False
        
    try:
        from enhanced_themes import ThemeManager, ThemeCustomizerDialog
        print("✅ Enhanced themes module imported")
    except ImportError as e:
        print(f"❌ Enhanced themes module import failed: {e}")
        return False
        
    try:
        from gui_enhancements import EnhancedFeatureIntegrator, enhance_existing_window
        print("✅ GUI enhancements module imported")
    except ImportError as e:
        print(f"❌ GUI enhancements module import failed: {e}")
        return False
        
    return True


def test_realtime_graphs():
    """Test real-time graphs functionality"""
    print("\n📊 Testing real-time graphs...")
    
    try:
        from realtime_graphs import RealtimeGraphsPanel
        
        app = QApplication.instance() or QApplication(sys.argv)
        
        # Create graphs panel
        panel = RealtimeGraphsPanel()
        
        # Test adding sample data
        sample_networks = [
            {'ssid': 'TestNet1', 'signal': -45, 'security': 'WPA2'},
            {'ssid': 'TestNet2', 'signal': -65, 'security': 'Open'},
            {'ssid': 'TestNet3', 'signal': -55, 'security': 'WPA3'}
        ]
        
        panel.update_with_real_data(sample_networks)
        print("✅ Real-time graphs data update successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Real-time graphs test failed: {e}")
        return False


def test_export_functionality():
    """Test export functionality"""
    print("\n📤 Testing export functionality...")
    
    try:
        from export_module import DataExporter, ExportData
        
        # Create sample data
        sample_networks = [
            {
                'ssid': 'TestNetwork1',
                'bssid': '00:11:22:33:44:55',
                'security': 'WPA2',
                'signal': -45,
                'channel': 6,
                'frequency': '2.437 GHz'
            },
            {
                'ssid': 'TestNetwork2',
                'bssid': '66:77:88:99:AA:BB',
                'security': 'Open',
                'signal': -65,
                'channel': 11,
                'frequency': '2.462 GHz'
            }
        ]
        
        export_data = ExportData(
            networks=sample_networks,
            scan_metadata={'test': True},
            timestamp='2024-01-01 12:00:00'
        )
        
        # Test CSV export
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            csv_file = f.name
            
        success = DataExporter.export_to_csv(export_data, csv_file)
        if success and os.path.exists(csv_file):
            print("✅ CSV export successful")
            os.unlink(csv_file)
        else:
            print("❌ CSV export failed")
            return False
            
        # Test JSON export
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json_file = f.name
            
        success = DataExporter.export_to_json(export_data, json_file)
        if success and os.path.exists(json_file):
            print("✅ JSON export successful")
            os.unlink(json_file)
        else:
            print("❌ JSON export failed")
            return False
            
        # Test HTML export
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            html_file = f.name
            
        success = DataExporter.export_to_html(export_data, html_file)
        if success and os.path.exists(html_file):
            print("✅ HTML export successful")
            os.unlink(html_file)
        else:
            print("❌ HTML export failed")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Export functionality test failed: {e}")
        return False


def test_accessibility():
    """Test accessibility features"""
    print("\n♿ Testing accessibility features...")
    
    try:
        from accessibility import AccessibilityManager, apply_accessibility_to_widget
        
        app = QApplication.instance() or QApplication(sys.argv)
        
        # Create accessibility manager
        accessibility_manager = AccessibilityManager()
        
        # Test settings
        accessibility_manager.toggle_high_contrast()
        accessibility_manager.set_font_scale(1.2)
        accessibility_manager.set_theme("high_contrast")
        
        print("✅ Accessibility manager functionality working")
        
        # Test applying to widget
        test_widget = QWidget()
        nav_handler = apply_accessibility_to_widget(test_widget)
        
        if nav_handler:
            print("✅ Accessibility widget enhancement working")
        else:
            print("❌ Accessibility widget enhancement failed")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Accessibility test failed: {e}")
        return False


def test_internationalization():
    """Test internationalization features"""
    print("\n🌍 Testing internationalization...")
    
    try:
        from internationalization import TranslationManager
        
        # Create translation manager
        translation_manager = TranslationManager()
        
        # Test getting text
        title = translation_manager.get_text("main_window", "title")
        if title:
            print(f"✅ Translation retrieval working: '{title}'")
        else:
            print("❌ Translation retrieval failed")
            return False
            
        # Test language switching
        original_lang = translation_manager.current_language
        translation_manager.set_language("es")
        translation_manager.set_language(original_lang)
        
        print("✅ Language switching working")
        
        # Test available languages
        languages = translation_manager.get_available_languages()
        if len(languages) > 1:
            print(f"✅ Multiple languages available: {len(languages)}")
        else:
            print("❌ Insufficient languages available")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Internationalization test failed: {e}")
        return False


def test_themes():
    """Test theme system"""
    print("\n🎨 Testing theme system...")
    
    try:
        from enhanced_themes import ThemeManager
        
        # Create theme manager
        theme_manager = ThemeManager()
        
        # Test getting themes
        themes = theme_manager.get_available_themes()
        if len(themes) > 1:
            print(f"✅ Multiple themes available: {len(themes)}")
        else:
            print("❌ Insufficient themes available")
            return False
            
        # Test stylesheet generation
        stylesheet = theme_manager.create_stylesheet()
        if stylesheet and len(stylesheet) > 100:
            print("✅ Theme stylesheet generation working")
        else:
            print("❌ Theme stylesheet generation failed")
            return False
            
        # Test theme switching
        original_theme = theme_manager.current_theme_name
        for theme_name in list(themes.keys())[:2]:
            theme_manager.set_theme(theme_name)
            
        theme_manager.set_theme(original_theme)
        print("✅ Theme switching working")
        
        return True
        
    except Exception as e:
        print(f"❌ Theme system test failed: {e}")
        return False


def test_gui_integration():
    """Test GUI integration"""
    print("\n🔧 Testing GUI integration...")
    
    try:
        from gui_enhancements import EnhancedMainWindow, enhance_existing_window
        
        app = QApplication.instance() or QApplication(sys.argv)
        
        # Test enhanced main window
        enhanced_window = EnhancedMainWindow()
        enhanced_window.setWindowTitle("Enhanced Test Window")
        
        if hasattr(enhanced_window, 'feature_integrator'):
            print("✅ Enhanced main window creation working")
        else:
            print("❌ Enhanced main window creation failed")
            return False
            
        # Test enhancing existing window
        basic_window = QMainWindow()
        enhanced_basic = enhance_existing_window(basic_window)
        
        if hasattr(enhanced_basic, 'feature_integrator'):
            print("✅ Existing window enhancement working")
        else:
            print("❌ Existing window enhancement failed")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ GUI integration test failed: {e}")
        return False


def test_file_creation():
    """Test that necessary files and directories are created"""
    print("\n📁 Testing file creation...")
    
    try:
        from internationalization import create_translation_file_template
        
        # Test translation template creation
        create_translation_file_template()
        
        if os.path.exists("translations"):
            print("✅ Translations directory created")
        else:
            print("❌ Translations directory not created")
            return False
            
        if os.path.exists("translations/templates"):
            print("✅ Translation templates directory created")
        else:
            print("❌ Translation templates directory not created")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ File creation test failed: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("🚀 Starting Enhanced GUI Features Test Suite")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("Real-time Graphs", test_realtime_graphs),
        ("Export Functionality", test_export_functionality),
        ("Accessibility", test_accessibility),
        ("Internationalization", test_internationalization),
        ("Theme System", test_themes),
        ("GUI Integration", test_gui_integration),
        ("File Creation", test_file_creation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} test failed")
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Enhanced GUI features are working correctly.")
        return True
    else:
        print(f"⚠️ {total - passed} tests failed. Some features may not work correctly.")
        return False


if __name__ == "__main__":
    # Ensure we're in the right directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Run tests
    success = run_all_tests()
    sys.exit(0 if success else 1)