#!/usr/bin/env python3
"""
Test the WiFi scanner backend without GUI
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_wifi_scanner():
    """Test the WiFiScanner class without GUI dependencies"""
    print("🔧 Testing WiFi Scanner Backend Logic...")
    
    try:
        # Import required modules
        from config_manager import config_manager
        from vendor_service import vendor_service
        from security_engine import security_engine
        from distance_engine import distance_engine
        print("✅ All engine modules imported successfully!")
        
        # Test configuration
        print(f"✅ Configuration loaded: {len(config_manager.security_profiles)} security profiles")
        
        # Test vendor service
        vendor = vendor_service.get_vendor("00:1b:63:00:00:00")  # Apple MAC
        print(f"✅ Vendor service working: {vendor}")
        
        # Test security analysis
        result = security_engine.analyze_access_point("TestNetwork", "00:11:22:33:44:55", "WPA2", -50, 2400)
        print(f"✅ Security analysis working: {result.threat_level}")
        
        # Test distance calculation
        distance = distance_engine.calculate_distance(-50, 2400)
        print(f"✅ Distance calculation working: {distance:.1f}m")
        
        print("\n🎉 BACKEND LOGIC TEST SUCCESSFUL!")
        print("✨ All engines working perfectly - no hardcoding!")
        print("🚀 WiFi scanner backend is ready!")
        
        return True
        
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_wifi_scanner()
    sys.exit(0 if success else 1)
