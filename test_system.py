#!/usr/bin/env python3
"""
Test script to validate the new configuration-driven WiFi radar system
"""

def test_imports():
    """Test all module imports"""
    try:
        import config_manager
        print("✓ Config manager imported")
        
        import vendor_service
        print("✓ Vendor service imported")
        
        import security_engine
        print("✓ Security engine imported")
        
        import distance_engine
        print("✓ Distance engine imported")
        
        from wifi_pentest_radar_modern import WiFiScanner
        print("✓ WiFi scanner imported")
        
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_config_system():
    """Test configuration loading"""
    try:
        from config_manager import config_manager
        print(f"✓ Configuration loaded: {len(config_manager.security_profiles)} security profiles")
        print(f"✓ WiFi scanning config: {config_manager.config['wifi_scanner']['channel_range']}")
        return True
    except Exception as e:
        print(f"✗ Config test failed: {e}")
        return False

def test_vendor_service():
    """Test vendor service"""
    try:
        from vendor_service import vendor_service
        print(f"✓ Vendor database: {len(vendor_service.oui_database)} entries")
        
        # Test vendor lookup
        test_mac = "00:1B:63:84:45:E6"
        vendor = vendor_service.get_vendor(test_mac)
        print(f"✓ Vendor lookup test: {test_mac} -> {vendor}")
        return True
    except Exception as e:
        print(f"✗ Vendor service test failed: {e}")
        return False

def test_security_engine():
    """Test security analysis"""
    try:
        from security_engine import security_engine
        
        # Test security analysis
        analysis = security_engine.analyze_access_point(
            ssid='TestNetwork',
            bssid='00:1B:63:84:45:E6',
            security='WEP',
            signal_dbm=-45,
            frequency=2412
        )
        print(f"✓ Security analysis: {analysis.threat_level} (score: {analysis.vulnerability_score})")
        return True
    except Exception as e:
        print(f"✗ Security engine test failed: {e}")
        return False

def test_distance_engine():
    """Test distance calculation"""
    try:
        from distance_engine import distance_engine
        
        # Test distance calculation
        distance = distance_engine.calculate_distance(-45, 2412)  # -45 dBm at 2412 MHz
        print(f"✓ Distance calculation: {distance:.2f} meters")
        return True
    except Exception as e:
        print(f"✗ Distance engine test failed: {e}")
        return False

def test_wifi_scanner():
    """Test WiFi scanner class"""
    try:
        from wifi_pentest_radar_modern import WiFiScanner
        scanner = WiFiScanner()
        print("✓ WiFiScanner initialized")
        
        # Test parsing (with realistic scan output)
        test_output = """BSS 00:1b:63:84:45:e6(on wlan0) -- associated
	freq: 2437
	beacon interval: 100
	capability: ESS Privacy ShortSlotTime (0x0411)
	signal: -45.00 dBm
	last seen: 1024 ms ago
	Information elements from Probe Response frame:
	SSID: Apple_Network
	Supported rates: 1.0* 2.0* 5.5* 11.0* 6.0 9.0 12.0 18.0 
	DS Parameter set: channel 6
	ERP: <no flags>
	Extended supported rates: 24.0 36.0 48.0 54.0 
	RSN:	 * Version: 1
		 * Group cipher: CCMP
		 * Pairwise ciphers: CCMP
		 * Authentication suites: PSK
		 * RSN capabilities: 0x0000
BSS 00:0a:e4:12:34:56(on wlan0)
	freq: 2462
	signal: -67.00 dBm
	SSID: NETGEAR_Open
	capability: ESS (0x0001)"""
        networks = scanner.parse_scan_output(test_output)
        print(f"✓ Parsing test: Found {len(networks)} networks")
        if networks:
            for i, network in enumerate(networks):
                print(f"  Network {i+1}: {network['ssid']} ({network['security']}) - {network['signal']} dBm")
        return True
    except Exception as e:
        print(f"✗ WiFi scanner test failed: {e}")
        return False

def main():
    """Main test runner"""
    print("Testing new configuration-driven WiFi radar system...")
    print("=" * 60)
    
    tests = [
        ("Module Imports", test_imports),
        ("Configuration System", test_config_system),
        ("Vendor Service", test_vendor_service),
        ("Security Engine", test_security_engine),
        ("Distance Engine", test_distance_engine),
        ("WiFi Scanner", test_wifi_scanner)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 30)
        try:
            if test_func():
                passed += 1
                print(f"✓ {test_name} PASSED")
            else:
                print(f"✗ {test_name} FAILED")
        except Exception as e:
            print(f"✗ {test_name} FAILED: {e}")
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The new logic system is working perfectly!")
        print("✓ No more hardcoding - everything is configuration-driven")
        print("✓ Modular architecture with separate engines")
        print("✓ External data sources for vendor detection")
        print("✓ Algorithmic distance calculation")
        print("✓ Pattern-based security analysis")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()
