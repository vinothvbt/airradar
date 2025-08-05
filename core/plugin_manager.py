#!/usr/bin/env python3
"""
Plugin Manager for WiFi Security Radar Suite
Handles discovery, loading, and management of WiFi monitoring plugins
"""

import os
import sys
import logging
import importlib
import inspect
from pathlib import Path
from typing import Dict, List, Type, Optional, Any
from PyQt5.QtCore import QObject, pyqtSignal

from .plugin_base import WiFiPlugin, PluginMetadata

logger = logging.getLogger(__name__)


class PluginManager(QObject):
    """
    Manages WiFi monitoring plugins
    
    Handles plugin discovery, loading, validation, and lifecycle management
    """
    
    # Signals for plugin events
    plugin_loaded = pyqtSignal(str)  # Plugin name
    plugin_unloaded = pyqtSignal(str)  # Plugin name
    plugin_error = pyqtSignal(str, str)  # Plugin name, error message
    
    def __init__(self):
        super().__init__()
        self._plugins: Dict[str, Type[WiFiPlugin]] = {}
        self._plugin_instances: Dict[str, WiFiPlugin] = {}
        self._plugin_paths: List[Path] = []
        self._default_plugin_dir = Path(__file__).parent.parent / "plugins"
        
        # Add default plugin directory
        if self._default_plugin_dir.exists():
            self.add_plugin_path(self._default_plugin_dir)
    
    def add_plugin_path(self, path: Path) -> bool:
        """
        Add a directory to search for plugins
        
        Args:
            path: Path to plugin directory
            
        Returns:
            bool: True if path added successfully
        """
        try:
            path = Path(path).resolve()
            if path.exists() and path.is_dir():
                if path not in self._plugin_paths:
                    self._plugin_paths.append(path)
                    logger.info(f"Added plugin path: {path}")
                return True
            else:
                logger.warning(f"Plugin path does not exist or is not a directory: {path}")
                return False
        except Exception as e:
            logger.error(f"Error adding plugin path {path}: {e}")
            return False
    
    def discover_plugins(self) -> int:
        """
        Discover all available plugins in plugin paths
        
        Returns:
            int: Number of plugins discovered
        """
        discovered_count = 0
        
        for plugin_path in self._plugin_paths:
            try:
                discovered_count += self._discover_plugins_in_path(plugin_path)
            except Exception as e:
                logger.error(f"Error discovering plugins in {plugin_path}: {e}")
        
        logger.info(f"Discovered {discovered_count} plugins")
        return discovered_count
    
    def _discover_plugins_in_path(self, path: Path) -> int:
        """Discover plugins in a specific path"""
        count = 0
        
        # Add path to Python path if not already there
        path_str = str(path)
        if path_str not in sys.path:
            sys.path.insert(0, path_str)
        
        try:
            # Look for Python files in the directory
            for file_path in path.glob("*.py"):
                if file_path.name.startswith("__"):
                    continue
                
                try:
                    module_name = file_path.stem
                    self._load_plugin_from_file(file_path, module_name)
                    count += 1
                except Exception as e:
                    logger.warning(f"Failed to load plugin from {file_path}: {e}")
            
            # Look for plugin packages (directories with __init__.py)
            for dir_path in path.iterdir():
                if dir_path.is_dir() and (dir_path / "__init__.py").exists():
                    try:
                        self._load_plugin_from_package(dir_path)
                        count += 1
                    except Exception as e:
                        logger.warning(f"Failed to load plugin package {dir_path}: {e}")
        
        finally:
            # Remove path from Python path
            if path_str in sys.path:
                sys.path.remove(path_str)
        
        return count
    
    def _load_plugin_from_file(self, file_path: Path, module_name: str):
        """Load plugin from a single Python file"""
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None:
            raise ImportError(f"Could not load spec from {file_path}")
        
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Find WiFiPlugin subclasses in the module
        plugin_classes = self._find_plugin_classes(module)
        
        for plugin_class in plugin_classes:
            self._register_plugin_class(plugin_class)
    
    def _load_plugin_from_package(self, package_path: Path):
        """Load plugin from a package directory"""
        package_name = package_path.name
        
        # Import the package
        spec = importlib.util.spec_from_file_location(
            package_name, 
            package_path / "__init__.py"
        )
        if spec is None:
            raise ImportError(f"Could not load spec from package {package_path}")
        
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Find WiFiPlugin subclasses in the package
        plugin_classes = self._find_plugin_classes(module)
        
        for plugin_class in plugin_classes:
            self._register_plugin_class(plugin_class)
    
    def _find_plugin_classes(self, module) -> List[Type[WiFiPlugin]]:
        """Find WiFiPlugin subclasses in a module"""
        plugin_classes = []
        
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if (issubclass(obj, WiFiPlugin) and 
                obj is not WiFiPlugin and 
                not inspect.isabstract(obj)):
                plugin_classes.append(obj)
        
        return plugin_classes
    
    def _register_plugin_class(self, plugin_class: Type[WiFiPlugin]):
        """Register a plugin class"""
        try:
            # Create temporary instance to get metadata
            temp_instance = plugin_class()
            metadata = temp_instance.metadata
            
            # Validate metadata
            if not isinstance(metadata, PluginMetadata):
                raise ValueError("Plugin metadata must be a PluginMetadata instance")
            
            # Check for name conflicts
            if metadata.name in self._plugins:
                logger.warning(f"Plugin name conflict: {metadata.name}. Skipping registration.")
                return
            
            # Validate dependencies
            success, missing_deps = temp_instance.validate_dependencies()
            if not success:
                logger.warning(f"Plugin {metadata.name} has missing dependencies: {missing_deps}")
                # Still register but mark as having issues
            
            # Register the plugin
            self._plugins[metadata.name] = plugin_class
            logger.info(f"Registered plugin: {metadata.name} v{metadata.version}")
            
            # Clean up temporary instance
            temp_instance.cleanup()
            
        except Exception as e:
            logger.error(f"Failed to register plugin class {plugin_class.__name__}: {e}")
    
    def get_available_plugins(self) -> Dict[str, PluginMetadata]:
        """
        Get metadata for all available plugins
        
        Returns:
            Dict[str, PluginMetadata]: Plugin name to metadata mapping
        """
        plugins_info = {}
        
        for name, plugin_class in self._plugins.items():
            try:
                # Create temporary instance to get metadata
                temp_instance = plugin_class()
                plugins_info[name] = temp_instance.metadata
                temp_instance.cleanup()
            except Exception as e:
                logger.error(f"Error getting metadata for plugin {name}: {e}")
        
        return plugins_info
    
    def load_plugin(self, plugin_name: str, config: Dict[str, Any] = None) -> Optional[WiFiPlugin]:
        """
        Load and instantiate a plugin
        
        Args:
            plugin_name: Name of the plugin to load
            config: Optional configuration for the plugin
            
        Returns:
            WiFiPlugin instance or None if loading failed
        """
        if plugin_name not in self._plugins:
            logger.error(f"Plugin not found: {plugin_name}")
            return None
        
        if plugin_name in self._plugin_instances:
            logger.warning(f"Plugin {plugin_name} is already loaded")
            return self._plugin_instances[plugin_name]
        
        try:
            plugin_class = self._plugins[plugin_name]
            plugin_instance = plugin_class()
            
            # Configure the plugin
            if config:
                if not plugin_instance.configure(config):
                    logger.warning(f"Failed to configure plugin {plugin_name}")
            
            # Validate dependencies
            success, missing_deps = plugin_instance.validate_dependencies()
            if not success:
                logger.error(f"Plugin {plugin_name} has missing dependencies: {missing_deps}")
                plugin_instance.cleanup()
                return None
            
            # Store the instance
            self._plugin_instances[plugin_name] = plugin_instance
            
            logger.info(f"Loaded plugin: {plugin_name}")
            self.plugin_loaded.emit(plugin_name)
            
            return plugin_instance
            
        except Exception as e:
            logger.error(f"Failed to load plugin {plugin_name}: {e}")
            self.plugin_error.emit(plugin_name, str(e))
            return None
    
    def unload_plugin(self, plugin_name: str) -> bool:
        """
        Unload a plugin instance
        
        Args:
            plugin_name: Name of the plugin to unload
            
        Returns:
            bool: True if unloaded successfully
        """
        if plugin_name not in self._plugin_instances:
            logger.warning(f"Plugin {plugin_name} is not loaded")
            return False
        
        try:
            plugin_instance = self._plugin_instances[plugin_name]
            plugin_instance.cleanup()
            del self._plugin_instances[plugin_name]
            
            logger.info(f"Unloaded plugin: {plugin_name}")
            self.plugin_unloaded.emit(plugin_name)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to unload plugin {plugin_name}: {e}")
            self.plugin_error.emit(plugin_name, str(e))
            return False
    
    def get_loaded_plugins(self) -> Dict[str, WiFiPlugin]:
        """Get all currently loaded plugin instances"""
        return self._plugin_instances.copy()
    
    def get_plugin(self, plugin_name: str) -> Optional[WiFiPlugin]:
        """Get a specific loaded plugin instance"""
        return self._plugin_instances.get(plugin_name)
    
    def unload_all_plugins(self):
        """Unload all currently loaded plugins"""
        plugin_names = list(self._plugin_instances.keys())
        for plugin_name in plugin_names:
            self.unload_plugin(plugin_name)
    
    def reload_plugin(self, plugin_name: str, config: Dict[str, Any] = None) -> Optional[WiFiPlugin]:
        """
        Reload a plugin (unload and load again)
        
        Args:
            plugin_name: Name of the plugin to reload
            config: Optional new configuration for the plugin
            
        Returns:
            WiFiPlugin instance or None if reloading failed
        """
        if plugin_name in self._plugin_instances:
            self.unload_plugin(plugin_name)
        
        return self.load_plugin(plugin_name, config)


# Global plugin manager instance
plugin_manager = PluginManager()