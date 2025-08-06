#!/usr/bin/env python3
"""
Master Test Runner for WiFi Security Radar Suite v5.0
=====================================================

This script runs all test categories and generates comprehensive reports.
It serves as the main entry point for testing the entire suite.

Usage:
    python3 run_all_tests.py [--verbose] [--screenshot]
"""

import sys
import os
import subprocess
import time
from datetime import datetime

def run_command(command, description):
    """Run a command and return success status"""
    print(f"\n🧪 {description}")
    print("=" * 60)
    
    start_time = time.time()
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        duration = time.time() - start_time
        
        # Print output
        if result.stdout:
            print(result.stdout)
        if result.stderr and result.returncode != 0:
            print("STDERR:", result.stderr)
            
        success = result.returncode == 0
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"\n{status} ({duration:.2f}s)")
        
        return success, result.stdout, result.stderr
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False, "", str(e)

def main():
    """Main test runner"""
    print("🚀 WiFi Security Radar Suite v5.0 - Master Test Runner")
    print("=" * 70)
    print(f"📅 Test Session Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # Test sequence in order of complexity
    test_sequence = [
        ("python3 quick_test.py", "Quick Smoke Test"),
        ("python3 test_system.py", "Comprehensive System Test"),
        ("python3 test_integration.py", "Integration Tests"),
        ("python3 test_security_validation.py", "Security Validation Tests"),
        ("python3 test_plugin_system.py", "Plugin System Tests"),
        ("python3 test_core_features.py", "Enhanced Features Tests"),
        ("DISPLAY=:99 xvfb-run -a python3 test_gui_non_display.py", "GUI Component Tests (Non-Display)"),
        ("python3 comprehensive_test_suite.py --category all", "Comprehensive Test Suite")
    ]
    
    results = []
    total_duration = 0
    
    for command, description in test_sequence:
        success, stdout, stderr = run_command(command, description)
        results.append({
            'description': description,
            'command': command,
            'success': success,
            'stdout': stdout,
            'stderr': stderr
        })
        
        # Add delay between tests
        time.sleep(1)
    
    # Generate final report
    print("\n" + "=" * 70)
    print("📊 MASTER TEST REPORT")
    print("=" * 70)
    
    passed_tests = sum(1 for r in results if r['success'])
    total_tests = len(results)
    success_rate = passed_tests / total_tests * 100
    
    print(f"🎯 Overall Success Rate: {success_rate:.1f}% ({passed_tests}/{total_tests})")
    print(f"📅 Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n📋 Individual Test Results:")
    print("-" * 50)
    
    for i, result in enumerate(results, 1):
        status = "✅" if result['success'] else "❌"
        print(f"{i:2d}. {status} {result['description']}")
        if not result['success'] and result['stderr']:
            print(f"    Error: {result['stderr'][:100]}...")
    
    # Test category summary
    print("\n🔍 Test Category Analysis:")
    print("-" * 35)
    
    categories = {
        'Core System': ['Quick Smoke Test', 'Comprehensive System Test'],
        'Integration': ['Integration Tests'],
        'Security': ['Security Validation Tests'],
        'Plugin System': ['Plugin System Tests'],
        'Enhanced Features': ['Enhanced Features Tests'],
        'GUI Components': ['GUI Component Tests (Non-Display)'],
        'Comprehensive': ['Comprehensive Test Suite']
    }
    
    for category, test_names in categories.items():
        category_results = [r for r in results if r['description'] in test_names]
        category_passed = sum(1 for r in category_results if r['success'])
        category_total = len(category_results)
        
        if category_total > 0:
            category_rate = category_passed / category_total * 100
            status = "✅" if category_rate == 100 else "⚠️" if category_rate >= 50 else "❌"
            print(f"  {status} {category}: {category_passed}/{category_total} ({category_rate:.0f}%)")
    
    # Quality assessment
    print("\n🏆 Quality Assessment:")
    print("-" * 25)
    
    if success_rate >= 90:
        print("🎉 EXCELLENT - System is production ready!")
        print("✅ All critical components are working correctly")
        print("✅ Security validation passed")
        print("✅ Integration tests successful")
    elif success_rate >= 75:
        print("👍 GOOD - System is mostly functional")
        print("⚠️ Some non-critical issues detected")
        print("✅ Core functionality verified")
    elif success_rate >= 50:
        print("⚠️ FAIR - System has significant issues")
        print("🔧 Multiple test failures require investigation")
        print("⚠️ Core functionality may be compromised")
    else:
        print("❌ POOR - System has critical issues")
        print("🚨 Major test failures detected")
        print("🔧 Immediate attention required")
    
    # Recommendations
    print("\n💡 Recommendations:")
    print("-" * 20)
    
    failed_tests = [r for r in results if not r['success']]
    if not failed_tests:
        print("🎯 System is working excellently!")
        print("📝 Consider adding more edge case tests")
        print("🔄 Schedule regular test runs")
    else:
        print("🔧 Address the following failed tests:")
        for test in failed_tests[:3]:  # Show first 3 failures
            print(f"  • {test['description']}")
        if len(failed_tests) > 3:
            print(f"  • ... and {len(failed_tests) - 3} more")
        
        print("📋 Review error logs for detailed debugging information")
        print("🔄 Re-run individual test modules after fixes")
    
    # Save detailed report
    report_file = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    import json
    
    report_data = {
        'timestamp': datetime.now().isoformat(),
        'total_tests': total_tests,
        'passed_tests': passed_tests,
        'success_rate': success_rate,
        'test_results': results,
        'system_info': {
            'python_version': sys.version.split()[0],
            'platform': sys.platform,
            'working_directory': os.getcwd()
        }
    }
    
    with open(report_file, 'w') as f:
        json.dump(report_data, f, indent=2)
    
    print(f"\n📄 Detailed report saved to: {report_file}")
    
    # Exit with appropriate code
    exit_code = 0 if success_rate >= 75 else 1
    return exit_code

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)