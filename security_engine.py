#!/usr/bin/env python3
"""
Security Analysis Engine for WiFi Security Radar Suite
Analyzes WiFi security and calculates vulnerability scores
"""

import re
import logging
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass
from config_manager import config_manager

logger = logging.getLogger(__name__)

@dataclass
class SecurityAnalysisResult:
    """Result of security analysis"""
    vulnerability_score: int
    threat_level: str
    threat_color: str
    attack_vectors: List[str]
    risk_factors: List[str]
    recommendations: List[str]
    confidence: float

class SecurityAnalysisEngine:
    """Engine for analyzing WiFi security vulnerabilities"""
    
    def __init__(self):
        self.config = config_manager
        self._load_analysis_patterns()
    
    def _load_analysis_patterns(self):
        """Load patterns for SSID analysis"""
        self.ssid_patterns = {
            'default_names': [
                r'^(default|admin|router|root)$',
                r'^(linksys|netgear|dlink|tplink|asus)$',
                r'^(belkin|zyxel|huawei|motorola)$',
                r'^(wifi|wireless|internet|broadband)$'
            ],
            'weak_patterns': [
                r'^(test|temp|guest|public)$',
                r'^(password|123456|admin)$',
                r'(phone|mobile|iphone|android)',
                r'(personal|private|home)'
            ],
            'personal_info': [
                r'[0-9]{3,}',  # Phone numbers, addresses
                r'(family|house|apartment|apt)',
                r'(street|road|ave|avenue|blvd)',
                r'[a-zA-Z]+\s*[0-9]+[a-zA-Z]*'  # Address-like patterns
            ],
            'business_patterns': [
                r'(corp|company|business|office)',
                r'(hotel|restaurant|cafe|shop)',
                r'(school|university|college)',
                r'(hospital|clinic|medical)'
            ]
        }
    
    def analyze_access_point(self, ssid: str, bssid: str, security: str, 
                           signal_dbm: float, frequency: int) -> SecurityAnalysisResult:
        """Perform comprehensive security analysis of access point"""
        
        # Get base security profile
        security_profile = self.config.get_security_profile(security)
        if not security_profile:
            # Fallback for unknown security types
            security_profile = self.config.get_security_profile("WPA2")
        
        base_score = security_profile.base_score
        attack_vectors = security_profile.attack_vectors.copy()
        risk_factors = [f"Security type: {security}"]
        recommendations = []
        
        # Signal strength analysis
        signal_bonus, signal_factors = self._analyze_signal_strength(signal_dbm)
        base_score += signal_bonus
        risk_factors.extend(signal_factors)
        
        # SSID analysis
        ssid_bonus, ssid_factors, ssid_recommendations = self._analyze_ssid(ssid)
        base_score += ssid_bonus
        risk_factors.extend(ssid_factors)
        recommendations.extend(ssid_recommendations)
        
        # Frequency analysis
        freq_factors = self._analyze_frequency(frequency)
        risk_factors.extend(freq_factors)
        
        # BSSID analysis (for patterns indicating default configs)
        bssid_factors = self._analyze_bssid(bssid)
        risk_factors.extend(bssid_factors)
        
        # Additional attack vectors based on analysis
        additional_vectors = self._get_additional_attack_vectors(
            security, signal_dbm, ssid, frequency
        )
        attack_vectors.extend(additional_vectors)
        
        # Security recommendations
        security_recommendations = self._get_security_recommendations(
            security, signal_dbm, ssid
        )
        recommendations.extend(security_recommendations)
        
        # Normalize score (0-100)
        final_score = max(0, min(100, base_score))
        
        # Determine threat level and color
        threat_level, threat_color = self.config.get_threat_level_for_score(final_score)
        
        # Calculate confidence based on signal strength and data completeness
        confidence = self._calculate_confidence(signal_dbm, ssid, security)
        
        return SecurityAnalysisResult(
            vulnerability_score=final_score,
            threat_level=threat_level,
            threat_color=threat_color,
            attack_vectors=list(set(attack_vectors)),  # Remove duplicates
            risk_factors=risk_factors,
            recommendations=recommendations,
            confidence=confidence
        )
    
    def _analyze_signal_strength(self, signal_dbm: float) -> Tuple[int, List[str]]:
        """Analyze signal strength for vulnerability scoring"""
        signal_range = self.config.get_signal_range_info(signal_dbm)
        factors = []
        bonus = 0
        
        if signal_range:
            bonus = signal_range.bonus
            
        if signal_dbm > -30:
            factors.append("Excellent signal strength - highly accessible")
        elif signal_dbm > -50:
            factors.append("Good signal strength - easily accessible")
        elif signal_dbm > -70:
            factors.append("Fair signal strength - accessible with positioning")
        elif signal_dbm > -80:
            factors.append("Poor signal strength - requires proximity")
        else:
            factors.append("Very poor signal strength - limited accessibility")
            
        return bonus, factors
    
    def _analyze_ssid(self, ssid: str) -> Tuple[int, List[str], List[str]]:
        """Analyze SSID for security issues"""
        if not ssid or ssid.lower() in ['hidden', '']:
            return (5, ["Hidden SSID (minor security through obscurity)"], 
                    ["Consider using a descriptive but non-personal SSID"])
        
        factors = []
        recommendations = []
        bonus = 0
        
        ssid_lower = ssid.lower()
        
        # Check for default router names
        for pattern in self.ssid_patterns['default_names']:
            if re.search(pattern, ssid_lower):
                bonus += 15
                factors.append(f"Default/common SSID name detected: {ssid}")
                recommendations.append("Change SSID from default router name")
                break
        
        # Check for weak patterns
        for pattern in self.ssid_patterns['weak_patterns']:
            if re.search(pattern, ssid_lower):
                bonus += 10
                factors.append(f"Weak SSID pattern detected")
                recommendations.append("Use a unique, non-obvious SSID name")
                break
        
        # Check for personal information
        for pattern in self.ssid_patterns['personal_info']:
            if re.search(pattern, ssid_lower):
                bonus += 8
                factors.append("SSID may contain personal information")
                recommendations.append("Avoid personal information in SSID")
                break
        
        # Check SSID length
        if len(ssid) < 3:
            bonus += 5
            factors.append("Very short SSID")
        elif len(ssid) > 32:
            factors.append("SSID exceeds standard length")
        
        # Check for special characters (can indicate technical knowledge)
        if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', ssid):
            bonus -= 2  # Slight reduction for complexity
            factors.append("SSID contains special characters")
        
        return bonus, factors, recommendations
    
    def _analyze_frequency(self, frequency: int) -> List[str]:
        """Analyze frequency band characteristics"""
        factors = []
        
        if 2400 <= frequency <= 2500:
            factors.append("2.4 GHz band - longer range, more interference")
        elif 5000 <= frequency <= 6000:
            factors.append("5 GHz band - shorter range, less congested")
        elif frequency > 6000:
            factors.append("6 GHz band - latest standard, limited device support")
        else:
            factors.append(f"Unusual frequency: {frequency} MHz")
        
        return factors
    
    def _analyze_bssid(self, bssid: str) -> List[str]:
        """Analyze BSSID for patterns indicating default configurations"""
        factors = []
        
        if not bssid or bssid == "Unknown":
            return factors
        
        # Check for sequential patterns that might indicate default configs
        octets = bssid.split(':')
        if len(octets) == 6:
            # Check for patterns like 00:00:00:xx:xx:xx
            if octets[0] == '00' and octets[1] == '00' and octets[2] == '00':
                factors.append("BSSID suggests default configuration")
            
            # Check for vendor-specific default patterns
            if octets[3] == octets[4] == octets[5]:
                factors.append("BSSID shows repetitive pattern")
        
        return factors
    
    def _get_additional_attack_vectors(self, security: str, signal_dbm: float, 
                                     ssid: str, frequency: int) -> List[str]:
        """Get additional attack vectors based on analysis"""
        additional_vectors = []
        
        # Strong signal enables more attacks
        if signal_dbm > -40:
            additional_vectors.extend([
                "Physical proximity attacks",
                "RF jamming attacks",
                "Rogue AP setup"
            ])
        
        # Weak security + good signal = more vectors
        if security in ['Open', 'WEP'] and signal_dbm > -60:
            additional_vectors.extend([
                "Wardriving attacks",
                "Passive monitoring",
                "Session hijacking"
            ])
        
        # Default SSID patterns suggest more vulnerabilities
        ssid_lower = ssid.lower() if ssid else ""
        for pattern in self.ssid_patterns['default_names']:
            if re.search(pattern, ssid_lower):
                additional_vectors.extend([
                    "Default credential attacks",
                    "Firmware vulnerability exploitation",
                    "Router management interface attacks"
                ])
                break
        
        # WPS attacks for certain vendors/patterns
        if security in ['WPA', 'WPA2']:
            additional_vectors.append("WPS PIN brute force")
            additional_vectors.append("Pixie Dust attack")
        
        return additional_vectors
    
    def _get_security_recommendations(self, security: str, signal_dbm: float, 
                                    ssid: str) -> List[str]:
        """Get security recommendations based on analysis"""
        recommendations = []
        
        # Security protocol recommendations
        if security == "Open":
            recommendations.extend([
                "Enable WPA3 or WPA2 encryption immediately",
                "Use a strong, unique password",
                "Consider MAC address filtering for sensitive networks"
            ])
        elif security == "WEP":
            recommendations.extend([
                "Upgrade to WPA3 or WPA2 immediately",
                "WEP is easily crackable and should never be used",
                "Update router firmware to support modern security"
            ])
        elif security == "WPA":
            recommendations.extend([
                "Upgrade to WPA3 or WPA2 for better security",
                "Use a strong passphrase (12+ characters)",
                "Disable WPS if not needed"
            ])
        elif security == "WPA2":
            recommendations.extend([
                "Consider upgrading to WPA3 if supported",
                "Use a strong passphrase (15+ characters)",
                "Disable WPS to prevent PIN attacks",
                "Enable 802.11w (Management Frame Protection)"
            ])
        elif security == "WPA3":
            recommendations.extend([
                "Excellent security choice",
                "Ensure all devices support WPA3",
                "Use SAE (Simultaneous Authentication of Equals)"
            ])
        
        # Signal strength recommendations
        if signal_dbm > -30:
            recommendations.append("Consider reducing transmit power to limit range")
        
        # General recommendations
        recommendations.extend([
            "Change default router admin credentials",
            "Keep router firmware updated",
            "Disable unnecessary services (Telnet, SSH, UPnP)",
            "Enable router firewall",
            "Use guest network for visitors",
            "Monitor connected devices regularly"
        ])
        
        return recommendations
    
    def _calculate_confidence(self, signal_dbm: float, ssid: str, security: str) -> float:
        """Calculate confidence score for the analysis"""
        confidence = 0.5  # Base confidence
        
        # Signal strength affects confidence
        if signal_dbm > -50:
            confidence += 0.3
        elif signal_dbm > -70:
            confidence += 0.2
        elif signal_dbm > -85:
            confidence += 0.1
        
        # SSID availability affects confidence
        if ssid and ssid.lower() not in ['hidden', '']:
            confidence += 0.15
        
        # Security detection affects confidence
        if security and security != "Unknown":
            confidence += 0.15
        
        return min(1.0, confidence)
    
    def get_analysis_summary(self, results: List[SecurityAnalysisResult]) -> Dict[str, Any]:
        """Generate summary statistics from multiple analysis results"""
        if not results:
            return {}
        
        total_aps = len(results)
        threat_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        security_types = {}
        avg_score = 0
        
        for result in results:
            threat_counts[result.threat_level] += 1
            avg_score += result.vulnerability_score
        
        avg_score = avg_score / total_aps if total_aps > 0 else 0
        
        return {
            "total_access_points": total_aps,
            "threat_distribution": threat_counts,
            "average_vulnerability_score": round(avg_score, 1),
            "security_type_distribution": security_types,
            "high_risk_percentage": round((threat_counts["CRITICAL"] + threat_counts["HIGH"]) / total_aps * 100, 1) if total_aps > 0 else 0
        }


# Global security analysis engine instance
security_engine = SecurityAnalysisEngine()
