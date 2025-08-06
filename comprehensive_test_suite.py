#!/usr/bin/env python3
"""
Comprehensive Test Suite for WiFi Security Radar Suite v5.0
============================================================

This test suite provides comprehensive testing coverage for all components
of the WiFi Security Radar Suite, including:
- Core functionality testing
- Plugin system validation  
- GUI component testing (non-display mode)
- Integration testing
- Performance benchmarking
- Security validation

Usage:
    python3 comprehensive_test_suite.py [--verbose] [--category CATEGORY] [--no-performance]
"""

import sys
import os
import time
import traceback
import json
from pathlib import Path
from datetime import datetime
import argparse

# Test categories and modules
TEST_MODULES = {
    'core': ['quick_test', 'test_system'],
    'features': ['test_core_features'],
    'plugins': ['test_plugin_system'],
    'integration': ['test_launcher_functionality', 'test_integration'],
    'security': ['test_security_validation'],
    'gui': ['test_gui_non_display'],
    'imports': ['test_imports'],
    'backend': ['test_backend']
}

class TestResult:
    """Class to track test results"""
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.passed = False
        self.error = None
        self.output = ""
        self.duration = 0
        self.timestamp = datetime.now()

class ComprehensiveTestRunner:
    """Main test runner for the comprehensive test suite"""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.results = []
        self.start_time = time.time()
        
    def log(self, message, level="INFO"):
        """Log a message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        if level == "ERROR":
            icon = "❌"
        elif level == "WARN":
            icon = "⚠️"
        elif level == "SUCCESS":
            icon = "✅"
        else:
            icon = "ℹ️"
        print(f"[{timestamp}] {icon} {message}")
        
    def run_single_test(self, test_name, category):
        """Run a single test module"""
        result = TestResult(test_name, category)
        start_time = time.time()
        
        self.log(f"Running {test_name} ({category})")
        
        try:
            # Import and run the test module
            if os.path.exists(f"{test_name}.py"):
                # Capture output
                import subprocess
                process = subprocess.run(
                    [sys.executable, f"{test_name}.py"], 
                    capture_output=True, 
                    text=True,
                    timeout=120  # 2 minute timeout per test
                )
                
                result.output = process.stdout + process.stderr
                result.passed = process.returncode == 0
                
                if not result.passed:
                    result.error = f"Exit code: {process.returncode}"
                    if process.stderr:
                        result.error += f"\nSTDERR: {process.stderr}"
                        
            else:
                result.error = f"Test file {test_name}.py not found"
                result.passed = False
                
        except subprocess.TimeoutExpired:
            result.error = "Test timed out after 120 seconds"
            result.passed = False
        except Exception as e:
            result.error = str(e)
            result.passed = False
            
        result.duration = time.time() - start_time
        return result
        
    def run_category_tests(self, category):
        """Run all tests in a category"""
        if category not in TEST_MODULES:
            self.log(f"Unknown test category: {category}", "ERROR")
            return []
            
        results = []
        test_modules = TEST_MODULES[category]
        
        self.log(f"Running {category.upper()} tests ({len(test_modules)} modules)")
        print("=" * 60)
        
        for test_module in test_modules:
            result = self.run_single_test(test_module, category)
            results.append(result)
            
            if result.passed:
                self.log(f"{test_module} PASSED ({result.duration:.2f}s)", "SUCCESS")
            else:
                self.log(f"{test_module} FAILED: {result.error}", "ERROR")
                
            if self.verbose and result.output:
                print(f"--- Output from {test_module} ---")
                print(result.output)
                print("--- End Output ---\n")
                
        return results
        
    def run_performance_tests(self):
        """Run performance benchmarks"""
        self.log("Running performance benchmarks")
        performance_results = []
        
        # Test 1: Import speed
        start_time = time.time()
        try:
            import config_manager
            import vendor_service  
            import security_engine
            import distance_engine
            from wifi_pentest_radar_modern import WiFiScanner
            import_time = time.time() - start_time
            performance_results.append(("Module Import Speed", import_time, "seconds"))
            self.log(f"Module imports completed in {import_time:.3f} seconds", "SUCCESS")
        except Exception as e:
            performance_results.append(("Module Import Speed", -1, f"FAILED: {e}"))
            
        # Test 2: Configuration loading speed
        start_time = time.time()
        try:
            from config_manager import config_manager
            config_time = time.time() - start_time
            performance_results.append(("Configuration Loading", config_time, "seconds"))
            self.log(f"Configuration loaded in {config_time:.3f} seconds", "SUCCESS")
        except Exception as e:
            performance_results.append(("Configuration Loading", -1, f"FAILED: {e}"))
            
        # Test 3: Security analysis performance
        start_time = time.time()
        try:
            from security_engine import security_engine
            # Run 100 security analyses
            for i in range(100):
                analysis = security_engine.analyze_access_point(
                    f'TestNetwork_{i}', 
                    f'00:1B:63:84:45:{i:02X}', 
                    'WPA2' if i % 2 else 'Open',
                    -50 - (i % 30),
                    2412 + (i % 12) * 5
                )
            analysis_time = time.time() - start_time
            avg_time = analysis_time / 100
            performance_results.append(("Security Analysis (100x)", analysis_time, "seconds"))
            performance_results.append(("Security Analysis (avg)", avg_time, "seconds"))
            self.log(f"100 security analyses completed in {analysis_time:.3f}s (avg: {avg_time:.4f}s)", "SUCCESS")
        except Exception as e:
            performance_results.append(("Security Analysis", -1, f"FAILED: {e}"))
            
        return performance_results
        
    def generate_report(self, all_results, performance_results=None):
        """Generate comprehensive test report"""
        total_tests = len(all_results)
        passed_tests = sum(1 for r in all_results if r.passed)
        total_time = time.time() - self.start_time
        
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE TEST SUITE REPORT")
        print("=" * 80)
        print(f"🕐 Execution Time: {total_time:.2f} seconds")
        print(f"📈 Test Results: {passed_tests}/{total_tests} tests passed ({passed_tests/total_tests*100:.1f}%)")
        print(f"📅 Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Category breakdown
        print("\n📋 Results by Category:")
        print("-" * 40)
        categories = {}
        for result in all_results:
            if result.category not in categories:
                categories[result.category] = {'passed': 0, 'total': 0}
            categories[result.category]['total'] += 1
            if result.passed:
                categories[result.category]['passed'] += 1
                
        for category, stats in categories.items():
            percentage = stats['passed'] / stats['total'] * 100
            status = "✅" if percentage == 100 else "⚠️" if percentage >= 50 else "❌"
            print(f"  {status} {category.upper()}: {stats['passed']}/{stats['total']} ({percentage:.1f}%)")
            
        # Failed tests details
        failed_tests = [r for r in all_results if not r.passed]
        if failed_tests:
            print("\n❌ Failed Tests:")
            print("-" * 40)
            for result in failed_tests:
                print(f"  • {result.name} ({result.category}): {result.error}")
                
        # Performance results
        if performance_results:
            print("\n⚡ Performance Benchmarks:")
            print("-" * 40)
            for test_name, value, unit in performance_results:
                if isinstance(value, (int, float)) and value >= 0:
                    print(f"  • {test_name}: {value:.4f} {unit}")
                else:
                    print(f"  • {test_name}: {unit}")
                    
        # System information
        print("\n🖥️ System Information:")
        print("-" * 40)
        print(f"  • Python Version: {sys.version.split()[0]}")
        print(f"  • Platform: {sys.platform}")
        print(f"  • Working Directory: {os.getcwd()}")
        
        # Save report to file
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'execution_time': total_time,
            'categories': categories,
            'failed_tests': [{'name': r.name, 'category': r.category, 'error': r.error} for r in failed_tests],
            'performance': performance_results or [],
            'system_info': {
                'python_version': sys.version.split()[0],
                'platform': sys.platform,
                'working_directory': os.getcwd()
            }
        }
        
        with open('test_report.json', 'w') as f:
            json.dump(report_data, f, indent=2)
        self.log("Test report saved to test_report.json", "SUCCESS")
        
        # Overall status
        if passed_tests == total_tests:
            print("\n🎉 ALL TESTS PASSED! The WiFi Security Radar Suite is working perfectly!")
        elif passed_tests / total_tests >= 0.8:
            print(f"\n⚠️ Most tests passed ({passed_tests}/{total_tests}). Some features may have issues.")
        else:
            print(f"\n❌ Many tests failed ({passed_tests}/{total_tests}). Please investigate issues.")
            
        return passed_tests == total_tests

def main():
    """Main test runner"""
    parser = argparse.ArgumentParser(description='WiFi Security Radar Suite - Comprehensive Test Suite')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed output from tests')
    parser.add_argument('--category', '-c', choices=list(TEST_MODULES.keys()) + ['all'], 
                       default='all', help='Run tests for specific category only')
    parser.add_argument('--no-performance', action='store_true', help='Skip performance benchmarks')
    
    args = parser.parse_args()
    
    print("🚀 WiFi Security Radar Suite - Comprehensive Test Suite")
    print("=" * 60)
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔧 Configuration: verbose={args.verbose}, category={args.category}")
    print("=" * 60)
    
    runner = ComprehensiveTestRunner(verbose=args.verbose)
    all_results = []
    
    # Run tests by category
    if args.category == 'all':
        for category in TEST_MODULES.keys():
            results = runner.run_category_tests(category)
            all_results.extend(results)
            print()  # Add spacing between categories
    else:
        results = runner.run_category_tests(args.category)
        all_results.extend(results)
        
    # Run performance tests
    performance_results = None
    if not args.no_performance and args.category in ['all', 'core']:
        print("⚡ PERFORMANCE BENCHMARKS")
        print("=" * 60)
        performance_results = runner.run_performance_tests()
        
    # Generate final report
    success = runner.generate_report(all_results, performance_results)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()