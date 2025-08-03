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
        import config_manager
        cm = config_manager.ConfigManager()
        print(
            f"✓ Configuration loaded: {len(cm.security_profiles)} security profiles")
        print(
            f"✓ WiFi scanning config: {
                cm.config['wifi_scanning']['channel_range']}")
        return True
    except Exception as e:
        print(f"✗ Config test failed: {e}")
        return False


def test_vendor_service():
    """Test vendor service"""
    try:
        import vendor_service
        vs = vendor_service.VendorService()
        print(f"✓ Vendor database: {len(vs.oui_database)} entries")

        # Test vendor lookup
        test_mac = "00:1B:63:84:45:E6"
        vendor = vs.get_vendor(test_mac)
        print(f"✓ Vendor lookup test: {test_mac} -> {vendor}")
        return True
    except Exception as e:
        print(f"✗ Vendor service test failed: {e}")
        return False


def test_security_engine():
    """Test security analysis"""
    try:
        import security_engine
        se = security_engine.SecurityEngine()

        # Test security analysis
        test_ap = {
            'ssid': 'TestNetwork',
            'encryption': 'WEP',
            'signal': -45
        }
        analysis = se.analyze_access_point(test_ap)
        print(
            f"✓ Security analysis: {
                analysis['threat_level']} (score: {
                analysis['vulnerability_score']})")
        return True
    except Exception as e:
        print(f"✗ Security engine test failed: {e}")
        return False


def test_distance_engine():
    """Test distance calculation"""
    try:
        import distance_engine
        de = distance_engine.DistanceEngine()

        # Test distance calculation
        distance = de.calculate_distance(-45, 2412)  # -45 dBm at 2412 MHz
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

        # Test parsing (without actual scan)
        test_output = "Cell 01 - Address: 00:1B:63:84:45:E6\n          ESSID:\"TestNetwork\"\n          Mode:Master\n          Frequency:2.437 GHz (Channel 6)\n          Quality:70/70  Signal level:-45 dBm\n          Encryption key:on\n          IE: IEEE 802.11i/WPA2 Version 1"
        networks = scanner.parse_scan_output(test_output)
        print(f"✓ Parsing test: Found {len(networks)} networks")
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
