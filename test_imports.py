#!/usr/bin/env python3
"""Simple test script to verify engine imports"""

print("🔧 Testing WiFi Radar Engine Imports...")

try:
    from config_manager import config_manager
    print("✅ config_manager imported")
except Exception as e:
    print(f"❌ config_manager failed: {e}")
    exit(1)

try:
    from vendor_service import vendor_service
    print("✅ vendor_service imported")
except Exception as e:
    print(f"❌ vendor_service failed: {e}")
    exit(1)

try:
    from security_engine import security_engine
    print("✅ security_engine imported")
except Exception as e:
    print(f"❌ security_engine failed: {e}")
    exit(1)

try:
    from distance_engine import distance_engine
    print("✅ distance_engine imported")
except Exception as e:
    print(f"❌ distance_engine failed: {e}")
    exit(1)

print("🎉 ALL IMPORTS SUCCESSFUL!")
print("✨ Ready to run the WiFi radar!")
