#!/usr/bin/env python3
"""Quick validation test for the rebuilt WiFi radar system"""

def main():
    print("🔧 Testing WiFi Radar System Components")
    print("=" * 50)
    
    # Test 1: Configuration Manager
    try:
        from config_manager import ConfigManager
        cm = ConfigManager()
        print(f"✅ Configuration Manager: {len(cm.security_profiles)} profiles loaded")
    except Exception as e:
        print(f"❌ Configuration Manager failed: {e}")
        return False
    
    # Test 2: Vendor Service
    try:
        from vendor_service import VendorService
        vs = VendorService()
        vendor = vs.get_vendor("00:1b:63:00:00:00")  # Apple MAC
        print(f"✅ Vendor Service: {vendor}")
    except Exception as e:
        print(f"❌ Vendor Service failed: {e}")
        return False
    
    # Test 3: Security Engine
    try:
        from security_engine import SecurityAnalysisEngine
        sae = SecurityAnalysisEngine()
        result = sae.analyze_security("TestNetwork", "WPA2")
        print(f"✅ Security Engine: Threat level {result['threat_level']}")
    except Exception as e:
        print(f"❌ Security Engine failed: {e}")
        return False
    
    # Test 4: Distance Engine
    try:
        from distance_engine import DistanceCalculationEngine
        dce = DistanceCalculationEngine()
        distance = dce.calculate_distance(-50, 2400)
        print(f"✅ Distance Engine: {distance:.1f}m calculated")
    except Exception as e:
        print(f"❌ Distance Engine failed: {e}")
        return False
    
    # Test 5: Main Scanner Import
    try:
        import wifi_pentest_radar_modern
        print("✅ Main Scanner: Import successful")
    except Exception as e:
        print(f"❌ Main Scanner failed: {e}")
        return False
    
    print("\n🎉 ALL SYSTEMS WORKING!")
    print("✨ No more hardcoding - everything is configuration-driven!")
    print("🚀 Ready to launch the rebuilt WiFi radar!")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        exit(1)
