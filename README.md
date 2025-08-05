# WiFi Security Radar Suite v5.0

## Professional WiFi Security Analysis Tools

A comprehensive suite of WiFi security analysis tools featuring modern interfaces, comprehensive theming, and advanced penetration testing capabilities.

### Quick Start

```bash
# Install dependencies
sudo apt update
sudo apt install python3-pyqt5 python3-pyqt5-dev wireless-tools iw

# Install Python dependencies
pip install -r requirements.txt

# Launch the main suite (requires root for WiFi scanning)
sudo python3 main_launcher.py
```

## Available Tools

The suite now features a **modular plugin architecture** that enables easy addition and removal of WiFi monitoring tools.

### Plugin-Based Architecture
- **Automatic Plugin Discovery**: Dynamic detection and loading of plugins
- **Standardized Interfaces**: Consistent API for all WiFi monitoring tools
- **Easy Extension**: Add new tools without modifying core code
- **Hot Loading**: Load/unload plugins at runtime

### Core Plugins

### 1. Navigation Enhanced WiFi Radar Plugin
- **Modern navigation bar interface** with professional menu system
- **Multiple view modes**: Compact (800x500), Normal (1400x800), Fullscreen
- **Comprehensive hacker-style theming** with Matrix green accents
- **Scrollable analysis panels** with enhanced readability
- **Professional status bar** with real-time information
- **Zoom functionality** and keyboard shortcuts

**Features:**
- Complete UI theming consistency
- Dynamic view mode switching
- Comprehensive keyboard shortcuts
- Enhanced dialog systems
- Professional status indicators

### 2. Penetration Testing Radar Plugin
- **Modern radar display v4.0** with advanced visualization modes
- **Multiple visualization types**: Grid, Polar, and Heatmap modes
- **Advanced vulnerability scoring** with comprehensive threat analysis
- **Enhanced distance calculation** using sophisticated algorithms
- **Professional modern UI** with Material Design elements
- **Copy functionality** for analysis results and reports

**Features:**
- Industry-level vulnerability assessment
- Real-time radar visualization with animations
- Intelligent AP positioning to prevent overlapping
- Advanced threat level classification
- Modern professional interface design
- Comprehensive analysis report generation

## Project Structure

```
wifiMap/
├── main_launcher_plugin.py        # Plugin-based launcher (NEW)
├── main_launcher.py               # Original launcher (preserved)
├── core/                          # Plugin framework (NEW)
│   ├── plugin_base.py            # Base classes and interfaces
│   └── plugin_manager.py         # Plugin discovery and management
├── plugins/                       # Plugin directory (NEW)
│   ├── navigation_enhanced.py    # Navigation enhanced plugin
│   └── penetration_testing.py   # Penetration testing plugin
├── docs/                          # Documentation (NEW)
│   ├── PLUGIN_DEVELOPMENT.md    # Plugin development guide
│   └── MODULAR_ARCHITECTURE.md  # Architecture overview
├── wifi_radar_nav_enhanced.py    # Navigation enhanced interface
├── wifi_pentest_radar_modern.py  # Modern penetration testing radar v4.0
├── requirements.txt              # Python dependencies
├── settings.json                 # Application settings
├── README.md                     # This documentation
├── THEMING_AND_VIEWS.md         # Theming and view modes guide
├── modern_styles.qss            # Modern UI stylesheet
├── old/                         # Previous versions and deprecated files
├── backup/                      # Duplicate files from cleanup
└── .venv/                       # Virtual environment (optional)
```

## System Requirements

### Operating System
- Linux (Ubuntu/Debian/Kali recommended)
- Root privileges required for WiFi scanning

### Dependencies
- Python 3.6+
- PyQt5
- Wireless tools (iw, iwlist)

### Installation Commands

```bash
# Ubuntu/Debian
sudo apt install python3-pyqt5 python3-pyqt5-dev wireless-tools iw

# Kali Linux
sudo apt install python3-pyqt5 wireless-tools iw

# Arch Linux
sudo pacman -S python-pyqt5 wireless_tools iw

# Python packages
pip install PyQt5
```

## Usage

### Method 1: Plugin-Based Launcher (Recommended)
```bash
sudo python3 main_launcher_plugin.py
```
- **New modular architecture** with plugin system
- Automatic plugin discovery and loading
- Enhanced interface with plugin details and capabilities
- Fallback support for direct tool launch

### Method 2: Original Launcher
```bash
sudo python3 main_launcher.py
```
- Choose between Navigation Enhanced or Modern Penetration Testing interface
- Professional launcher with program selection (preserved for compatibility)

### Method 2: Direct Launch
```bash
# Navigation Enhanced Interface
sudo python3 wifi_radar_nav_enhanced.py

# Modern Penetration Testing Radar
sudo python3 wifi_pentest_radar_modern.py
```

## Keyboard Shortcuts

### Navigation Enhanced Interface
- `Ctrl+1`: Compact Mode (800x500)
- `Ctrl+2`: Normal Mode (1400x800)  
- `F11`: Fullscreen Mode
- `F5`: Refresh Scan
- `Ctrl+N`: New Scan
- `Ctrl+S`: Save Results
- `Ctrl++`: Zoom In
- `Ctrl+-`: Zoom Out
- `Ctrl+Q`: Exit

### Modern Penetration Testing Radar
- `Ctrl+1`: Compact Mode (800x500)
- `Ctrl+2`: Normal Mode (1400x800)
- `F11`: Fullscreen Mode
- `Ctrl+N`: New Scan
- `Ctrl+S`: Save Results
- `F5`: Manual Scan
- `Spacebar`: Start/Stop Scanning
- `Mouse Click`: Select Access Point
- `Scroll Wheel`: Adjust Range
- `Ctrl+Q`: Exit

## Modern Radar Visualization Modes

### Grid Mode
- **Organized grid layout** preventing AP overlaps
- **Professional grid lines** with distance markers
- **Intelligent positioning** based on signal strength and distance

### Polar Mode
- **Traditional radar sweep** with animated visualization
- **Distance rings** with labeled ranges
- **Angle-based positioning** with sweep animation

### Heatmap Mode
- **Signal strength visualization** with colored gradients
- **Threat level indicators** with color coding
- **Cluster analysis** based on signal patterns

## Theming System

Both interfaces feature comprehensive **professional hacker-style theming**:

- **Matrix Green Color Scheme** (#00FF00) with dark backgrounds
- **JetBrains Mono Typography** for authentic monospace appearance
- **Consistent UI Elements** across all components
- **Professional Hover Effects** and interactive feedback
- **Custom Styled Components** (scrollbars, buttons, dialogs)
- **Modern Material Design** elements in the radar interface

See `THEMING_AND_VIEWS.md` for detailed theming documentation.

## Security Features

### WiFi Analysis
- Real-time access point detection
- Security protocol identification (Open/WEP/WPA/WPA2/WPA3)
- Signal strength analysis with advanced calculations
- Distance calculation using enhanced algorithms
- Vendor identification with extensive OUI database

### Advanced Vulnerability Assessment
- Automated security scoring with multi-factor analysis
- Attack vector identification with tool recommendations
- Threat level classification (LOW/MEDIUM/HIGH/CRITICAL)
- Confidence rating system
- Comprehensive analysis report generation

### Professional Reporting
- Detailed target analysis with technical specifications
- Vulnerability summaries with scoring explanations
- Attack methodology suggestions with tool recommendations
- Security recommendations based on threat level
- Copy functionality for easy report sharing

## Modern Features (v5.0 - Modular Architecture)

### Plugin System
- **Modular Design**: Easy addition and removal of WiFi monitoring tools
- **Automatic Discovery**: Dynamic plugin detection and loading
- **Standardized Interface**: Consistent API for all plugins
- **Hot Loading**: Runtime plugin management without restart
- **Dependency Validation**: Automatic checking of plugin requirements

### Enhanced Launcher
- **Plugin Browser**: Visual interface for selecting and launching plugins
- **Plugin Details**: Comprehensive information about each plugin's capabilities
- **Fallback Support**: Graceful handling when plugin system is unavailable
- **Status Monitoring**: Real-time plugin status and error reporting

### Developer Experience
- **Plugin Development Kit**: Complete framework for creating new tools
- **Documentation**: Comprehensive guides for plugin development
- **Testing Framework**: Automated testing for plugin functionality
- **Template System**: Quick-start templates for new plugins

### Enhanced Visualization (v4.0 Continued)
- Multiple radar modes (Grid/Polar/Heatmap)
- Intelligent AP positioning to prevent overlapping
- Modern animations and smooth transitions
- Professional color schemes and gradients

### Advanced Analysis (Continued)
- Enhanced distance calculation algorithms
- Comprehensive vendor identification
- Multi-factor vulnerability scoring
- Detailed attack vector analysis

### User Experience (Enhanced)
- Modern Material Design interface
- Copy functionality for all analysis results
- Professional dialog systems
- Responsive layout design
- Plugin-based extensibility

## Troubleshooting

### Common Issues

**"No wireless interfaces detected"**
```bash
# Check available interfaces
iwconfig
iw dev

# Ensure interface is up
sudo ip link set wlan0 up
```

**"Permission denied" errors**
```bash
# Run with root privileges
sudo python3 main_launcher.py
```

**Missing dependencies**
```bash
# Install all required packages
sudo apt install python3-pyqt5 python3-pyqt5-dev wireless-tools iw
pip install -r requirements.txt
```

**Interface busy/scanning fails**
```bash
# Stop NetworkManager temporarily
sudo systemctl stop NetworkManager
sudo systemctl stop wpa_supplicant

# Run the application
sudo python3 main_launcher.py

# Restart NetworkManager after use
sudo systemctl start NetworkManager
```

**TypeError in radar visualization**
- This has been fixed in the modern version by converting float values to integers in drawEllipse calls

## Documentation

- **README.md** - Main documentation (this file)
- **docs/PLUGIN_DEVELOPMENT.md** - Comprehensive plugin development guide
- **docs/MODULAR_ARCHITECTURE.md** - Architecture overview and design decisions
- **THEMING_AND_VIEWS.md** - Comprehensive theming and view modes guide
- **PROJECT_CLEANUP_SUMMARY.md** - Project organization and cleanup details
- **old/** - Previous versions and deprecated documentation
- **backup/** - Duplicate files from project cleanup

## Developing Plugins

The modular architecture enables easy development of new WiFi monitoring tools. See `docs/PLUGIN_DEVELOPMENT.md` for a comprehensive guide including:

- Plugin architecture overview
- Step-by-step plugin creation
- API reference and examples
- Testing and deployment
- Best practices and troubleshooting

### Quick Plugin Example

```python
from core.plugin_base import WiFiPlugin, PluginMetadata

class MyCustomPlugin(WiFiPlugin):
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="My Custom Tool",
            version="1.0.0",
            description="Custom WiFi monitoring tool",
            author="Your Name",
            capabilities=["wifi_scanning", "custom_analysis"]
        )
    
    def create_main_window(self):
        return MyCustomMainWindow()
    
    # Implement other required methods...

def get_plugin_class():
    return MyCustomPlugin
```

## Version History

- **v5.0** - **Modular Architecture**: Plugin system, automatic discovery, enhanced launcher
- **v4.0** - Modern radar v4.0, project cleanup, fixed drawEllipse issues
- **v3.0** - Navigation enhanced interface with view modes
- **v2.0** - Penetration testing radar with vulnerability analysis
- **v1.0** - UI improvements and theming enhancements
- **v0.1** - Initial WiFi radar implementation

## Recent Updates (v5.0 - Modular Architecture)

### New Features
- ✅ **Plugin System**: Modular architecture for extensible WiFi monitoring tools
- ✅ **Plugin Manager**: Automatic discovery, loading, and management of plugins
- ✅ **Enhanced Launcher**: Modern interface with plugin browser and details
- ✅ **Developer Framework**: Complete plugin development kit with documentation
- ✅ **Testing Suite**: Comprehensive testing for plugin system functionality

### Architecture Improvements
- ✅ **Standardized Interfaces**: Consistent API for all WiFi monitoring tools
- ✅ **Loose Coupling**: Plugin system with abstract base classes
- ✅ **Error Isolation**: Plugin errors don't crash the entire system
- ✅ **Hot Loading**: Runtime plugin management without restart
- ✅ **Backward Compatibility**: All original functionality preserved

### Developer Experience
- ✅ **Plugin Development Guide**: Comprehensive documentation with examples
- ✅ **Template System**: Quick-start templates for new plugins
- ✅ **Automatic Discovery**: No manual registration required
- ✅ **Dependency Validation**: Automatic checking of plugin requirements
- ✅ **Testing Framework**: Automated testing for plugin functionality

## Legal Notice

This tool is designed for **educational purposes** and **authorized security testing** only. Users are responsible for ensuring compliance with applicable laws and regulations. Unauthorized access to WiFi networks is illegal in most jurisdictions.

**Use responsibly and ethically.**

## Contributing

Contributions are welcome! This project follows a formal code review process to ensure quality and security.

### Code Review Process

- **Official Reviewer**: All major feature and improvement pull requests are reviewed by @github/copilot
- **Review Standards**: We maintain high standards for code quality, security, and documentation
- **Community Involvement**: Community feedback and contributions are encouraged and valued

### Getting Started

1. Read our [Contributing Guidelines](CONTRIBUTING.md)
2. Fork the repository and create a feature branch
3. Make your changes following our coding standards
4. Submit a pull request using the provided template
5. Participate in the code review process

### Review Standards

All pull requests must meet the following criteria:
- ✅ Code quality and style consistency
- ✅ Security considerations addressed
- ✅ Adequate documentation and comments
- ✅ Appropriate test coverage
- ✅ No breaking changes without justification

Please ensure any modifications maintain the professional theming and security focus of the project.

---

**© 2025 WiFi Security Tools - Professional Hacker-Style Interface with Modern Visualization**
