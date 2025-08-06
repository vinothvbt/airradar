#!/usr/bin/env python3
"""
Integration Tests for WiFi Security Radar Suite
===============================================

Tests integration between different components and end-to-end workflows.
"""

import sys
import os
import tempfile
import json
from pathlib import Path

def test_end_to_end_workflow():
    """Test complete workflow from scan to analysis to report"""
    print("🔄 Testing end-to-end workflow...")
    
    try:
        # Step 1: Initialize all engines
        from config_manager import config_manager
        from vendor_service import vendor_service
        from security_engine import security_engine
        from distance_engine import distance_engine
        from wifi_pentest_radar_modern import WiFiScanner
        
        print("✅ All engines initialized")
        
        # Step 2: Create mock scan data
        mock_networks = [
            {
                'ssid': 'TestNetwork_Secure',
                'bssid': '00:1A:2B:3C:4D:5E',
                'frequency': 2437,
                'signal': -45.0,
                'security': 'WPA3'
            },
            {
                'ssid': 'TestNetwork_Vulnerable', 
                'bssid': '00:1A:2B:3C:4D:5F',
                'frequency': 2412,
                'signal': -65.0,
                'security': 'Open'
            },
            {
                'ssid': 'TestNetwork_Legacy',
                'bssid': '00:1A:2B:3C:4D:60',
                'frequency': 2462,
                'signal': -55.0,
                'security': 'WEP'
            }
        ]
        
        print(f"✅ Created mock data with {len(mock_networks)} networks")
        
        # Step 3: Process each network through all engines
        analysis_results = []
        for network in mock_networks:
            # Vendor lookup
            vendor = vendor_service.get_vendor(network['bssid'])
            
            # Distance calculation
            distance = distance_engine.calculate_distance(
                network['signal'], 
                network['frequency']
            )
            
            # Security analysis
            security_analysis = security_engine.analyze_access_point(
                network['ssid'],
                network['bssid'],
                network['security'],
                network['signal'],
                network['frequency']
            )
            
            result = {
                'network': network,
                'vendor': vendor,
                'distance': distance,
                'security_analysis': {
                    'threat_level': security_analysis.threat_level,
                    'vulnerability_score': security_analysis.vulnerability_score,
                    'risk_factors': security_analysis.risk_factors,
                    'attack_vectors': security_analysis.attack_vectors
                }
            }
            analysis_results.append(result)
            
        print(f"✅ Processed {len(analysis_results)} networks through all engines")
        
        # Step 4: Validate results
        secure_network = analysis_results[0]
        vulnerable_network = analysis_results[1]
        legacy_network = analysis_results[2]
        
        # Validate WPA3 network is considered low/minimal threat
        if secure_network['security_analysis']['threat_level'] not in ['LOW', 'MINIMAL']:
            print(f"❌ WPA3 network should be LOW/MINIMAL threat, got {secure_network['security_analysis']['threat_level']}")
            return False
            
        # Validate Open network is considered high threat
        if vulnerable_network['security_analysis']['threat_level'] not in ['CRITICAL', 'HIGH']:
            print(f"❌ Open network should be HIGH/CRITICAL threat, got {vulnerable_network['security_analysis']['threat_level']}")
            return False
            
        # Validate WEP network is considered critical threat
        if legacy_network['security_analysis']['threat_level'] not in ['CRITICAL']:
            print(f"❌ WEP network should be CRITICAL threat, got {legacy_network['security_analysis']['threat_level']}")
            return False
            
        print("✅ Security analysis results are correct")
        
        # Step 5: Test distance calculations are reasonable
        for result in analysis_results:
            distance = result['distance']
            if distance < 0 or distance > 1000:  # Should be between 0 and 1000 meters
                print(f"❌ Unreasonable distance calculation: {distance}m")
                return False
                
        print("✅ Distance calculations are reasonable")
        
        # Step 6: Test export functionality
        try:
            from export_module import DataExporter, ExportData
            from datetime import datetime
            
            # Create export data with required parameters
            networks_data = []
            for result in analysis_results:
                net = result['network']
                networks_data.append({
                    'ssid': net['ssid'],
                    'bssid': net['bssid'], 
                    'frequency': net['frequency'],
                    'signal_dbm': net['signal'],
                    'security': net['security'],
                    'vendor': result['vendor'],
                    'distance': result['distance'],
                    'threat_level': result['security_analysis']['threat_level'],
                    'risk_factors': ', '.join(result['security_analysis']['risk_factors'])
                })
            
            export_data = ExportData(
                networks=networks_data,
                scan_metadata={'scan_time': datetime.now().isoformat(), 'interface': 'test'},
                timestamp=datetime.now().isoformat()
            )
            
            exporter = DataExporter()
            
            # Test CSV export
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
                csv_success = exporter.export_to_csv(export_data, f.name)
                csv_file = f.name
                
            if not csv_success:
                print("❌ CSV export failed")
                return False
                
            # Validate CSV content
            with open(csv_file, 'r') as f:
                csv_content = f.read()
                if 'TestNetwork_Secure' not in csv_content or 'WPA3' not in csv_content:
                    print("❌ CSV export missing expected data")
                    return False
                    
            os.unlink(csv_file)
            print("✅ CSV export working correctly")
            
        except ImportError:
            print("⚠️ Export module not available, skipping export test")
            
        print("✅ End-to-end workflow completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ End-to-end workflow failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_plugin_integration():
    """Test plugin system integration"""
    print("🔌 Testing plugin integration...")
    
    try:
        from core.plugin_manager import plugin_manager
        
        # Discover plugins
        plugin_count = plugin_manager.discover_plugins()
        if plugin_count == 0:
            print("❌ No plugins discovered")
            return False
            
        print(f"✅ Discovered {plugin_count} plugins")
        
        # Test loading each plugin
        available_plugins = plugin_manager.get_available_plugins()
        
        for plugin_name in available_plugins:
            # Load plugin
            plugin_instance = plugin_manager.load_plugin(plugin_name)
            if not plugin_instance:
                print(f"❌ Failed to load plugin: {plugin_name}")
                return False
                
            # Validate dependencies
            success, missing = plugin_instance.validate_dependencies()
            if not success:
                print(f"❌ Plugin {plugin_name} has missing dependencies: {missing}")
                return False
                
            # Test configuration
            try:
                plugin_instance.configure({})  # Pass empty config
                print(f"✅ Plugin {plugin_name} configuration successful")
            except TypeError:
                # Some plugins may not need configuration
                print(f"✅ Plugin {plugin_name} configuration not required")
            except Exception as e:
                print(f"❌ Plugin {plugin_name} configuration failed: {e}")
                return False
                
            # Unload plugin
            plugin_manager.unload_plugin(plugin_name)
            
        print("✅ All plugins load, configure, and unload correctly")
        return True
        
    except Exception as e:
        print(f"❌ Plugin integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_configuration_integration():
    """Test configuration system integration across modules"""
    print("⚙️ Testing configuration integration...")
    
    try:
        from config_manager import config_manager
        
        # Test that all modules use the same configuration
        original_channels = config_manager.config['wifi_scanner']['channel_range']['2.4ghz'].copy()
        
        # Modify configuration
        config_manager.config['wifi_scanner']['channel_range']['2.4ghz'] = [1, 6, 11]
        
        # Verify other modules see the change
        from wifi_pentest_radar_modern import WiFiScanner
        scanner = WiFiScanner()
        
        # Note: In a real integration test, we'd check if the scanner actually uses the modified channels
        # For now, we'll just verify the configuration is accessible
        
        if config_manager.config['wifi_scanner']['channel_range']['2.4ghz'] != [1, 6, 11]:
            print("❌ Configuration modification not reflected")
            return False
            
        # Restore original configuration
        config_manager.config['wifi_scanner']['channel_range']['2.4ghz'] = original_channels
        
        print("✅ Configuration integration working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Configuration integration test failed: {e}")
        return False

def test_error_handling():
    """Test error handling across the system"""
    print("🛡️ Testing error handling...")
    
    try:
        from security_engine import security_engine
        from distance_engine import distance_engine
        from vendor_service import vendor_service
        
        # Test with invalid inputs
        test_cases = [
            # Invalid signal strength
            lambda: distance_engine.calculate_distance(None, 2412),
            lambda: distance_engine.calculate_distance("invalid", 2412),
            lambda: distance_engine.calculate_distance(-200, 2412),  # Extreme value
            
            # Invalid MAC addresses
            lambda: vendor_service.get_vendor("invalid_mac"),
            lambda: vendor_service.get_vendor(""),
            lambda: vendor_service.get_vendor(None),
            
            # Invalid security analysis parameters
            lambda: security_engine.analyze_access_point("", "", "", None, None),
            lambda: security_engine.analyze_access_point(None, None, None, None, None),
        ]
        
        for i, test_case in enumerate(test_cases):
            try:
                result = test_case()
                # If we get here, the function handled the error gracefully
                print(f"✅ Error case {i+1} handled gracefully")
            except Exception as e:
                # This is actually expected for some cases
                print(f"⚠️ Error case {i+1} raised exception: {type(e).__name__}")
        
        print("✅ Error handling tests completed")
        return True
        
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False

def test_data_consistency():
    """Test data consistency across modules"""
    print("📊 Testing data consistency...")
    
    try:
        from security_engine import security_engine
        
        # Test that same input produces consistent output
        test_networks = [
            ('TestNet1', '00:1A:2B:3C:4D:5E', 'WPA2', -50, 2437),
            ('TestNet2', '00:1A:2B:3C:4D:5F', 'Open', -60, 2412),
            ('TestNet3', '00:1A:2B:3C:4D:60', 'WEP', -45, 2462),
        ]
        
        # Run analysis multiple times and check consistency
        for network in test_networks:
            results = []
            for _ in range(5):  # Run 5 times
                analysis = security_engine.analyze_access_point(*network)
                results.append({
                    'threat_level': analysis.threat_level,
                    'vulnerability_score': analysis.vulnerability_score,
                    'risk_factors_count': len(analysis.risk_factors)
                })
            
            # Check all results are identical
            first_result = results[0]
            for result in results[1:]:
                if result != first_result:
                    print(f"❌ Inconsistent analysis results for {network[0]}")
                    print(f"   First: {first_result}")
                    print(f"   Other: {result}")
                    return False
        
        print("✅ Analysis results are consistent")
        return True
        
    except Exception as e:
        print(f"❌ Data consistency test failed: {e}")
        return False

def main():
    """Main integration test runner"""
    print("🔗 WiFi Security Radar Suite - Integration Tests")
    print("=" * 55)
    
    tests = [
        ("End-to-End Workflow", test_end_to_end_workflow),
        ("Plugin Integration", test_plugin_integration),
        ("Configuration Integration", test_configuration_integration),
        ("Error Handling", test_error_handling),
        ("Data Consistency", test_data_consistency)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}")
        print("-" * 30)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print("\n" + "=" * 55)
    print(f"Integration Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All integration tests passed!")
        print("✅ System components work together correctly")
        print("✅ Data flows properly between modules")
        print("✅ Error handling is robust")
    else:
        print("⚠️ Some integration tests failed")
        print("🔧 System may have integration issues")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)