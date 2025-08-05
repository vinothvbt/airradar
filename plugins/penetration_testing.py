#!/usr/bin/env python3
"""
Penetration Testing Radar Plugin
Modern radar v4.0 with advanced visualization and vulnerability analysis
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import core modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.plugin_base import WiFiPlugin, PluginMetadata, WiFiScanResult
from PyQt5.QtWidgets import QMainWindow


class PenetrationTestingPlugin(WiFiPlugin):
    """
    Penetration Testing Radar Plugin
    
    Provides modern radar display with advanced visualization modes,
    vulnerability scoring, and comprehensive threat analysis.
    """
    
    @property
    def metadata(self) -> PluginMetadata:
        """Return plugin metadata"""
        return PluginMetadata(
            name="Penetration Testing Radar",
            version="4.0.0",
            description="Modern radar with advanced visualization and vulnerability analysis",
            author="WiFi Security Tools", 
            requires_root=True,
            capabilities=[
                "wifi_scanning",
                "radar_visualization",
                "vulnerability_assessment",
                "threat_analysis",
                "attack_vector_identification",
                "multiple_radar_modes",
                "distance_calculation",
                "vendor_identification"
            ],
            dependencies=["PyQt5", "requests"]
        )
    
    def create_main_window(self) -> QMainWindow:
        """Create and return the main window for this plugin"""
        # Import the original window class
        from wifi_pentest_radar_modern import WiFiPentestRadarModern
        
        window = WiFiPentestRadarModern()
        
        # Connect the window's scanning signals to our plugin signals
        self._connect_window_signals(window)
        
        return window
    
    def _connect_window_signals(self, window):
        """Connect window signals to plugin signals"""
        # We'll need to modify the original window to emit these signals
        # For now, we'll set up basic connections
        try:
            if hasattr(window, 'scan_started'):
                window.scan_started.connect(self.scan_started.emit)
            if hasattr(window, 'scan_completed'):
                window.scan_completed.connect(self._on_scan_completed)
            if hasattr(window, 'scan_progress'):
                window.scan_progress.connect(self.scan_progress.emit)
            if hasattr(window, 'error_occurred'):
                window.error_occurred.connect(self.error_occurred.emit)
        except AttributeError:
            # Signals not available in original window
            pass
    
    def _on_scan_completed(self, results):
        """Convert window scan results to plugin format"""
        converted_results = []
        
        # Convert results to WiFiScanResult format
        if isinstance(results, list):
            for result in results:
                if isinstance(result, dict):
                    wifi_result = WiFiScanResult(
                        ssid=result.get('ssid', ''),
                        bssid=result.get('bssid', ''),
                        signal_strength=result.get('signal_strength', 0),
                        security=result.get('security', ''),
                        channel=result.get('channel', 0),
                        frequency=result.get('frequency', '')
                    )
                    wifi_result.vendor = result.get('vendor')
                    wifi_result.distance = result.get('distance')
                    wifi_result.vulnerability_score = result.get('vulnerability_score')
                    wifi_result.additional_data = {
                        'attack_vectors': result.get('attack_vectors', []),
                        'threat_level': result.get('threat_level', 'UNKNOWN'),
                        'confidence': result.get('confidence', 0)
                    }
                    converted_results.append(wifi_result)
        
        self._scan_results = converted_results
        self.scan_completed.emit(converted_results)
    
    def start_scan(self, **kwargs) -> bool:
        """Start WiFi scanning"""
        # This would normally trigger scanning in the window
        # For now, return True as scanning is handled by the window itself
        self._is_scanning = True
        return True
    
    def stop_scan(self) -> bool:
        """Stop WiFi scanning"""
        # This would normally stop scanning in the window
        self._is_scanning = False
        return True
    
    def get_scan_results(self) -> list:
        """Get current scan results"""
        return self._scan_results.copy()


# Plugin entry point - this is what the plugin manager looks for
def get_plugin_class():
    """Return the plugin class"""
    return PenetrationTestingPlugin