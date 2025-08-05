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

### 1. Navigation Enhanced WiFi Radar (wifi_radar_nav_enhanced.py)
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

### 2. Modern Penetration Testing Radar (wifi_pentest_radar_modern.py)
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
├── main_launcher.py              # Main application launcher
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

### Method 1: Main Launcher (Recommended)
```bash
sudo python3 main_launcher.py
```
- Choose between Navigation Enhanced or Modern Penetration Testing interface
- Professional launcher with program selection

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

### Enhanced Features (v5.0)
- `Ctrl+G`: Toggle Real-time Graphs
- `Ctrl+E`: Export Data
- `Ctrl+Alt+A`: Accessibility Settings
- `F1`: Accessibility Help
- `Ctrl+Shift+S`: Toggle Screen Reader Mode
- `Ctrl+Shift+H`: Toggle High Contrast Mode

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

## Modern Features (v5.0)

### Enhanced GUI and Usability
- **Real-time Monitoring Dashboard**: Live graphs for signal strength, network activity, and security trends
- **Professional Export System**: Generate CSV, JSON, and styled HTML reports
- **Accessibility Features**: High contrast mode, font scaling (50%-300%), enhanced keyboard navigation
- **Multi-language Support**: 11 languages with runtime switching (English, Spanish, French, German, etc.)
- **Advanced Theme System**: 6+ built-in themes with complete customization options
- **Enhanced Navigation**: Improved menu structure, keyboard shortcuts, and spatial navigation

### Enhanced Visualization
- Multiple radar modes (Grid/Polar/Heatmap)
- Intelligent AP positioning to prevent overlapping
- Modern animations and smooth transitions
- Professional color schemes and gradients
- Real-time data visualization with customizable update intervals

### Advanced Analysis
- Enhanced distance calculation algorithms
- Comprehensive vendor identification
- Multi-factor vulnerability scoring
- Detailed attack vector analysis
- Professional reporting with export capabilities

### User Experience
- Modern Material Design interface
- Copy functionality for all analysis results
- Professional dialog systems
- Responsive layout design
- Comprehensive accessibility support

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
- **THEMING_AND_VIEWS.md** - Comprehensive theming and view modes guide
- **PROJECT_CLEANUP_SUMMARY.md** - Project organization and cleanup details
- **old/** - Previous versions and deprecated documentation
- **backup/** - Duplicate files from project cleanup

## Version History

- **v5.0** - Modern radar v4.0, project cleanup, fixed drawEllipse issues
- **v4.0** - Navigation enhanced interface with view modes
- **v3.0** - Penetration testing radar with vulnerability analysis
- **v2.0** - UI improvements and theming enhancements
- **v1.0** - Initial WiFi radar implementation

## Recent Updates (v5.0)

### Bug Fixes
- ✅ Fixed TypeError in `drawEllipse` methods by converting float to int
- ✅ Resolved radar visualization crashes in modern interface
- ✅ Updated main launcher to use modern pentest radar

### Major GUI and Usability Improvements
- ✅ **Real-time Graphs**: Signal strength, network activity, and security trend monitoring
- ✅ **Enhanced Export**: CSV, JSON, and professional HTML reports with styling
- ✅ **Accessibility Features**: High contrast mode, font scaling, keyboard navigation
- ✅ **Multi-language Support**: 11 languages with translation framework
- ✅ **Advanced Theming**: 6+ customizable themes with color/layout controls
- ✅ **Enhanced Navigation**: Improved menu structure and keyboard shortcuts

### Core Improvements
- ✅ Enhanced project organization with backup folder
- ✅ Modern radar with advanced visualization modes
- ✅ Professional Material Design interface elements
- ✅ Comprehensive analysis report generation
- ✅ Copy functionality for all analysis results
- ✅ Modular feature integration system

## Legal Notice

This tool is designed for **educational purposes** and **authorized security testing** only. Users are responsible for ensuring compliance with applicable laws and regulations. Unauthorized access to WiFi networks is illegal in most jurisdictions.

**Use responsibly and ethically.**

## Contributing

Contributions are welcome! Please ensure any modifications maintain the professional theming and security focus of the project.

---

**© 2025 WiFi Security Tools - Professional Hacker-Style Interface with Modern Visualization**
