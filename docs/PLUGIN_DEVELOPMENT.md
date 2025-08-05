# Plugin Development Guide

## WiFi Security Radar Suite - Plugin Development

This guide explains how to develop and integrate new modules for the WiFi Security Radar Suite using the plugin system.

## Overview

The WiFi Security Radar Suite uses a modular plugin architecture that allows easy addition and removal of WiFi monitoring tools. The plugin system provides:

- **Standardized interfaces** for consistent functionality
- **Automatic plugin discovery** and loading
- **Dependency validation** and error handling
- **Signal-based communication** between plugins and the main application
- **Configuration management** for plugin settings

## Plugin Architecture

### Core Components

1. **Plugin Base Classes** (`core/plugin_base.py`)
   - `WiFiPlugin`: Abstract base class for all plugins
   - `PluginMetadata`: Plugin information and capabilities
   - `WiFiScanResult`: Standardized scan result format
   - `WiFiPluginWidget`: Base widget for plugin UI components

2. **Plugin Manager** (`core/plugin_manager.py`)
   - Discovers and loads plugins from directories
   - Manages plugin lifecycle (load/unload/reload)
   - Validates dependencies and capabilities
   - Provides plugin registry and instance management

3. **Plugin Directory** (`plugins/`)
   - Contains all plugin implementations
   - Supports both single-file and package-based plugins
   - Automatic discovery of `WiFiPlugin` subclasses

## Creating a New Plugin

### Step 1: Define Plugin Metadata

Create a new Python file in the `plugins/` directory:

```python
#!/usr/bin/env python3
"""
My Custom WiFi Tool Plugin
Description of what this plugin does
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import core modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.plugin_base import WiFiPlugin, PluginMetadata, WiFiScanResult
from PyQt5.QtWidgets import QMainWindow

class MyCustomPlugin(WiFiPlugin):
    """
    My Custom WiFi Tool Plugin
    
    Detailed description of plugin capabilities and features.
    """
    
    @property
    def metadata(self) -> PluginMetadata:
        """Return plugin metadata"""
        return PluginMetadata(
            name="My Custom WiFi Tool",
            version="1.0.0",
            description="Custom WiFi monitoring and analysis tool",
            author="Your Name",
            requires_root=True,  # Set to False if root not required
            capabilities=[
                "wifi_scanning",
                "custom_analysis",
                "special_feature"
            ],
            dependencies=["PyQt5", "requests"]  # List required packages
        )
```

### Step 2: Implement Required Methods

```python
    def create_main_window(self) -> QMainWindow:
        """Create and return the main window for this plugin"""
        # Create your main window/widget here
        window = MyCustomMainWindow()
        
        # Connect window signals to plugin signals
        self._connect_window_signals(window)
        
        return window
    
    def start_scan(self, **kwargs) -> bool:
        """Start WiFi scanning"""
        try:
            # Implement scanning logic
            self._is_scanning = True
            self.scan_started.emit()
            
            # Your scanning code here
            
            return True
        except Exception as e:
            self.error_occurred.emit(str(e))
            return False
    
    def stop_scan(self) -> bool:
        """Stop WiFi scanning"""
        try:
            # Implement scan stopping logic
            self._is_scanning = False
            return True
        except Exception as e:
            self.error_occurred.emit(str(e))
            return False
    
    def get_scan_results(self) -> List[WiFiScanResult]:
        """Get current scan results"""
        return self._scan_results.copy()
```

### Step 3: Handle Scan Results

Convert your scan results to the standardized format:

```python
    def _process_scan_results(self, raw_results):
        """Convert raw scan results to WiFiScanResult format"""
        converted_results = []
        
        for raw_result in raw_results:
            wifi_result = WiFiScanResult(
                ssid=raw_result['ssid'],
                bssid=raw_result['bssid'],
                signal_strength=raw_result['signal'],
                security=raw_result['encryption'],
                channel=raw_result['channel'],
                frequency=raw_result.get('frequency', '')
            )
            
            # Add optional fields
            wifi_result.vendor = raw_result.get('vendor')
            wifi_result.distance = raw_result.get('distance')
            wifi_result.vulnerability_score = raw_result.get('vuln_score')
            wifi_result.additional_data = {
                'custom_field': raw_result.get('custom_data')
            }
            
            converted_results.append(wifi_result)
        
        self._scan_results = converted_results
        self.scan_completed.emit(converted_results)
```

### Step 4: Create Plugin Entry Point

Add this at the end of your plugin file:

```python
# Plugin entry point - this is what the plugin manager looks for
def get_plugin_class():
    """Return the plugin class"""
    return MyCustomPlugin
```

## Plugin Capabilities

### Standard Capabilities

- `wifi_scanning`: Basic WiFi network scanning
- `signal_analysis`: Signal strength analysis and visualization
- `vendor_identification`: Device vendor identification
- `security_assessment`: Security protocol analysis
- `vulnerability_assessment`: Security vulnerability analysis
- `distance_calculation`: Distance estimation from signal strength
- `attack_vector_identification`: Identification of potential attack vectors
- `radar_visualization`: Radar-style network visualization
- `multiple_view_modes`: Support for different display modes
- `professional_theming`: Professional UI theming support

### Custom Capabilities

You can define custom capabilities for your plugin:

```python
capabilities=[
    "wifi_scanning",
    "custom_frequency_analysis",  # Custom capability
    "advanced_packet_capture",   # Custom capability
    "machine_learning_analysis"  # Custom capability
]
```

## Signal Communication

### Plugin Signals

All plugins inherit these signals from `WiFiPlugin`:

```python
# Scanning lifecycle signals
scan_started = pyqtSignal()
scan_completed = pyqtSignal(list)  # List of WiFiScanResult
scan_progress = pyqtSignal(int)    # Progress percentage (0-100)
error_occurred = pyqtSignal(str)   # Error message
```

### Emitting Signals

```python
# Start scanning
self.scan_started.emit()

# Report progress
self.scan_progress.emit(50)  # 50% complete

# Scanning complete
self.scan_completed.emit(scan_results)

# Error occurred
self.error_occurred.emit("Failed to access wireless interface")
```

## Configuration Management

### Plugin Configuration

```python
def configure(self, config: Dict[str, Any]) -> bool:
    """Configure the plugin with settings"""
    try:
        # Apply configuration settings
        self.scan_interval = config.get('scan_interval', 5)
        self.interface = config.get('interface', 'wlan0')
        self.enable_logging = config.get('logging', True)
        
        # Store configuration
        self._config = config
        return True
    except Exception as e:
        self.error_occurred.emit(f"Configuration error: {e}")
        return False

def get_config(self) -> Dict[str, Any]:
    """Get current plugin configuration"""
    return {
        'scan_interval': self.scan_interval,
        'interface': self.interface,
        'logging': self.enable_logging
    }
```

## UI Development

### Main Window Implementation

```python
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import pyqtSignal

class MyCustomMainWindow(QMainWindow):
    """Main window for the custom plugin"""
    
    # Signals to connect with plugin
    scan_started = pyqtSignal()
    scan_completed = pyqtSignal(list)
    scan_progress = pyqtSignal(int)
    error_occurred = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
        self._apply_theme()
    
    def _setup_ui(self):
        """Setup the user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Add your UI components here
        
    def _apply_theme(self):
        """Apply consistent theming"""
        # Use the standard airradar theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0A0A0A;
                color: #00FF00;
                font-family: 'JetBrains Mono', monospace;
            }
            /* Add more styling as needed */
        """)
```

### Using Plugin Widget Base Class

```python
from core.plugin_base import WiFiPluginWidget

class MyPluginWidget(WiFiPluginWidget):
    """Custom widget that automatically connects to plugin signals"""
    
    def __init__(self, plugin, parent=None):
        super().__init__(plugin, parent)
        self._setup_ui()
    
    def on_scan_started(self):
        """Called when scanning starts"""
        self.status_label.setText("Scanning...")
    
    def on_scan_completed(self, results):
        """Called when scanning completes"""
        self.status_label.setText(f"Found {len(results)} networks")
        self._update_results_display(results)
    
    def on_scan_progress(self, progress):
        """Called with scan progress updates"""
        self.progress_bar.setValue(progress)
    
    def on_error(self, error_message):
        """Called when an error occurs"""
        self.status_label.setText(f"Error: {error_message}")
```

## Testing Your Plugin

### Basic Plugin Test

Create a test file for your plugin:

```python
#!/usr/bin/env python3
"""
Test script for My Custom Plugin
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.plugin_manager import plugin_manager
from plugins.my_custom_plugin import MyCustomPlugin

def test_plugin():
    """Test the custom plugin"""
    
    # Test plugin instantiation
    plugin = MyCustomPlugin()
    
    # Test metadata
    metadata = plugin.metadata
    print(f"Plugin: {metadata.name} v{metadata.version}")
    print(f"Description: {metadata.description}")
    print(f"Capabilities: {metadata.capabilities}")
    
    # Test dependency validation
    success, missing = plugin.validate_dependencies()
    if success:
        print("✅ All dependencies satisfied")
    else:
        print(f"❌ Missing dependencies: {missing}")
    
    # Test configuration
    config = {
        'scan_interval': 10,
        'interface': 'wlan0'
    }
    if plugin.configure(config):
        print("✅ Configuration successful")
    else:
        print("❌ Configuration failed")
    
    # Test window creation
    try:
        window = plugin.create_main_window()
        print("✅ Main window created successfully")
        window.close()
    except Exception as e:
        print(f"❌ Window creation failed: {e}")
    
    # Cleanup
    plugin.cleanup()
    print("✅ Plugin test completed")

if __name__ == '__main__':
    test_plugin()
```

### Integration Test

Test with the plugin manager:

```python
def test_with_plugin_manager():
    """Test plugin with the plugin manager"""
    
    # Discover plugins
    count = plugin_manager.discover_plugins()
    print(f"Discovered {count} plugins")
    
    # Check if our plugin was found
    available = plugin_manager.get_available_plugins()
    if "My Custom WiFi Tool" in available:
        print("✅ Plugin discovered by manager")
        
        # Load the plugin
        plugin = plugin_manager.load_plugin("My Custom WiFi Tool")
        if plugin:
            print("✅ Plugin loaded successfully")
            
            # Test plugin functionality
            window = plugin.create_main_window()
            print("✅ Plugin window created")
            
            # Cleanup
            plugin_manager.unload_plugin("My Custom WiFi Tool")
            print("✅ Plugin unloaded")
        else:
            print("❌ Failed to load plugin")
    else:
        print("❌ Plugin not discovered")
```

## Advanced Features

### Multi-Window Support

```python
def create_main_window(self) -> QMainWindow:
    """Create main window with additional windows"""
    main_window = MyMainWindow()
    
    # Create additional windows if needed
    self.settings_window = MySettingsWindow()
    self.analysis_window = MyAnalysisWindow()
    
    # Connect windows
    main_window.show_settings.connect(self.settings_window.show)
    main_window.show_analysis.connect(self.analysis_window.show)
    
    return main_window
```

### Custom Data Processing

```python
def process_custom_data(self, raw_data):
    """Process custom data format"""
    # Implement custom processing logic
    processed_data = self._apply_custom_algorithms(raw_data)
    
    # Convert to standard format
    results = []
    for data in processed_data:
        result = WiFiScanResult(
            ssid=data['network_name'],
            bssid=data['mac_address'],
            signal_strength=data['signal_level'],
            security=data['encryption_type'],
            channel=data['channel_number']
        )
        
        # Add custom analysis results
        result.additional_data = {
            'custom_score': data['custom_analysis_score'],
            'threat_indicators': data['threat_indicators'],
            'performance_metrics': data['performance_data']
        }
        
        results.append(result)
    
    return results
```

### Background Processing

```python
from PyQt5.QtCore import QThread, pyqtSignal

class ScanThread(QThread):
    """Background scanning thread"""
    
    results_ready = pyqtSignal(list)
    progress_update = pyqtSignal(int)
    
    def __init__(self, plugin):
        super().__init__()
        self.plugin = plugin
        self.running = False
    
    def run(self):
        """Run background scanning"""
        self.running = True
        
        while self.running:
            try:
                # Perform scan
                results = self._perform_scan()
                self.results_ready.emit(results)
                
                # Update progress
                self.progress_update.emit(100)
                
                # Wait before next scan
                self.msleep(5000)  # 5 second interval
                
            except Exception as e:
                self.plugin.error_occurred.emit(str(e))
                break
    
    def stop(self):
        """Stop background scanning"""
        self.running = False
        self.wait()

# In your plugin class:
def start_scan(self, **kwargs) -> bool:
    """Start background scanning"""
    if not self._is_scanning:
        self.scan_thread = ScanThread(self)
        self.scan_thread.results_ready.connect(self._on_results_ready)
        self.scan_thread.progress_update.connect(self.scan_progress.emit)
        self.scan_thread.start()
        
        self._is_scanning = True
        self.scan_started.emit()
        return True
    
    return False
```

## Package-Based Plugins

For complex plugins, you can create a package structure:

```
plugins/
├── my_complex_plugin/
│   ├── __init__.py
│   ├── main_window.py
│   ├── scan_engine.py
│   ├── analysis_tools.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── dialogs.py
│   │   └── widgets.py
│   └── data/
│       ├── config.json
│       └── templates/
```

`plugins/my_complex_plugin/__init__.py`:
```python
"""
Complex WiFi Analysis Plugin Package
"""

from .main_plugin import ComplexAnalysisPlugin

# Plugin entry point
def get_plugin_class():
    return ComplexAnalysisPlugin

__all__ = ['ComplexAnalysisPlugin']
```

## Best Practices

### 1. Error Handling

```python
def start_scan(self, **kwargs) -> bool:
    """Start scanning with proper error handling"""
    try:
        # Validate prerequisites
        if not self._validate_interface():
            self.error_occurred.emit("No valid wireless interface found")
            return False
        
        # Start scanning
        self._is_scanning = True
        self.scan_started.emit()
        
        # Perform scan operations
        results = self._perform_scan()
        
        # Process and emit results
        self._process_results(results)
        
        return True
        
    except PermissionError:
        self.error_occurred.emit("Root privileges required for scanning")
        return False
    except Exception as e:
        self.error_occurred.emit(f"Scan failed: {str(e)}")
        return False
    finally:
        self._is_scanning = False
```

### 2. Resource Management

```python
def cleanup(self):
    """Cleanup resources when plugin is unloaded"""
    try:
        # Stop any running operations
        if self._is_scanning:
            self.stop_scan()
        
        # Close file handles
        if hasattr(self, 'log_file'):
            self.log_file.close()
        
        # Stop background threads
        if hasattr(self, 'scan_thread'):
            self.scan_thread.stop()
        
        # Clear data structures
        self._scan_results.clear()
        
    except Exception as e:
        # Log cleanup errors but don't raise
        print(f"Cleanup error in {self.metadata.name}: {e}")
```

### 3. Configuration Validation

```python
def configure(self, config: Dict[str, Any]) -> bool:
    """Configure with validation"""
    try:
        # Validate required settings
        required_keys = ['interface', 'scan_interval']
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Missing required setting: {key}")
        
        # Validate value ranges
        scan_interval = config['scan_interval']
        if not isinstance(scan_interval, int) or scan_interval < 1:
            raise ValueError("scan_interval must be a positive integer")
        
        # Apply configuration
        self._config = config
        self._apply_config()
        
        return True
        
    except Exception as e:
        self.error_occurred.emit(f"Configuration error: {e}")
        return False
```

### 4. Thread Safety

```python
from PyQt5.QtCore import QMutex

class ThreadSafePlugin(WiFiPlugin):
    """Plugin with thread-safe operations"""
    
    def __init__(self):
        super().__init__()
        self._mutex = QMutex()
        self._scan_results = []
    
    def get_scan_results(self) -> List[WiFiScanResult]:
        """Thread-safe access to scan results"""
        self._mutex.lock()
        try:
            return self._scan_results.copy()
        finally:
            self._mutex.unlock()
    
    def _update_results(self, new_results):
        """Thread-safe update of scan results"""
        self._mutex.lock()
        try:
            self._scan_results = new_results
        finally:
            self._mutex.unlock()
```

## Deployment

### 1. Plugin Distribution

Package your plugin for distribution:

```bash
# Create plugin package
mkdir my_plugin_package
cp my_custom_plugin.py my_plugin_package/
cp README.md my_plugin_package/
cp requirements.txt my_plugin_package/

# Create installer script
cat > my_plugin_package/install.py << 'EOF'
#!/usr/bin/env python3
"""Plugin installer script"""
import shutil
import sys
from pathlib import Path

def install_plugin():
    # Find airradar installation
    airradar_dir = Path.cwd()
    plugins_dir = airradar_dir / "plugins"
    
    if not plugins_dir.exists():
        print("Error: plugins directory not found")
        return False
    
    # Copy plugin file
    plugin_file = Path("my_custom_plugin.py")
    if plugin_file.exists():
        shutil.copy2(plugin_file, plugins_dir)
        print(f"Installed plugin to {plugins_dir}")
        return True
    else:
        print("Error: plugin file not found")
        return False

if __name__ == '__main__':
    install_plugin()
EOF
```

### 2. Plugin Registration

For automatic registration, ensure your plugin follows the naming convention and includes the entry point:

```python
# At the end of your plugin file
def get_plugin_class():
    """Plugin entry point for automatic discovery"""
    return YourPluginClass

# Optional: Plugin information for package managers
PLUGIN_INFO = {
    'name': 'My Custom Plugin',
    'version': '1.0.0',
    'class': 'MyCustomPlugin',
    'file': __file__
}
```

## Troubleshooting

### Common Issues

1. **Plugin Not Discovered**
   - Check file is in `plugins/` directory
   - Ensure `get_plugin_class()` function exists
   - Verify plugin inherits from `WiFiPlugin`

2. **Import Errors**
   - Check plugin dependencies are installed
   - Verify Python path includes parent directory
   - Ensure core modules are accessible

3. **Signal Connection Issues**
   - Verify signal names match exactly
   - Check signal/slot parameter types
   - Ensure signals are emitted from correct thread

4. **Window Creation Fails**
   - Check PyQt5 is properly installed
   - Verify parent/child widget relationships
   - Ensure proper cleanup of previous instances

### Debug Mode

Enable debug logging for plugin development:

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class DebugPlugin(WiFiPlugin):
    def start_scan(self, **kwargs):
        logger.debug(f"Starting scan with args: {kwargs}")
        # ... rest of implementation
```

## Conclusion

The plugin system provides a powerful and flexible way to extend the WiFi Security Radar Suite. By following this guide, you can create professional-grade WiFi monitoring tools that integrate seamlessly with the existing framework.

Key takeaways:
- Inherit from `WiFiPlugin` and implement required methods
- Use standardized `WiFiScanResult` format for consistency
- Emit appropriate signals for UI integration
- Handle errors gracefully and cleanup resources
- Follow naming conventions for automatic discovery
- Test thoroughly before deployment

For more examples, see the existing plugins in the `plugins/` directory.