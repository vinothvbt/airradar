#!/usr/bin/env python3
"""
Configuration Manager for WiFi Security Radar Suite
Handles loading and validation of configuration settings
"""

import json
import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class SecurityProfile:
    """Security profile configuration"""
    base_score: int
    risk_level: str
    attack_vectors: List[str]


@dataclass
class SignalRange:
    """Signal strength range configuration"""
    min_dbm: int
    multiplier: float
    bonus: int = 0


@dataclass
class VisualizationMode:
    """Visualization mode configuration"""
    name: str
    description: str
    settings: Dict[str, Any]


class ConfigurationManager:
    """Manages application configuration from JSON files"""

    def __init__(self, config_file: str = "config.json"):
        self.config_file = Path(config_file)
        self.config = {}
        self.security_profiles = {}
        self.signal_ranges = {}
        self.visualization_modes = {}
        self.vendor_database = {}

        self._load_configuration()
        self._parse_security_profiles()
        self._parse_signal_ranges()
        self._parse_visualization_modes()

    def _load_configuration(self):
        """Load configuration from JSON file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
                logger.info(f"Configuration loaded from {self.config_file}")
            else:
                logger.warning(
                    f"Configuration file {
                        self.config_file} not found, using defaults")
                self.config = self._get_default_config()

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file: {e}")
            self.config = self._get_default_config()
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            self.config = self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Return minimal default configuration"""
        return {
            "wifi_scanner": {
                "interface_detection": {
                    "commands": {
                        "scan_command": ["iw", "dev", "{interface}", "scan"]
                    },
                    "timeouts": {"scan_timeout": 15}
                }
            },
            "security_analysis": {
                "vulnerability_scoring": {
                    "security_types": {
                        "Open": {"base_score": 90, "risk_level": "CRITICAL", "attack_vectors": ["Direct Access"]},
                        "WEP": {"base_score": 85, "risk_level": "CRITICAL", "attack_vectors": ["WEP Cracking"]},
                        "WPA": {"base_score": 40, "risk_level": "HIGH", "attack_vectors": ["Handshake Capture"]},
                        "WPA2": {"base_score": 30, "risk_level": "MEDIUM", "attack_vectors": ["PMKID Attack"]},
                        "WPA3": {"base_score": 10, "risk_level": "LOW", "attack_vectors": ["SAE Attack"]}
                    }
                }
            }
        }

    def _parse_security_profiles(self):
        """Parse security profiles from configuration"""
        try:
            # Try new format first (from config.json)
            security_types = self.config.get("security_profiles", {})

            # If empty, try old format for backward compatibility
            if not security_types:
                security_types = self.config.get(
                    "security_analysis",
                    {}).get(
                    "vulnerability_scoring",
                    {}).get(
                    "security_types",
                    {})

            for sec_type, profile_data in security_types.items():
                self.security_profiles[sec_type] = SecurityProfile(
                    base_score=profile_data.get("base_score", 50),
                    risk_level=profile_data.get("risk_level", "MEDIUM"),
                    attack_vectors=profile_data.get("attack_vectors", [])
                )

            logger.info(
                f"Loaded {len(self.security_profiles)} security profiles")

        except Exception as e:
            logger.error(f"Error parsing security profiles: {e}")

    def _parse_signal_ranges(self):
        """Parse signal strength ranges from configuration"""
        try:
            # Try new format first (from config.json)
            signal_ranges = self.config.get("signal_strength_ranges", {})

            # If empty, try old format for backward compatibility
            if not signal_ranges:
                signal_ranges = self.config.get(
                    "distance_calculation",
                    {}).get(
                    "formulas",
                    {}).get(
                    "signal_ranges",
                    {})

            for range_name, range_data in signal_ranges.items():
                self.signal_ranges[range_name] = SignalRange(
                    min_dbm=range_data.get("min_dbm", -70),
                    multiplier=range_data.get("multiplier", 1.0),
                    bonus=range_data.get("bonus", 0)
                )

            logger.info(f"Loaded {len(self.signal_ranges)} signal ranges")

        except Exception as e:
            logger.error(f"Error parsing signal ranges: {e}")

    def _parse_visualization_modes(self):
        """Parse visualization modes from configuration"""
        try:
            # Try new format first (from config.json)
            viz_modes = self.config.get("visualization_modes", {})

            # If empty, try old format for backward compatibility
            if not viz_modes:
                viz_modes = self.config.get(
                    "visualization", {}).get(
                    "radar_modes", {})

            for mode_name, mode_data in viz_modes.items():
                self.visualization_modes[mode_name] = VisualizationMode(
                    name=mode_data.get("name", mode_name),
                    description=mode_data.get("description", ""),
                    settings=mode_data.get("settings", {})
                )

            logger.info(
                f"Loaded {len(self.visualization_modes)} visualization modes")

        except Exception as e:
            logger.error(f"Error parsing visualization modes: {e}")

    def get_security_profile(
            self,
            security_type: str) -> Optional[SecurityProfile]:
        """Get security profile for given security type"""
        return self.security_profiles.get(security_type)

    def get_signal_range_info(
            self,
            signal_dbm: float) -> Optional[SignalRange]:
        """Get signal range information for given signal strength"""
        for range_name, signal_range in self.signal_ranges.items():
            if signal_dbm >= signal_range.min_dbm:
                return signal_range
        return None

    def get_visualization_mode(
            self, mode_name: str) -> Optional[VisualizationMode]:
        """Get visualization mode configuration"""
        return self.visualization_modes.get(mode_name)

    def get_scan_command(self, interface: str) -> List[str]:
        """Get scan command for interface"""
        cmd_template = self.config.get(
            "wifi_scanner", {}).get(
            "interface_detection", {}).get(
            "commands", {}).get(
                "scan_command", [
                    "iw", "dev", "{interface}", "scan"])
        return [
            cmd.format(
                interface=interface) if "{interface}" in cmd else cmd for cmd in cmd_template]

    def get_scan_timeout(self) -> int:
        """Get scan timeout value"""
        return self.config.get(
            "wifi_scanner",
            {}).get(
            "interface_detection",
            {}).get(
            "timeouts",
            {}).get(
                "scan_timeout",
            15)

    def get_parsing_patterns(self) -> Dict[str, str]:
        """Get regex patterns for parsing scan output"""
        return self.config.get("wifi_scanner", {}).get("parsing", {}).get("patterns", {
            "mac_address": r"([0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2})",
            "signal_strength": r"signal:\s*(-\d+\.?\d*)\s*dBm",
            "frequency": r"freq:\s*(\d+)",
            "ssid": r"SSID:\s*(.+)"
        })

    def get_security_keywords(self) -> Dict[str, List[str]]:
        """Get security detection keywords"""
        return self.config.get(
            "wifi_scanner", {}).get(
            "parsing", {}).get(
            "security_keywords", {
                "WPA3": [
                    "WPA3", "SAE"], "WPA2": [
                        "WPA2", "RSN"], "WPA": ["WPA"], "WEP": [
                            "WEP", "Privacy"], "Open": []})

    def get_distance_formula_params(self) -> Dict[str, Any]:
        """Get distance calculation parameters"""
        return self.config.get("distance_calculation", {}).get("formulas", {})

    def get_frequency_corrections(self) -> Dict[str, Dict[str, Any]]:
        """Get frequency-specific corrections for distance calculation"""
        return self.config.get(
            "distance_calculation",
            {}).get(
            "formulas",
            {}).get(
            "frequency_corrections",
            {})

    def get_vendor_config(self) -> Dict[str, Any]:
        """Get vendor detection configuration"""
        return self.config.get("vendor_detection", {})

    def get_ui_layout_config(self) -> Dict[str, Any]:
        """Get UI layout configuration"""
        return self.config.get("ui_layout", {})

    def get_color_scheme(self) -> Dict[str, str]:
        """Get color scheme configuration"""
        return self.config.get("visualization", {}).get("colors", {})

    def get_threat_level_for_score(self, score: int) -> Tuple[str, str]:
        """Get threat level and color for vulnerability score"""
        threat_levels = self.config.get(
            "security_analysis", {}).get(
            "vulnerability_scoring", {}).get(
            "threat_levels", {
                "CRITICAL": {
                    "min": 80, "color": "#ff4444"}, "HIGH": {
                        "min": 60, "color": "#ff8800"}, "MEDIUM": {
                            "min": 40, "color": "#ffaa00"}, "LOW": {
                                "min": 0, "color": "#88ff88"}})

        for level, config in sorted(
                threat_levels.items(), key=lambda x: x[1]["min"], reverse=True):
            if score >= config["min"]:
                return level, config.get("color", "#ffffff")

        return "LOW", "#88ff88"

    def save_configuration(self):
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            logger.info(f"Configuration saved to {self.config_file}")
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")

    def reload_configuration(self):
        """Reload configuration from file"""
        self._load_configuration()
        self._parse_security_profiles()
        self._parse_signal_ranges()
        self._parse_visualization_modes()
        logger.info("Configuration reloaded")


# Global configuration instance
config_manager = ConfigurationManager()

# Alias for backward compatibility
ConfigManager = ConfigurationManager
