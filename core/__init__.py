"""
Core framework for WiFi Security Radar Suite
Provides base classes and interfaces for modular architecture
"""

from .plugin_base import WiFiPlugin, PluginMetadata
from .plugin_manager import PluginManager

__all__ = ['WiFiPlugin', 'PluginMetadata', 'PluginManager']