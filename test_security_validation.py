#!/usr/bin/env python3
"""
Security Validation Tests for WiFi Security Radar Suite
=======================================================

Tests security-related functionality and validates security assessments.
"""

import sys
import os

def test_security_engine_accuracy():
    """Test security engine assessment accuracy"""
    print("🔒 Testing security engine accuracy...")
    
    try:
        from security_engine import security_engine
        
        # Test cases with expected threat levels
        test_cases = [
            # (ssid, bssid, security, signal, frequency, expected_threat_level)
            ('Open_Network', '00:1A:2B:3C:4D:5E', 'Open', -50, 2412, ['CRITICAL', 'HIGH']),
            ('WEP_Network', '00:1A:2B:3C:4D:5F', 'WEP', -45, 2437, ['CRITICAL']),
            ('WPA_Network', '00:1A:2B:3C:4D:60', 'WPA', -55, 2462, ['HIGH', 'MEDIUM']),
            ('WPA2_Network', '00:1A:2B:3C:4D:61', 'WPA2', -60, 5180, ['MEDIUM', 'LOW']),
            ('WPA3_Network', '00:1A:2B:3C:4D:62', 'WPA3', -65, 5200, ['LOW', 'MINIMAL']),
            ('Enterprise_Network', '00:1A:2B:3C:4D:63', 'WPA2-Enterprise', -70, 5220, ['LOW', 'MINIMAL']),
        ]
        
        correct_assessments = 0
        total_assessments = len(test_cases)
        
        for ssid, bssid, security, signal, frequency, expected_levels in test_cases:
            analysis = security_engine.analyze_access_point(ssid, bssid, security, signal, frequency)
            
            if analysis.threat_level in expected_levels:
                print(f"✅ {ssid} ({security}): {analysis.threat_level} - Correct")
                correct_assessments += 1
            else:
                print(f"❌ {ssid} ({security}): Expected {expected_levels}, got {analysis.threat_level}")
        
        accuracy = correct_assessments / total_assessments * 100
        print(f"🎯 Security assessment accuracy: {accuracy:.1f}% ({correct_assessments}/{total_assessments})")
        
        return accuracy >= 80  # Require at least 80% accuracy
        
    except Exception as e:
        print(f"❌ Security engine accuracy test failed: {e}")
        return False

def test_vulnerability_detection():
    """Test vulnerability detection capabilities"""
    print("🔍 Testing vulnerability detection...")
    
    try:
        from security_engine import security_engine
        
        # Test specific vulnerability scenarios
        scenarios = [
            {
                'name': 'Open Network',
                'params': ('OpenWiFi', '00:1A:2B:3C:4D:5E', 'Open', -40, 2412),
                'expected_vulnerabilities': ['Security type: Open']
            },
            {
                'name': 'WEP Network',
                'params': ('OldNetwork', '00:1A:2B:3C:4D:5F', 'WEP', -45, 2437),
                'expected_vulnerabilities': ['Security type: WEP']
            },
            {
                'name': 'Default SSID',
                'params': ('NETGEAR', '00:1A:2B:3C:4D:60', 'WPA2', -50, 2462),
                'expected_vulnerabilities': ['Default/common SSID', 'NETGEAR']
            }
        ]
        
        vulnerabilities_found = 0
        total_scenarios = len(scenarios)
        
        for scenario in scenarios:
            analysis = security_engine.analyze_access_point(*scenario['params'])
            
            # Check if any expected vulnerability is detected
            found_expected = False
            for expected_vuln in scenario['expected_vulnerabilities']:
                for detected_vuln in analysis.risk_factors:
                    if expected_vuln.lower() in detected_vuln.lower():
                        found_expected = True
                        break
                if found_expected:
                    break
            
            if found_expected:
                print(f"✅ {scenario['name']}: Vulnerability detected correctly")
                vulnerabilities_found += 1
            else:
                print(f"❌ {scenario['name']}: Expected vulnerability not detected")
                print(f"   Expected: {scenario['expected_vulnerabilities']}")
                print(f"   Detected: {analysis.risk_factors}")
        
        detection_rate = vulnerabilities_found / total_scenarios * 100
        print(f"🎯 Vulnerability detection rate: {detection_rate:.1f}% ({vulnerabilities_found}/{total_scenarios})")
        
        return detection_rate >= 75  # Require at least 75% detection rate
        
    except Exception as e:
        print(f"❌ Vulnerability detection test failed: {e}")
        return False

def test_attack_vector_identification():
    """Test attack vector identification"""
    print("⚔️ Testing attack vector identification...")
    
    try:
        from security_engine import security_engine
        
        # Test networks with known attack vectors
        attack_scenarios = [
            {
                'name': 'Open Network Attack Vectors',
                'params': ('FreeWiFi', '00:1A:2B:3C:4D:5E', 'Open', -35, 2412),
                'expected_attacks': ['Evil Twin', 'Man-in-the-Middle', 'Packet Sniffing']
            },
            {
                'name': 'WEP Network Attack Vectors',
                'params': ('LegacyNet', '00:1A:2B:3C:4D:5F', 'WEP', -40, 2437),
                'expected_attacks': ['WEP Cracking', 'Aircrack']
            },
            {
                'name': 'WPS Enabled Attack Vectors',
                'params': ('HomeRouter', '00:1A:2B:3C:4D:60', 'WPA2+WPS', -45, 2462),
                'expected_attacks': ['WPS PIN', 'Reaver', 'Pixie Dust']
            }
        ]
        
        vectors_found = 0
        total_scenarios = len(attack_scenarios)
        
        for scenario in attack_scenarios:
            analysis = security_engine.analyze_access_point(*scenario['params'])
            
            # Check if attack vectors are identified
            found_vectors = 0
            for expected_attack in scenario['expected_attacks']:
                for detected_attack in analysis.attack_vectors:
                    if expected_attack.lower() in detected_attack.lower():
                        found_vectors += 1
                        break
            
            if found_vectors > 0:
                print(f"✅ {scenario['name']}: {found_vectors}/{len(scenario['expected_attacks'])} attack vectors identified")
                vectors_found += 1
            else:
                print(f"❌ {scenario['name']}: No expected attack vectors identified")
                print(f"   Expected: {scenario['expected_attacks']}")
                print(f"   Detected: {analysis.attack_vectors}")
        
        identification_rate = vectors_found / total_scenarios * 100
        print(f"🎯 Attack vector identification rate: {identification_rate:.1f}% ({vectors_found}/{total_scenarios})")
        
        return identification_rate >= 70  # Require at least 70% identification rate
        
    except Exception as e:
        print(f"❌ Attack vector identification test failed: {e}")
        return False

def test_security_scoring():
    """Test security scoring system"""
    print("📊 Testing security scoring system...")
    
    try:
        from security_engine import security_engine
        
        # Test networks with expected score ranges
        scoring_tests = [
            {
                'name': 'Secure WPA3 Network',
                'params': ('SecureCorpNet', '00:1A:2B:3C:4D:5E', 'WPA3', -70, 5180),
                'expected_range': (0, 30)  # Low vulnerability score (0-30)
            },
            {
                'name': 'Standard WPA2 Network',
                'params': ('HomeNetwork', '00:1A:2B:3C:4D:5F', 'WPA2', -55, 2437),
                'expected_range': (20, 60)  # Medium vulnerability score
            },
            {
                'name': 'Vulnerable WEP Network',
                'params': ('OldRouter', '00:1A:2B:3C:4D:60', 'WEP', -40, 2412),
                'expected_range': (70, 100)  # High vulnerability score
            },
            {
                'name': 'Critical Open Network',
                'params': ('PublicWiFi', '00:1A:2B:3C:4D:61', 'Open', -30, 2462),
                'expected_range': (80, 100)  # Very high vulnerability score
            }
        ]
        
        correct_scores = 0
        total_tests = len(scoring_tests)
        
        for test in scoring_tests:
            analysis = security_engine.analyze_access_point(*test['params'])
            score = analysis.vulnerability_score
            min_score, max_score = test['expected_range']
            
            if min_score <= score <= max_score:
                print(f"✅ {test['name']}: Score {score} (expected {min_score}-{max_score})")
                correct_scores += 1
            else:
                print(f"❌ {test['name']}: Score {score} (expected {min_score}-{max_score})")
        
        scoring_accuracy = correct_scores / total_tests * 100
        print(f"🎯 Security scoring accuracy: {scoring_accuracy:.1f}% ({correct_scores}/{total_tests})")
        
        return scoring_accuracy >= 75  # Require at least 75% scoring accuracy
        
    except Exception as e:
        print(f"❌ Security scoring test failed: {e}")
        return False

def test_threat_level_consistency():
    """Test threat level consistency with vulnerability scores"""
    print("⚖️ Testing threat level consistency...")
    
    try:
        from security_engine import security_engine
        
        # Test that threat levels align with vulnerability scores
        test_networks = [
            ('TestNet1', '00:1A:2B:3C:4D:5E', 'Open', -40, 2412),
            ('TestNet2', '00:1A:2B:3C:4D:5F', 'WEP', -45, 2437),
            ('TestNet3', '00:1A:2B:3C:4D:60', 'WPA', -50, 2462),
            ('TestNet4', '00:1A:2B:3C:4D:61', 'WPA2', -55, 5180),
            ('TestNet5', '00:1A:2B:3C:4D:62', 'WPA3', -60, 5200),
        ]
        
        consistent_results = 0
        total_networks = len(test_networks)
        
        for network in test_networks:
            analysis = security_engine.analyze_access_point(*network)
            score = analysis.vulnerability_score
            threat_level = analysis.threat_level
            
            # Check consistency between score and threat level
            is_consistent = False
            
            if threat_level == 'LOW' and score <= 40:
                is_consistent = True
            elif threat_level == 'MEDIUM' and 30 <= score <= 70:
                is_consistent = True
            elif threat_level == 'HIGH' and 60 <= score <= 90:
                is_consistent = True
            elif threat_level == 'CRITICAL' and score >= 80:
                is_consistent = True
            
            if is_consistent:
                print(f"✅ {network[0]}: {threat_level} level consistent with score {score}")
                consistent_results += 1
            else:
                print(f"❌ {network[0]}: {threat_level} level inconsistent with score {score}")
        
        consistency_rate = consistent_results / total_networks * 100
        print(f"🎯 Threat level consistency: {consistency_rate:.1f}% ({consistent_results}/{total_networks})")
        
        return consistency_rate >= 80  # Require at least 80% consistency
        
    except Exception as e:
        print(f"❌ Threat level consistency test failed: {e}")
        return False

def test_security_recommendations():
    """Test security recommendations"""
    print("💡 Testing security recommendations...")
    
    try:
        from security_engine import security_engine
        
        # Test networks that should generate specific recommendations
        recommendation_tests = [
            {
                'name': 'Open Network',
                'params': ('CafeWiFi', '00:1A:2B:3C:4D:5E', 'Open', -40, 2412),
                'expected_keywords': ['encryption', 'WPA', 'secure']
            },
            {
                'name': 'WEP Network',
                'params': ('OldNetwork', '00:1A:2B:3C:4D:5F', 'WEP', -45, 2437),
                'expected_keywords': ['upgrade', 'WPA2', 'WPA3']
            },
            {
                'name': 'Default SSID',
                'params': ('NETGEAR45', '00:1A:2B:3C:4D:60', 'WPA2', -50, 2462),
                'expected_keywords': ['SSID', 'name', 'change']
            }
        ]
        
        good_recommendations = 0
        total_tests = len(recommendation_tests)
        
        for test in recommendation_tests:
            analysis = security_engine.analyze_access_point(*test['params'])
            
            # Check if recommendations contain expected keywords
            recommendations_text = ' '.join(analysis.recommendations).lower()
            
            found_keywords = 0
            for keyword in test['expected_keywords']:
                if keyword.lower() in recommendations_text:
                    found_keywords += 1
            
            if found_keywords > 0:
                print(f"✅ {test['name']}: Found {found_keywords}/{len(test['expected_keywords'])} relevant recommendations")
                good_recommendations += 1
            else:
                print(f"❌ {test['name']}: No relevant recommendations found")
                print(f"   Expected keywords: {test['expected_keywords']}")
                print(f"   Recommendations: {analysis.recommendations}")
        
        recommendation_quality = good_recommendations / total_tests * 100
        print(f"🎯 Recommendation quality: {recommendation_quality:.1f}% ({good_recommendations}/{total_tests})")
        
        return recommendation_quality >= 70  # Require at least 70% quality
        
    except Exception as e:
        print(f"❌ Security recommendations test failed: {e}")
        return False

def main():
    """Main security validation test runner"""
    print("🔒 WiFi Security Radar Suite - Security Validation Tests")
    print("=" * 65)
    
    tests = [
        ("Security Engine Accuracy", test_security_engine_accuracy),
        ("Vulnerability Detection", test_vulnerability_detection),
        ("Attack Vector Identification", test_attack_vector_identification),
        ("Security Scoring", test_security_scoring),
        ("Threat Level Consistency", test_threat_level_consistency),
        ("Security Recommendations", test_security_recommendations)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}")
        print("-" * 40)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 65)
    print(f"Security Validation Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All security validation tests passed!")
        print("✅ Security engine provides accurate assessments")
        print("✅ Vulnerability detection is working correctly")
        print("✅ Attack vector identification is functional")
        print("✅ Security scoring is consistent and accurate")
    else:
        print("⚠️ Some security validation tests failed")
        print("🔧 Security assessment accuracy may be compromised")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)