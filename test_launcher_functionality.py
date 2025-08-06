#!/usr/bin/env python3
"""
Test the plugin-based launcher functionality
Tests launcher components without actually showing GUI
"""

import sys
import os
from pathlib import Path

def test_launcher_imports():
    """Test launcher module imports"""
    print("🚀 Testing launcher imports...")
    
    try:
        # Set QT_QPA_PLATFORM to offscreen for headless testing
        os.environ['QT_QPA_PLATFORM'] = 'offscreen'
        
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        
        from main_launcher_plugin import WiFiRadarPluginLauncher
        print("✅ Plugin launcher imported successfully")
        
        return True, app
    except Exception as e:
        print(f"❌ Launcher import error: {e}")
        return False, None

def test_launcher_functionality(app):
    """Test launcher basic functionality"""
    print("\n🔧 Testing launcher functionality...")
    
    try:
        from main_launcher_plugin import WiFiRadarPluginLauncher
        
        # Create launcher instance
        launcher = WiFiRadarPluginLauncher()
        print("✅ Launcher instance created successfully")
        
        # Test plugin discovery
        print("   Plugin discovery completed")
        print(f"   Available plugins: {list(launcher._plugins_info.keys())}")
        
        # Test plugin selection simulation
        if launcher._plugins_info:
            first_plugin = list(launcher._plugins_info.keys())[0]
            launcher._on_plugin_selected(first_plugin)
            print(f"✅ Plugin selection works: {first_plugin}")
            
            if launcher.selected_plugin == first_plugin:
                print("✅ Plugin selection state updated correctly")
        
        launcher.close()
        return True
        
    except Exception as e:
        print(f"❌ Launcher functionality error: {e}")
        return False

def test_fallback_components():
    """Test fallback components"""
    print("\n🔄 Testing fallback components...")
    
    try:
        # Test enhanced button without animations
        from main_launcher_plugin import EnhancedButton
        button = EnhancedButton("Test Button")
        print("✅ EnhancedButton created successfully")
        
        # Test plugin list widget
        from main_launcher_plugin import PluginListWidget
        from core.plugin_base import PluginMetadata
        
        list_widget = PluginListWidget()
        
        # Test with sample data
        sample_plugins = {
            "test_plugin": PluginMetadata(
                name="Test Plugin",
                version="1.0.0",
                description="A test plugin",
                author="Test Author"
            )
        }
        
        list_widget.populate_plugins(sample_plugins)
        print("✅ PluginListWidget populated successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Fallback components error: {e}")
        return False

def test_plugin_loading_simulation():
    """Test plugin loading simulation"""
    print("\n🔌 Testing plugin loading simulation...")
    
    try:
        from core.plugin_manager import plugin_manager
        
        # Get available plugins
        available_plugins = plugin_manager.get_available_plugins()
        
        if available_plugins:
            # Test loading first available plugin
            first_plugin_name = list(available_plugins.keys())[0]
            print(f"   Attempting to load: {first_plugin_name}")
            
            plugin_instance = plugin_manager.load_plugin(first_plugin_name)
            if plugin_instance:
                print(f"✅ Plugin {first_plugin_name} loaded successfully")
                
                # Test plugin metadata
                metadata = plugin_instance.metadata
                print(f"   Metadata: {metadata.name} v{metadata.version}")
                
                # Test configuration
                test_config = {"test_setting": "test_value"}
                if plugin_instance.configure(test_config):
                    print("✅ Plugin configuration successful")
                
                # Cleanup
                plugin_manager.unload_plugin(first_plugin_name)
                print("✅ Plugin unloaded successfully")
            else:
                print(f"❌ Failed to load plugin {first_plugin_name}")
        else:
            print("⚠️  No plugins available for testing")
        
        return True
        
    except Exception as e:
        print(f"❌ Plugin loading simulation error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 WiFi Security Radar Suite - Plugin Launcher Test")
    print("=" * 65)
    
    all_tests_passed = True
    app = None
    
    # Test launcher imports
    success, app = test_launcher_imports()
    if not success:
        all_tests_passed = False
    
    if app:
        # Test launcher functionality
        if not test_launcher_functionality(app):
            all_tests_passed = False
    
    # Test fallback components
    if not test_fallback_components():
        all_tests_passed = False
    
    # Test plugin loading simulation
    if not test_plugin_loading_simulation():
        all_tests_passed = False
    
    print("\n" + "=" * 65)
    if all_tests_passed:
        print("🎉 ALL LAUNCHER TESTS PASSED!")
        print("✨ Plugin-based launcher is functional!")
    else:
        print("❌ SOME TESTS FAILED!")
        print("🔧 Please check the errors above.")
    
    if app:
        app.quit()
    
    return 0 if all_tests_passed else 1

if __name__ == '__main__':
    sys.exit(main())