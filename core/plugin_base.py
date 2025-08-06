#!/usr/bin/env python3
"""
Base Plugin Interface for WiFi Security Radar Suite
Provides standardized interface for WiFi monitoring tools
"""

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Tuple
from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtCore import pyqtSignal, QObject


@dataclass
class PluginMetadata:
    """Metadata for WiFi monitoring plugins"""
    name: str
    version: str
    description: str
    author: str
    requires_root: bool = True
    capabilities: List[str] = None
    dependencies: List[str] = None
    
    def __post_init__(self):
        if self.capabilities is None:
            self.capabilities = []
        if self.dependencies is None:
            self.dependencies = []


class WiFiScanResult:
    """Standardized WiFi scan result"""
    
    def __init__(self, ssid: str, bssid: str, signal_strength: int, 
                 security: str, channel: int, frequency: str = None):
        self.ssid = ssid
        self.bssid = bssid
        self.signal_strength = signal_strength
        self.security = security
        self.channel = channel
        self.frequency = frequency
        self.vendor = None
        self.distance = None
        self.vulnerability_score = None
        self.additional_data = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert scan result to dictionary"""
        return {
            'ssid': self.ssid,
            'bssid': self.bssid,
            'signal_strength': self.signal_strength,
            'security': self.security,
            'channel': self.channel,
            'frequency': self.frequency,
            'vendor': self.vendor,
            'distance': self.distance,
            'vulnerability_score': self.vulnerability_score,
            'additional_data': self.additional_data
        }


class QObjectMeta(type(QObject)):
    """Metaclass for QObject compatibility with ABC"""
    pass


class ABCQObjectMeta(ABCMeta, QObjectMeta):
    """Combined metaclass for ABC and QObject"""
    pass


class WiFiPlugin(QObject, metaclass=ABCQObjectMeta):
    """
    Abstract base class for WiFi monitoring plugins
    
    All WiFi monitoring tools should inherit from this class
    and implement the required abstract methods.
    """
    
    # Signals for plugin communication
    scan_started = pyqtSignal()
    scan_completed = pyqtSignal(list)  # List of WiFiScanResult
    scan_progress = pyqtSignal(int)  # Progress percentage
    error_occurred = pyqtSignal(str)  # Error message
    
    def __init__(self):
        super().__init__()
        self._metadata = None
        self._config = {}
        self._is_scanning = False
        self._scan_results = []
    
    @property
    @abstractmethod
    def metadata(self) -> PluginMetadata:
        """Return plugin metadata"""
        pass
    
    @abstractmethod
    def create_main_window(self) -> QMainWindow:
        """Create and return the main window for this plugin"""
        pass
    
    @abstractmethod
    def start_scan(self, **kwargs) -> bool:
        """
        Start WiFi scanning
        
        Returns:
            bool: True if scan started successfully, False otherwise
        """
        pass
    
    @abstractmethod
    def stop_scan(self) -> bool:
        """
        Stop WiFi scanning
        
        Returns:
            bool: True if scan stopped successfully, False otherwise
        """
        pass
    
    @abstractmethod
    def get_scan_results(self) -> List[WiFiScanResult]:
        """
        Get current scan results
        
        Returns:
            List[WiFiScanResult]: List of current scan results
        """
        pass
    
    def configure(self, config: Dict[str, Any]) -> bool:
        """
        Configure the plugin with settings
        
        Args:
            config: Configuration dictionary
            
        Returns:
            bool: True if configuration successful, False otherwise
        """
        self._config = config
        return True
    
    def get_config(self) -> Dict[str, Any]:
        """Get current plugin configuration"""
        return self._config.copy()
    
    def is_scanning(self) -> bool:
        """Check if plugin is currently scanning"""
        return self._is_scanning
    
    def validate_dependencies(self) -> Tuple[bool, List[str]]:
        """
        Validate plugin dependencies
        
        Returns:
            Tuple[bool, List[str]]: (success, missing_dependencies)
        """
        missing = []
        for dep in self.metadata.dependencies:
            try:
                __import__(dep)
            except ImportError:
                missing.append(dep)
        
        return len(missing) == 0, missing
    
    def get_capabilities(self) -> List[str]:
        """Get plugin capabilities"""
        return self.metadata.capabilities.copy()
    
    def supports_capability(self, capability: str) -> bool:
        """Check if plugin supports a specific capability"""
        return capability in self.metadata.capabilities
    
    def cleanup(self):
        """Cleanup resources when plugin is unloaded"""
        if self._is_scanning:
            self.stop_scan()


class WiFiPluginWidget(QWidget):
    """
    Base widget class for plugin UI components
    
    Provides common functionality for plugin widgets
    """
    
    def __init__(self, plugin: WiFiPlugin, parent=None):
        super().__init__(parent)
        self.plugin = plugin
        self._setup_connections()
    
    def _setup_connections(self):
        """Setup signal connections with the plugin"""
        self.plugin.scan_started.connect(self.on_scan_started)
        self.plugin.scan_completed.connect(self.on_scan_completed)
        self.plugin.scan_progress.connect(self.on_scan_progress)
        self.plugin.error_occurred.connect(self.on_error)
    
    def on_scan_started(self):
        """Handle scan started signal"""
        pass
    
    def on_scan_completed(self, results: List[WiFiScanResult]):
        """Handle scan completed signal"""
        pass
    
    def on_scan_progress(self, progress: int):
        """Handle scan progress signal"""
        pass
    
    def on_error(self, error_message: str):
        """Handle error signal"""
        pass