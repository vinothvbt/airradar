#!/usr/bin/env python3
"""
Simple test for core plugin system components
Tests basic functionality without GUI dependencies
"""

import sys
import os
from pathlib import Path

def test_core_imports():
    """Test core module imports"""
    print("🔧 Testing core imports...")
    
    try:
        from core.plugin_base import WiFiPlugin, PluginMetadata, WiFiScanResult
        print("✅ plugin_base imported successfully")
        
        from core.plugin_manager import PluginManager
        print("✅ plugin_manager imported successfully")
        
        return True
    except Exception as e:
        print(f"❌ Core import error: {e}")
        return False

def test_plugin_metadata():
    """Test PluginMetadata functionality"""
    print("\n📋 Testing PluginMetadata...")
    
    try:
        from core.plugin_base import PluginMetadata
        
        metadata = PluginMetadata(
            name="Test Plugin",
            version="1.0.0",
            description="A test plugin",
            author="Test Author",
            requires_root=True,
            capabilities=["wifi_scanning", "test_capability"],
            dependencies=["PyQt5"]
        )
        
        print(f"   Name: {metadata.name}")
        print(f"   Version: {metadata.version}")
        print(f"   Capabilities: {metadata.capabilities}")
        print("✅ PluginMetadata working correctly")
        
        return True
    except Exception as e:
        print(f"❌ PluginMetadata error: {e}")
        return False

def test_scan_result():
    """Test WiFiScanResult functionality"""
    print("\n📡 Testing WiFiScanResult...")
    
    try:
        from core.plugin_base import WiFiScanResult
        
        result = WiFiScanResult(
            ssid="TestNetwork",
            bssid="00:11:22:33:44:55",
            signal_strength=-50,
            security="WPA2",
            channel=6,
            frequency="2.437 GHz"
        )
        
        result.vendor = "Test Vendor"
        result.distance = 10.5
        result.additional_data = {"test_field": "test_value"}
        
        result_dict = result.to_dict()
        print(f"   SSID: {result.ssid}")
        print(f"   Signal: {result.signal_strength} dBm")
        print(f"   Dict conversion: {len(result_dict)} fields")
        print("✅ WiFiScanResult working correctly")
        
        return True
    except Exception as e:
        print(f"❌ WiFiScanResult error: {e}")
        return False

def test_plugin_manager():
    """Test PluginManager basic functionality"""
    print("\n🔧 Testing PluginManager...")
    
    try:
        from core.plugin_manager import PluginManager
        
        manager = PluginManager()
        print(f"   Manager created with {len(manager._plugin_paths)} plugin paths")
        
        # Test adding a plugin path
        test_path = Path("/tmp/test_plugins")
        test_path.mkdir(exist_ok=True)
        
        if manager.add_plugin_path(test_path):
            print("✅ Plugin path added successfully")
        else:
            print("❌ Failed to add plugin path")
        
        # Test discovery (should find 0 plugins in empty directory)
        count = manager.discover_plugins()
        print(f"   Discovered {count} plugins")
        
        available = manager.get_available_plugins()
        print(f"   Available plugins: {list(available.keys())}")
        
        print("✅ PluginManager basic functionality working")
        
        return True
    except Exception as e:
        print(f"❌ PluginManager error: {e}")
        return False

def test_plugin_directory_structure():
    """Test plugin directory structure"""
    print("\n📁 Testing plugin directory structure...")
    
    try:
        plugins_dir = Path("plugins")
        core_dir = Path("core")
        
        if plugins_dir.exists():
            print(f"✅ Plugins directory exists: {plugins_dir}")
            plugin_files = list(plugins_dir.glob("*.py"))
            print(f"   Found {len(plugin_files)} plugin files")
            for pf in plugin_files:
                print(f"   - {pf.name}")
        else:
            print("❌ Plugins directory not found")
            return False
        
        if core_dir.exists():
            print(f"✅ Core directory exists: {core_dir}")
            core_files = list(core_dir.glob("*.py"))
            print(f"   Found {len(core_files)} core files")
            for cf in core_files:
                print(f"   - {cf.name}")
        else:
            print("❌ Core directory not found")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Directory structure error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 WiFi Security Radar Suite - Core Plugin System Test")
    print("=" * 65)
    
    all_tests_passed = True
    
    tests = [
        test_core_imports,
        test_plugin_metadata,
        test_scan_result,
        test_plugin_manager,
        test_plugin_directory_structure
    ]
    
    for test_func in tests:
        if not test_func():
            all_tests_passed = False
    
    print("\n" + "=" * 65)
    if all_tests_passed:
        print("🎉 ALL CORE TESTS PASSED!")
        print("✨ Core plugin system is functional!")
    else:
        print("❌ SOME TESTS FAILED!")
        print("🔧 Please check the errors above.")
    
    return 0 if all_tests_passed else 1

if __name__ == '__main__':
    sys.exit(main())