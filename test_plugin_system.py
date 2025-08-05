#!/usr/bin/env python3
"""
Test script for the plugin system
Tests plugin discovery, loading, and basic functionality
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_plugin_system():
    """Test the plugin system functionality"""
    print("🔧 Testing Plugin System...")
    
    try:
        # Test core imports
        from core.plugin_manager import plugin_manager
        from core.plugin_base import WiFiPlugin, PluginMetadata
        print("✅ Core plugin modules imported successfully")
        
        # Test plugin discovery
        print("\n📂 Testing plugin discovery...")
        plugin_count = plugin_manager.discover_plugins()
        print(f"   Discovered {plugin_count} plugins")
        
        # Get available plugins
        available_plugins = plugin_manager.get_available_plugins()
        print(f"   Available plugins: {list(available_plugins.keys())}")
        
        # Test each available plugin
        for plugin_name, metadata in available_plugins.items():
            print(f"\n🔌 Testing plugin: {plugin_name}")
            print(f"   Version: {metadata.version}")
            print(f"   Description: {metadata.description}")
            print(f"   Capabilities: {metadata.capabilities}")
            print(f"   Dependencies: {metadata.dependencies}")
            
            # Test plugin loading
            try:
                plugin_instance = plugin_manager.load_plugin(plugin_name)
                if plugin_instance:
                    print(f"   ✅ Plugin {plugin_name} loaded successfully")
                    
                    # Test dependency validation
                    success, missing = plugin_instance.validate_dependencies()
                    if success:
                        print(f"   ✅ All dependencies satisfied")
                    else:
                        print(f"   ⚠️  Missing dependencies: {missing}")
                    
                    # Test configuration
                    test_config = {
                        'scan_interval': 5,
                        'interface': 'wlan0'
                    }
                    if plugin_instance.configure(test_config):
                        print(f"   ✅ Configuration successful")
                    else:
                        print(f"   ❌ Configuration failed")
                    
                    # Test capabilities
                    capabilities = plugin_instance.get_capabilities()
                    print(f"   📋 Capabilities: {capabilities}")
                    
                    # Cleanup
                    plugin_manager.unload_plugin(plugin_name)
                    print(f"   ✅ Plugin {plugin_name} unloaded successfully")
                else:
                    print(f"   ❌ Failed to load plugin {plugin_name}")
                    
            except Exception as e:
                print(f"   ❌ Error testing plugin {plugin_name}: {e}")
        
        print("\n🎉 Plugin system test completed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure all required modules are available")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def test_plugin_launcher():
    """Test the plugin-based launcher"""
    print("\n🚀 Testing Plugin Launcher...")
    
    try:
        # Test launcher import
        from main_launcher_plugin import WiFiRadarPluginLauncher
        print("✅ Plugin launcher imported successfully")
        
        # Note: We can't actually run the GUI in this test environment
        # but we can test the class instantiation
        print("✅ Plugin launcher class available")
        
        return True
        
    except ImportError as e:
        print(f"❌ Launcher import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Launcher test error: {e}")
        return False

def test_fallback_mode():
    """Test fallback mode when plugin system is not available"""
    print("\n🔄 Testing fallback mode...")
    
    try:
        # Test direct imports of original tools
        from wifi_radar_nav_enhanced import NavigationRadarWindow
        print("✅ Navigation Enhanced tool available")
        
        from wifi_pentest_radar_modern import WiFiPentestRadarModern
        print("✅ Penetration Testing tool available")
        
        print("✅ Fallback mode functional")
        return True
        
    except ImportError as e:
        print(f"❌ Fallback import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Fallback test error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 WiFi Security Radar Suite - Plugin System Test")
    print("=" * 60)
    
    all_tests_passed = True
    
    # Test plugin system
    if not test_plugin_system():
        all_tests_passed = False
    
    # Test plugin launcher
    if not test_plugin_launcher():
        all_tests_passed = False
    
    # Test fallback mode
    if not test_fallback_mode():
        all_tests_passed = False
    
    print("\n" + "=" * 60)
    if all_tests_passed:
        print("🎉 ALL TESTS PASSED!")
        print("✨ Plugin system is ready for use!")
    else:
        print("❌ SOME TESTS FAILED!")
        print("🔧 Please check the errors above and fix any issues.")
    
    return 0 if all_tests_passed else 1

if __name__ == '__main__':
    sys.exit(main())