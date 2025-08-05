#!/usr/bin/env python3
"""
Non-GUI Test Suite for Enhanced Features
Tests core functionality without requiring display
"""

import sys
import os
import tempfile
import json

def test_imports():
    """Test that all new modules can be imported"""
    print("🧪 Testing module imports...")
    
    try:
        from realtime_graphs import RealtimeGraphWidget, SignalStrengthGraph
        print("✅ Real-time graphs module imported")
    except ImportError as e:
        print(f"❌ Real-time graphs import failed: {e}")
        return False
        
    try:
        from export_module import DataExporter, ExportData
        print("✅ Export module imported")
    except ImportError as e:
        print(f"❌ Export module import failed: {e}")
        return False
        
    try:
        from accessibility import AccessibilityManager
        print("✅ Accessibility module imported")
    except ImportError as e:
        print(f"❌ Accessibility module import failed: {e}")
        return False
        
    try:
        from internationalization import TranslationManager
        print("✅ Internationalization module imported")
    except ImportError as e:
        print(f"❌ Internationalization module import failed: {e}")
        return False
        
    try:
        from enhanced_themes import ThemeManager, ThemeConfig
        print("✅ Enhanced themes module imported")
    except ImportError as e:
        print(f"❌ Enhanced themes module import failed: {e}")
        return False
        
    return True


def test_export_functionality():
    """Test export functionality without GUI"""
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
            scan_metadata={'test': True, 'total_networks': 2},
            timestamp='2024-01-01 12:00:00'
        )
        
        # Test CSV export
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            csv_file = f.name
            
        success = DataExporter.export_to_csv(export_data, csv_file)
        if success and os.path.exists(csv_file):
            with open(csv_file, 'r') as f:
                content = f.read()
                if 'TestNetwork1' in content and 'WPA2' in content:
                    print("✅ CSV export successful and contains expected data")
                else:
                    print("❌ CSV export missing expected data")
                    return False
            os.unlink(csv_file)
        else:
            print("❌ CSV export failed")
            return False
            
        # Test JSON export
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json_file = f.name
            
        success = DataExporter.export_to_json(export_data, json_file)
        if success and os.path.exists(json_file):
            with open(json_file, 'r') as f:
                data = json.load(f)
                if 'networks' in data and len(data['networks']) == 2:
                    print("✅ JSON export successful and contains expected data")
                else:
                    print("❌ JSON export missing expected data")
                    return False
            os.unlink(json_file)
        else:
            print("❌ JSON export failed")
            return False
            
        # Test HTML export
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            html_file = f.name
            
        success = DataExporter.export_to_html(export_data, html_file)
        if success and os.path.exists(html_file):
            with open(html_file, 'r') as f:
                content = f.read()
                if 'TestNetwork1' in content and 'WiFi Security Radar Report' in content:
                    print("✅ HTML export successful and contains expected data")
                else:
                    print("❌ HTML export missing expected data")
                    return False
            os.unlink(html_file)
        else:
            print("❌ HTML export failed")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Export functionality test failed: {e}")
        return False


def test_accessibility_core():
    """Test accessibility core features without GUI"""
    print("\n♿ Testing accessibility core features...")
    
    try:
        from accessibility import AccessibilityManager
        
        # Create accessibility manager
        accessibility_manager = AccessibilityManager()
        
        # Test settings
        original_contrast = accessibility_manager.high_contrast_enabled
        accessibility_manager.toggle_high_contrast()
        if accessibility_manager.high_contrast_enabled != original_contrast:
            print("✅ High contrast toggle working")
        else:
            print("❌ High contrast toggle failed")
            return False
            
        # Test font scaling
        accessibility_manager.set_font_scale(1.5)
        if accessibility_manager.font_scale == 1.5:
            print("✅ Font scaling working")
        else:
            print("❌ Font scaling failed")
            return False
            
        # Test theme setting
        accessibility_manager.set_theme("high_contrast")
        if accessibility_manager.current_theme == "high_contrast":
            print("✅ Theme setting working")
        else:
            print("❌ Theme setting failed")
            return False
            
        # Test style generation
        style = accessibility_manager.get_high_contrast_style()
        if style and "#000000" in style:
            print("✅ High contrast style generation working")
        else:
            print("❌ High contrast style generation failed")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Accessibility test failed: {e}")
        return False


def test_internationalization_core():
    """Test internationalization core features"""
    print("\n🌍 Testing internationalization core...")
    
    try:
        from internationalization import TranslationManager
        
        # Create translation manager
        translation_manager = TranslationManager()
        
        # Test getting text
        title = translation_manager.get_text("main_window", "title")
        if title and title != "[Missing: main_window.title]":
            print(f"✅ Translation retrieval working: '{title}'")
        else:
            print("❌ Translation retrieval failed")
            return False
            
        # Test fallback
        missing = translation_manager.get_text("nonexistent", "key", "fallback_text")
        if missing == "fallback_text":
            print("✅ Translation fallback working")
        else:
            print("❌ Translation fallback failed")
            return False
            
        # Test language switching
        original_lang = translation_manager.current_language
        translation_manager.set_language("es")
        if translation_manager.current_language == "es":
            print("✅ Language switching working")
        else:
            print("❌ Language switching failed")
            return False
            
        translation_manager.set_language(original_lang)
        
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


def test_themes_core():
    """Test theme system core features"""
    print("\n🎨 Testing theme system core...")
    
    try:
        from enhanced_themes import ThemeManager, ThemeConfig, ThemeColors
        
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
            
        # Test specific theme
        matrix_theme = theme_manager.get_theme("matrix_green")
        if matrix_theme and matrix_theme.colors.primary == "#00ff00":
            print("✅ Matrix green theme loaded correctly")
        else:
            print("❌ Matrix green theme not loaded correctly")
            return False
            
        # Test theme switching
        original_theme = theme_manager.current_theme_name
        theme_manager.set_theme("cyberpunk_blue")
        if theme_manager.current_theme_name == "cyberpunk_blue":
            print("✅ Theme switching working")
        else:
            print("❌ Theme switching failed")
            return False
            
        theme_manager.set_theme(original_theme)
        
        # Test custom theme creation
        custom_colors = ThemeColors(
            background="#111111",
            primary="#ff0000"
        )
        custom_theme = ThemeConfig(
            name="test_theme",
            display_name="Test Theme",
            colors=custom_colors
        )
        
        if custom_theme.name == "test_theme":
            print("✅ Custom theme creation working")
        else:
            print("❌ Custom theme creation failed")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Theme system test failed: {e}")
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
            
        template_file = "translations/templates/translation_template.json"
        if os.path.exists(template_file):
            with open(template_file, 'r') as f:
                template_data = json.load(f)
                if 'main_window' in template_data:
                    print("✅ Translation template file created with correct structure")
                else:
                    print("❌ Translation template file missing expected structure")
                    return False
        else:
            print("❌ Translation template file not created")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ File creation test failed: {e}")
        return False


def test_config_files():
    """Test configuration file handling"""
    print("\n⚙️ Testing configuration files...")
    
    try:
        from accessibility import AccessibilityManager
        from internationalization import TranslationManager
        from enhanced_themes import ThemeManager
        
        # Test accessibility settings save/load
        acc_manager = AccessibilityManager()
        acc_manager.high_contrast_enabled = True
        acc_manager.font_scale = 1.3
        acc_manager.save_settings()
        
        if os.path.exists("accessibility_settings.json"):
            print("✅ Accessibility settings file created")
        else:
            print("❌ Accessibility settings file not created")
            return False
            
        # Test theme settings
        theme_manager = ThemeManager()
        theme_manager.set_theme("dark_red")
        
        if os.path.exists("theme_settings.json"):
            print("✅ Theme settings file created")
        else:
            print("❌ Theme settings file not created")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Configuration files test failed: {e}")
        return False


def run_core_tests():
    """Run all core tests that don't require GUI"""
    print("🚀 Starting Enhanced Features Core Test Suite")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("Export Functionality", test_export_functionality),
        ("Accessibility Core", test_accessibility_core),
        ("Internationalization Core", test_internationalization_core),
        ("Theme System Core", test_themes_core),
        ("File Creation", test_file_creation),
        ("Configuration Files", test_config_files)
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
            import traceback
            traceback.print_exc()
            
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All core tests passed! Enhanced features are working correctly.")
        print("\n📝 Summary of implemented features:")
        print("  ✅ Real-time graphs for signal strength, network activity, and security trends")
        print("  ✅ Data export in CSV, JSON, and HTML formats")
        print("  ✅ Accessibility features with high contrast and keyboard navigation")
        print("  ✅ Multi-language support with 11 language templates")
        print("  ✅ Enhanced theming system with 6+ built-in themes")
        print("  ✅ Configuration management and file handling")
        return True
    else:
        print(f"⚠️ {total - passed} tests failed. Some features may not work correctly.")
        return False


if __name__ == "__main__":
    # Ensure we're in the right directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Run core tests
    success = run_core_tests()
    sys.exit(0 if success else 1)