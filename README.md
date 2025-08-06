# WiFi Security Radar Suite v5.0

## Professional WiFi Security Analysis Tools

A comprehensive suite of WiFi security analysis tools featuring modern interfaces, comprehensive theming, and advanced penetration testing capabilities.

### Quick Start

#### For Experienced Users
```bash
# Install dependencies
sudo apt update
sudo apt install python3-pyqt5 python3-pyqt5-dev wireless-tools iw

# Install Python dependencies
pip install -r requirements.txt

# Launch the main suite (requires root for WiFi scanning)
sudo python3 main_launcher.py
```

#### Detailed First-Time Setup

1. **Verify Prerequisites**
   ```bash
   # Check Python version (should be 3.6+)
   python3 --version
   
   # Check if wireless interface exists
   iwconfig
   # or
   iw dev
   ```

2. **Prepare Wireless Interface** 
   ```bash
   # Identify your wireless interface (usually wlan0, wlp2s0, etc.)
   ip link show
   
   # Ensure interface is up
   sudo ip link set wlan0 up
   
   # Optional: Test basic scanning capability
   sudo iw dev wlan0 scan | head -20
   ```

3. **Launch Application**
   ```bash
   # Method 1: Use the main launcher (recommended)
   sudo python3 main_launcher.py
   
   # Method 2: Launch specific interface directly
   sudo python3 wifi_radar_nav_enhanced.py        # Navigation-enhanced UI
   sudo python3 wifi_pentest_radar_modern.py      # Modern penetration testing radar
   ```

4. **First Run Checklist**
   - ✅ Application launches without errors
   - ✅ Wireless interface is detected
   - ✅ Initial WiFi scan completes
   - ✅ UI themes load correctly
   - ✅ Access points are displayed in radar view

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

## Prerequisites and System Requirements

### Operating System Support
- **Primary**: Linux distributions (Ubuntu 18.04+, Debian 10+, Kali Linux 2020.1+)
- **Tested On**: Ubuntu 20.04/22.04, Debian 11/12, Kali Linux, Arch Linux
- **Note**: Windows and macOS are not supported due to wireless interface requirements

### Required Permissions
- **Root/Sudo Access**: Required for wireless interface scanning and monitoring
- **Network Interface Access**: Ability to put wireless interfaces in monitor mode
- **System Commands**: Access to `iw`, `iwlist`, and related wireless tools

### Hardware Requirements
- **Wireless Interface**: 802.11 compatible wireless adapter
- **Monitor Mode Support**: Wireless adapter that supports monitor mode (recommended)
- **Memory**: Minimum 512MB RAM (1GB+ recommended for large networks)
- **Storage**: 100MB free space for application and logs

### Software Dependencies

#### System Packages
| Package | Version | Purpose | Installation |
|---------|---------|---------|-------------|
| Python 3 | 3.6+ (3.8+ recommended) | Core runtime | `sudo apt install python3` |
| PyQt5 Development | 5.15+ | GUI framework | `sudo apt install python3-pyqt5-dev` |
| Wireless Tools | Latest | WiFi scanning | `sudo apt install wireless-tools` |
| iw | Latest | Modern WiFi interface control | `sudo apt install iw` |

#### Python Packages
| Package | Version | Purpose |
|---------|---------|---------|
| PyQt5 | ≥5.15.0 | GUI application framework |
| requests | ≥2.25.0 | HTTP requests for vendor lookups |

## Installation Guide

### Option 1: Automated Installation (Recommended)

Use the provided installation script for automatic setup:

```bash
# 1. Clone the repository
git clone https://github.com/vinothvbt/airradar.git
cd airradar

# 2. Run the automated installer
chmod +x install.sh
./install.sh

# 3. Follow the prompts and test the installation
```

The installer will:
- ✅ Detect your operating system automatically
- ✅ Install all required system packages
- ✅ Set up Python dependencies
- ✅ Check wireless interface availability  
- ✅ Test the complete installation
- ✅ Provide troubleshooting guidance if issues occur

### Option 2: Manual Installation

#### Quick Installation
```bash
# 1. Update package manager
sudo apt update && sudo apt upgrade -y

# 2. Install system dependencies
sudo apt install python3 python3-pip python3-pyqt5 python3-pyqt5-dev wireless-tools iw -y

# 3. Clone the repository
git clone https://github.com/vinothvbt/airradar.git
cd airradar

# 4. Install Python dependencies
pip3 install -r requirements.txt

# 5. Test installation
python3 quick_test.py

# 6. Launch application (requires root)
sudo python3 main_launcher.py
```

#### Virtual Environment Installation

```bash
# 1. Install system dependencies
sudo apt update
sudo apt install python3 python3-pip python3-venv python3-pyqt5-dev wireless-tools iw -y

# 2. Clone and setup
git clone https://github.com/vinothvbt/airradar.git
cd airradar

# 3. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 4. Install Python dependencies
pip install -r requirements.txt

# 5. Test installation
python3 quick_test.py

# 6. Launch application (requires root, but keep venv active)
sudo venv/bin/python3 main_launcher.py
```

### Platform-Specific Installation

#### Ubuntu/Debian Systems
```bash
# Standard installation
sudo apt update
sudo apt install python3-pyqt5 python3-pyqt5-dev wireless-tools iw aircrack-ng -y
pip3 install -r requirements.txt
```

#### Kali Linux
```bash
# Most tools pre-installed
sudo apt update
sudo apt install python3-pyqt5 wireless-tools iw -y
pip3 install -r requirements.txt
```

#### Arch Linux / Manjaro
```bash
# Using pacman
sudo pacman -S python python-pyqt5 wireless_tools iw
pip install -r requirements.txt
```

#### Fedora / CentOS / RHEL
```bash
# Using dnf/yum
sudo dnf install python3-qt5 wireless-tools iw
# or: sudo yum install python3-qt5 wireless-tools iw
pip3 install -r requirements.txt
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
#### Navigation Enhanced Interface
```bash
sudo python3 wifi_radar_nav_enhanced.py
```
**Best for:**
- General WiFi network discovery and analysis
- Professional reporting and documentation
- Multi-view mode operation (perfect for presentations)
- Educational demonstrations

**Expected Output:**
```
2025-08-05 10:30:15,025 - INFO - Configuration loaded from config.json
2025-08-05 10:30:15,025 - INFO - Loaded 5 security profiles
2025-08-05 10:30:15,030 - INFO - Wireless interface wlan0 detected
2025-08-05 10:30:15,035 - INFO - Starting WiFi scan...
2025-08-05 10:30:18,125 - INFO - Scan complete: 12 access points found
```

#### Modern Penetration Testing Radar
```bash
sudo python3 wifi_pentest_radar_modern.py
```
**Best for:**
- Security assessments and penetration testing
- Advanced vulnerability analysis
- Threat level evaluation
- Professional security audits

**Expected Output:**
```
2025-08-05 10:30:20,125 - INFO - Security engine initialized
2025-08-05 10:30:20,130 - INFO - Vendor database loaded: 24,000+ entries
2025-08-05 10:30:20,135 - INFO - Modern radar visualization ready
2025-08-05 10:30:25,200 - INFO - Vulnerability assessment complete: 3 HIGH, 5 MEDIUM threats detected
```

### Common Usage Scenarios

#### Scenario 1: Network Security Assessment
```bash
# 1. Launch penetration testing radar
sudo python3 wifi_pentest_radar_modern.py

# 2. Expected workflow:
#    - Automatic scan starts
#    - Radar displays APs with threat levels
#    - Click on high-threat APs for detailed analysis
#    - Copy vulnerability reports for documentation

# 3. Key features to use:
#    - Heatmap mode for threat visualization
#    - Vulnerability scoring system
#    - Attack vector recommendations
```

#### Scenario 2: WiFi Site Survey
```bash
# 1. Launch navigation enhanced interface
sudo python3 wifi_radar_nav_enhanced.py

# 2. Recommended settings:
#    - Use Normal mode (1400x800) for detailed view
#    - Enable continuous scanning
#    - Document signal strengths and coverage areas

# 3. Export options:
#    - Save scan results to file
#    - Generate professional reports
#    - Export AP lists with technical details
```

#### Scenario 3: Troubleshooting Connectivity
```bash
# 1. Stop NetworkManager temporarily (if needed)
sudo systemctl stop NetworkManager

# 2. Launch application for clean scanning
sudo python3 main_launcher.py

# 3. Analysis workflow:
#    - Scan for interfering networks
#    - Check channel congestion
#    - Analyze signal strengths
#    - Identify optimal channels

# 4. Restore normal networking
sudo systemctl start NetworkManager
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

## Screenshots and Visual Examples

### Main Launcher Interface
```
┌─────────────────────────────────────────────────────────────┐
│ WiFi Security Radar Suite v5.0 - Professional Launcher     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [📡 Navigation Enhanced WiFi Radar]                       │
│   • Modern navigation bar interface                         │
│   • Multiple view modes and professional theming            │
│   • Comprehensive analysis and reporting                    │
│                                                             │
│  [🔍 Modern Penetration Testing Radar]                     │
│   • Advanced vulnerability assessment                       │
│   • Modern radar visualization with threat levels           │
│   • Professional security analysis tools                    │
│                                                             │
│  [⚙️  Settings & Configuration]    [❓ Help & About]       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Navigation Enhanced Interface - Main View
```
┌─────────────────────────────────────────────────────────────────────────┐
│ File Edit View Scan Tools Help                     [Compact|Normal|Full] │
├─────────────────────────────────────────────────────────────────────────┤
│ ┌─────────────────┐ ┌─────────────────────────────────────────────────┐ │
│ │  WiFi Radar     │ │ Access Point Details                            │ │
│ │                 │ │ ┌─────────────────────────────────────────────┐ │ │
│ │    📡 AP1       │ │ │ SSID: "HomeNetwork_5G"                      │ │ │
│ │      📶 AP2     │ │ │ BSSID: 00:11:22:33:44:55                   │ │ │
│ │  📡     AP3     │ │ │ Channel: 149 (5.745 GHz)                   │ │ │
│ │        📶 AP4   │ │ │ Security: WPA3-Personal                     │ │ │
│ │    📡 AP5       │ │ │ Signal: -45 dBm (Excellent)                 │ │ │
│ │                 │ │ │ Vendor: Netgear Inc.                        │ │ │
│ │     [Scan]      │ │ │ Distance: ~12 meters                        │ │ │
│ └─────────────────┘ │ │ Security Score: 85/100 (Good)               │ │ │
│                     │ └─────────────────────────────────────────────┘ │ │
│                     └─────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────────┤
│ Status: Interface wlan0 | Mode: Normal | APs Found: 12 | Last Scan: 10:30 │
└─────────────────────────────────────────────────────────────────────────┘
```

### Modern Penetration Testing Radar - Threat View
```
┌─────────────────────────────────────────────────────────────────────────┐
│ WiFi Penetration Testing Radar v4.0                [Grid|Polar|Heatmap] │
├─────────────────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────┐ ┌─────────────────────────────────────┐ │
│ │     Radar Display           │ │ Vulnerability Analysis              │ │
│ │                             │ │                                     │ │
│ │        🔴 HIGH              │ │ Target: "OpenWiFi_Guest"            │ │
│ │         THREAT              │ │ Threat Level: 🔴 CRITICAL          │ │
│ │                             │ │                                     │ │
│ │   🟡     🟢     🟡         │ │ Vulnerabilities Detected:           │ │
│ │  MED     LOW    MED         │ │ • No encryption (Open network)     │ │
│ │                             │ │ • Default configuration detected    │ │
│ │       🟡 MED                │ │ • Weak signal isolation            │ │
│ │                             │ │                                     │ │
│ │  [Grid Mode Active]         │ │ Recommended Tools:                  │ │
│ └─────────────────────────────┘ │ • aircrack-ng (monitoring)         │ │
│                                 │ • Wireshark (packet analysis)      │ │
│                                 │ • Evil Twin attack possible         │ │
│                                 │                                     │ │
│                                 │ [Copy Report] [Save Analysis]       │ │
│                                 └─────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────────┤
│ Scanning: Active | Threats: 3 HIGH, 5 MED, 8 LOW | Range: 100m | Auto   │
└─────────────────────────────────────────────────────────────────────────┘
```

### Key Visual Features

#### Color Coding System
- **🔴 Red (Critical/High)**: Open networks, vulnerable configurations, high-value targets
- **🟡 Yellow (Medium)**: Weak encryption, default settings, moderate threats  
- **🟢 Green (Low)**: Strong encryption, proper configuration, minimal threats
- **⚫ Gray (Unknown)**: Insufficient data, hidden networks, analysis pending

#### Interface Themes
- **Hacker-Style Dark Theme**: Professional black background with Matrix green accents
- **Typography**: JetBrains Mono for authentic monospace appearance
- **Interactive Elements**: Hover effects, smooth animations, responsive design
- **Status Indicators**: Real-time updates, progress bars, connection status

#### Radar Visualization Modes

1. **Grid Mode**: Organized layout preventing AP overlap, clear positioning
2. **Polar Mode**: Traditional radar sweep with distance rings and angles  
3. **Heatmap Mode**: Signal strength and threat visualization with gradients

*Note: These are ASCII art representations of the actual interfaces. Actual screenshots showing these interfaces in action are available in the project wiki and documentation.*

## Radar Visualization Modes

The Modern Penetration Testing Radar offers three advanced visualization modes for different analysis needs:

### Grid Mode
- **Organized Layout**: Intelligent grid positioning prevents access point overlap
- **Distance Markers**: Professional grid lines with labeled distance measurements
- **Signal Mapping**: Access points positioned based on signal strength and calculated distance
- **Clear Overview**: Perfect for documenting network layouts and coverage areas
- **Professional Presentation**: Ideal for reports and client presentations

### Polar Mode  
- **Traditional Radar**: Classic radar sweep animation with rotating beam
- **Distance Rings**: Concentric circles with labeled range measurements
- **Angular Positioning**: APs positioned by angle and distance from center
- **Sweep Animation**: Real-time radar sweep effect with trail visualization
- **Immersive Experience**: Engaging visualization for live demonstrations

### Heatmap Mode
- **Signal Strength Visualization**: Color-coded signal strength gradients
- **Threat Level Indicators**: Visual threat classification with color coding
- **Cluster Analysis**: Identifies network clusters and interference patterns
- **Density Mapping**: Shows areas of high network concentration
- **Quick Assessment**: Rapid visual identification of security concerns

### Interactive Features

#### User Controls
- **Mode Switching**: Seamless switching between visualization modes
- **Zoom Control**: Mouse wheel zoom for detailed inspection
- **Click Selection**: Click any access point for detailed analysis
- **Range Adjustment**: Dynamic range scaling for optimal view
- **Auto-Refresh**: Continuous scanning with real-time updates

#### Visual Enhancements
- **Smooth Animations**: Professional transitions and hover effects
- **Color Coding**: Consistent threat level color scheme throughout
- **Modern UI**: Material Design elements with dark theme
- **Responsive Design**: Adapts to different screen sizes and resolutions
- **High DPI Support**: Crisp visuals on high-resolution displays

### Customization Options

#### Display Settings
- **Range Control**: Adjust detection range (50m to 500m)
- **Update Intervals**: Configure scan frequency and refresh rates
- **Theme Options**: Dark/light themes with custom color schemes
- **Font Scaling**: Adjustable text size for different viewing distances
- **Animation Speed**: Control animation timing and effects

#### Analysis Configuration
- **Threat Thresholds**: Customize threat level classification criteria
- **Signal Filtering**: Filter networks by signal strength or security type
- **Vendor Filtering**: Show/hide specific vendor equipment
- **Channel Selection**: Focus on specific frequency bands or channels

## Theming System

Both interfaces feature comprehensive **professional hacker-style theming**:

- **Matrix Green Color Scheme** (#00FF00) with dark backgrounds
- **JetBrains Mono Typography** for authentic monospace appearance
- **Consistent UI Elements** across all components
- **Professional Hover Effects** and interactive feedback
- **Custom Styled Components** (scrollbars, buttons, dialogs)
- **Modern Material Design** elements in the radar interface

See `THEMING_AND_VIEWS.md` for detailed theming documentation.

## Security and Permissions

### Why Root Access is Required

This application requires root privileges for several critical operations:

#### Wireless Interface Control
- **Monitor Mode**: Setting wireless interfaces to monitor mode requires root
- **Raw Socket Access**: Low-level network packet inspection needs privileged access
- **Interface Configuration**: Commands like `iw` and `iwconfig` require root for scanning
- **Frequency Control**: Accessing different wireless channels and frequencies

#### System Resource Access
- **Network Stack**: Direct access to kernel network subsystems
- **Hardware Control**: Wireless adapter configuration and control
- **Process Priorities**: Real-time scanning requires elevated process priorities

### Security Considerations

#### Running as Root
```bash
# Best Practice: Use sudo for temporary elevation
sudo python3 main_launcher.py

# Alternative: Run specific commands as root
sudo -E python3 main_launcher.py  # Preserves environment variables
```

#### Minimizing Security Risks
- **Temporary Privileges**: Only run as root when actively scanning
- **Network Isolation**: Consider running on isolated systems for security testing
- **Log Management**: Monitor application logs for suspicious activity
- **User Separation**: Use dedicated user account for wireless testing

#### Permission Alternatives (Advanced)

##### Using Capabilities (Linux)
```bash
# Grant specific capabilities instead of full root
sudo setcap cap_net_raw,cap_net_admin=eip /usr/bin/python3
# Then run without sudo (experimental)
```

##### NetworkManager Integration
```bash
# Add user to netdev group for some operations
sudo usermod -a -G netdev $USER
# Logout/login required, limited functionality
```

### Professional Usage Guidelines

#### Authorized Testing Only
- **Legal Compliance**: Only scan networks you own or have explicit permission to test
- **Corporate Policy**: Follow your organization's security testing policies
- **Documentation**: Maintain logs of what networks were scanned and when

#### Ethical Considerations
- **Responsible Disclosure**: Report vulnerabilities through proper channels
- **Privacy Respect**: Do not capture or analyze personal data
- **Professional Standards**: Follow industry best practices for security testing

#### Recommended Deployment Scenarios
1. **Dedicated Security Workstation**: Isolated system for security testing
2. **Virtual Machine**: Contained environment with USB WiFi adapter passthrough
3. **Kali Linux**: Purpose-built security testing distribution
4. **Live Boot Environment**: Boot from USB for temporary testing

### Network Interface Requirements

#### Supported Interface Types
- **USB WiFi Adapters**: Often better for monitor mode support
- **PCIe WiFi Cards**: Built-in wireless with driver support
- **External Adapters**: Dedicated security testing adapters

#### Monitor Mode Compatibility
```bash
# Check if your adapter supports monitor mode
sudo iw phy phy0 info | grep -A 10 "Supported interface modes"

# Look for: "monitor" in the output
```

#### Recommended Hardware
- **Alfa Network adapters**: Popular for security testing
- **Atheros chipset**: Generally good monitor mode support  
- **Ralink/MediaTek**: Many support monitor mode
- **Realtek**: Mixed support, check specific models

### Data Privacy and Security

#### What Data is Collected
- **WiFi Metadata**: SSID, BSSID, signal strength, security protocols
- **Vendor Information**: MAC address vendor lookups (OUI database)
- **Timing Information**: Scan timestamps and durations
- **Configuration Data**: Application settings and preferences

#### What Data is NOT Collected
- **Network Traffic**: No packet content analysis or interception
- **Personal Information**: No user data or personal information
- **Credentials**: No password or authentication data
- **Content**: No web browsing or application data

#### Data Storage
- **Local Only**: All data stored locally on your system
- **No Cloud Upload**: No automatic data transmission to external services
- **Temporary Logs**: Most scan data is temporary and not persistent
- **User Control**: Complete control over data retention and deletion

### Compliance and Legal Notes

#### Important Legal Disclaimer
- **Authorization Required**: Only scan networks you own or have explicit written permission to test
- **Local Laws**: Comply with all applicable local, state, and federal laws
- **Corporate Policies**: Follow your organization's IT and security policies
- **Professional Ethics**: Adhere to security industry ethical standards

#### Recommended Documentation
- Keep logs of authorized testing activities
- Document scope and permission for security assessments
- Record findings and recommendations professionally
- Follow responsible disclosure practices for vulnerabilities

*This tool is designed for educational purposes and authorized security testing only. Unauthorized network scanning may be illegal in your jurisdiction.*

### WiFi Analysis Features

#### Real-time Network Discovery
- **Access Point Detection**: Automatic discovery of all nearby WiFi networks
- **Signal Strength Analysis**: Advanced RSSI calculations with distance estimation
- **Channel Analysis**: Frequency and channel utilization monitoring
- **Vendor Identification**: Comprehensive OUI database with 24,000+ vendors

#### Security Protocol Assessment
- **Encryption Detection**: Identifies Open, WEP, WPA/WPA2/WPA3 protocols
- **Security Scoring**: Multi-factor analysis scoring system (0-100 scale)
- **Vulnerability Assessment**: Automated detection of common security weaknesses
- **Configuration Analysis**: Default settings and weak configuration detection

#### Advanced Threat Analysis
- **Risk Classification**: LOW/MEDIUM/HIGH/CRITICAL threat level assignment
- **Attack Vector Identification**: Specific vulnerability types and exploit methods
- **Confidence Rating**: Statistical confidence in analysis results
- **Tool Recommendations**: Suggested tools for further security testing

### Professional Reporting Capabilities

#### Comprehensive Analysis Reports
- **Technical Specifications**: Detailed AP characteristics and configurations
- **Vulnerability Summaries**: Executive and technical vulnerability overviews
- **Attack Methodology**: Step-by-step exploitation guidance
- **Remediation Advice**: Security improvement recommendations
- **Risk Scoring**: Quantified risk assessment with business impact

#### Export and Documentation
- **Copy Functionality**: Easy copying of analysis results for reports
- **Data Export**: Multiple format support for integration with other tools
- **Screenshot Capability**: Visual documentation of findings
- **Historical Tracking**: Scan result comparison over time

*This tool is designed for educational purposes and authorized security testing only. Unauthorized network scanning may be illegal in your jurisdiction.*

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
- Real-time data visualization with customizable update intervals

### Advanced Analysis (Continued)
- Enhanced distance calculation algorithms
- Comprehensive vendor identification
- Multi-factor vulnerability scoring
- Detailed attack vector analysis
- Professional reporting with export capabilities

### User Experience (Enhanced)
- Modern Material Design interface
- Copy functionality for all analysis results
- Professional dialog systems
- Responsive layout design

## Troubleshooting Guide

### Pre-Installation Issues

#### Python Version Compatibility
```bash
# Check Python version (must be 3.6+)
python3 --version

# If version is too old, update Python
sudo apt update
sudo apt install python3.8 python3.8-pip  # or latest available
```

#### Missing Development Tools
```bash
# Error: "Python.h not found" or "gcc not found"
sudo apt install build-essential python3-dev

# Error: "Qt5 development files not found"
sudo apt install qt5-default python3-pyqt5-dev
```

### Wireless Interface Issues

#### "No wireless interfaces detected"
```bash
# 1. Check if wireless interface exists
iwconfig
iw dev
lshw -C network

# 2. Common solutions:
# Enable interface if down
sudo ip link set wlan0 up

# Check if interface is blocked
rfkill list
sudo rfkill unblock wifi

# Restart network services
sudo systemctl restart NetworkManager
```

#### Interface Naming Issues
```bash
# Find your actual interface name
ip link show | grep -E "(wlan|wlp|wlo)"

# Common interface names:
# - wlan0, wlan1 (traditional naming)
# - wlp2s0, wlp3s0 (PCI-based naming)  
# - wlo1 (onboard wireless)

# Update application if using non-standard name:
# Edit config.json to specify your interface
```

#### Monitor Mode Problems
```bash
# Check if interface supports monitor mode
sudo iw phy phy0 info | grep -A 10 "Supported interface modes"

# Some adapters require specific drivers
# USB WiFi adapters often work better for monitoring
```

### Permission and Security Issues

#### "Permission denied" errors
```bash
# Always run with sudo for wireless scanning
sudo python3 main_launcher.py

# Check if user is in netdev group (alternative)
sudo usermod -a -G netdev $USER
# Then logout/login and try without sudo
```

#### NetworkManager Conflicts
```bash
# NetworkManager may interfere with scanning
# Temporary solution:
sudo systemctl stop NetworkManager
sudo python3 main_launcher.py
sudo systemctl start NetworkManager

# Permanent solution (advanced users):
# Configure NetworkManager to ignore your wireless interface
```

#### Firewall Blocking
```bash
# Check if firewall blocks the application
sudo ufw status
# Temporarily disable if needed:
sudo ufw disable
# Re-enable after testing:
sudo ufw enable
```

### Application Runtime Issues

#### "PyQt5 not found" or Import Errors
```bash
# Reinstall PyQt5 properly
pip3 uninstall PyQt5
sudo apt install python3-pyqt5 python3-pyqt5-dev
pip3 install PyQt5>=5.15.0

# For virtual environments:
source venv/bin/activate
pip install PyQt5>=5.15.0
```

#### "TypeError in radar visualization"
```bash
# This was fixed in v5.0, ensure you have latest version
git pull origin main
python3 quick_test.py  # Verify fix
```

#### Application Crashes on Startup
```bash
# Run with debug output
python3 -u main_launcher.py 2>&1 | tee debug.log

# Check for missing fonts (theming issue)
sudo apt install fonts-jetbrains-mono

# Check display environment
echo $DISPLAY
# If empty, export it:
export DISPLAY=:0
```

#### Scanning Fails or No Results
```bash
# 1. Test basic wireless scanning manually
sudo iw dev wlan0 scan | head -20
sudo iwlist wlan0 scan | head -20

# 2. Check interface is not busy
sudo airmon-ng check kill  # Kills conflicting processes

# 3. Reset wireless interface
sudo ip link set wlan0 down
sudo ip link set wlan0 up

# 4. Check for hardware issues
dmesg | grep -i wifi
dmesg | grep -i wireless
```

### Platform-Specific Issues

#### Ubuntu 22.04+ / Debian 12+
```bash
# Wayland display server issues
# Switch to X11 session or:
export QT_QPA_PLATFORM=xcb
```

#### Kali Linux
```bash
# Some tools may conflict
sudo airmon-ng check kill
sudo systemctl disable NetworkManager
# Run application, then re-enable:
sudo systemctl enable NetworkManager
```

#### Arch Linux / Manjaro
```bash
# Package naming differences
sudo pacman -S python-pyqt5 iw wireless_tools

# AUR packages if needed:
yay -S python-requests
```

#### Virtual Machines
```bash
# USB WiFi adapters work better in VMs
# Enable USB 3.0 controller in VM settings
# Pass through USB WiFi adapter to VM

# VMware: VM → Removable Devices → [WiFi Adapter] → Connect
# VirtualBox: Devices → USB → [WiFi Adapter]
```

### Performance Issues

#### Slow Scanning
```bash
# Reduce scan timeout in config.json
# Use faster scan command alternatives
# Limit scan to specific channels if needed
```

#### High CPU Usage
```bash
# Disable animations if needed
# Use Compact mode (800x500) for lower resource usage
# Close other resource-intensive applications
```

#### Memory Issues
```bash
# Monitor memory usage:
ps aux | grep python
# Clear scan history periodically
# Restart application if memory grows too large
```

### Advanced Diagnostics

#### Debug Mode
```bash
# Enable verbose logging
export PYTHONPATH="${PYTHONPATH}:."
python3 -c "import logging; logging.basicConfig(level=logging.DEBUG)"
python3 main_launcher.py
```

#### System Information Gathering
```bash
# Collect system info for bug reports
uname -a
python3 --version
pip3 list | grep -E "(PyQt5|requests)"
iwconfig
lsusb | grep -i wireless
dmesg | tail -50
```

#### Configuration Validation
```bash
# Test all components individually
python3 quick_test.py
python3 test_system.py
python3 validate_system.py
```

### Getting Help

If you encounter issues not covered here:

1. **Check Logs**: Look for error messages in terminal output
2. **Test Components**: Run `python3 quick_test.py` to isolate issues  
3. **System Info**: Gather system information using diagnostic commands above
4. **GitHub Issues**: Create an issue with system info and error logs
5. **Community**: Check existing issues and discussions

**Common Search Terms for Solutions:**
- "PyQt5 wireless interface monitor mode linux"
- "iw scan permission denied ubuntu"
- "NetworkManager conflict wireless scanning"
- "python wifi scanner root privileges"

## Testing

The WiFi Security Radar Suite includes a comprehensive test suite to validate all functionality and ensure system reliability. The testing infrastructure provides multiple levels of validation from basic smoke tests to full integration testing.

### Test Categories

#### 1. Core System Tests
```bash
# Quick smoke test - validates basic imports and functionality
python3 quick_test.py

# Comprehensive system test - validates all core engines
python3 test_system.py
```

**Coverage:**
- ✅ Module imports and dependencies
- ✅ Configuration system loading
- ✅ Vendor database functionality
- ✅ Security analysis engine
- ✅ Distance calculation engine
- ✅ WiFi scanner parsing logic

#### 2. Integration Tests
```bash
# End-to-end workflow validation
python3 test_integration.py
```

**Coverage:**
- ✅ End-to-end data flow from scan to analysis to export
- ✅ Plugin system integration and lifecycle management
- ✅ Configuration integration across modules
- ✅ Error handling and graceful degradation
- ✅ Data consistency across multiple runs

#### 3. Security Validation Tests
```bash
# Security analysis accuracy and threat detection
python3 test_security_validation.py
```

**Coverage:**
- ✅ Security engine accuracy (100% for standard cases)
- ✅ Vulnerability detection capabilities
- ✅ Attack vector identification
- ✅ Security scoring consistency
- ✅ Threat level classification
- ✅ Security recommendation quality

#### 4. Plugin System Tests
```bash
# Plugin discovery, loading, and management
python3 test_plugin_system.py
```

**Coverage:**
- ✅ Plugin discovery and registration
- ✅ Plugin loading and unloading
- ✅ Dependency validation
- ✅ Plugin configuration
- ✅ Plugin capabilities verification

#### 5. GUI Component Tests
```bash
# Non-display GUI component testing
DISPLAY=:99 xvfb-run -a python3 test_gui_non_display.py
```

**Coverage:**
- ✅ GUI module imports
- ✅ Widget creation and properties
- ✅ Theming system functionality
- ✅ Signal/slot connections
- ✅ Custom widget components

### Comprehensive Test Runner

For complete system validation, use the comprehensive test suite:

```bash
# Run all test categories
python3 comprehensive_test_suite.py --category all

# Run specific test category
python3 comprehensive_test_suite.py --category core
python3 comprehensive_test_suite.py --category security
python3 comprehensive_test_suite.py --category integration

# Run with detailed output
python3 comprehensive_test_suite.py --category all --verbose

# Run with performance benchmarks
python3 comprehensive_test_suite.py --category core  # includes performance tests
```

### Master Test Runner

Execute the complete test suite with comprehensive reporting:

```bash
# Run all tests with master reporting
python3 run_all_tests.py
```

This runs all test categories in sequence and provides:
- ✅ Individual test results
- ✅ Category-wise success rates
- ✅ Overall system quality assessment
- ✅ Performance benchmarks
- ✅ Detailed error reporting
- ✅ Quality recommendations

### Test Results Interpretation

#### Success Indicators
- **🎉 100% Pass Rate**: System is production ready
- **✅ 90%+ Pass Rate**: Excellent - minor issues only
- **👍 75%+ Pass Rate**: Good - mostly functional
- **⚠️ 50%+ Pass Rate**: Fair - significant issues
- **❌ <50% Pass Rate**: Poor - critical issues

#### Key Metrics
- **Security Assessment Accuracy**: 100% for standard security types
- **Integration Test Success**: All components work together
- **Plugin System Reliability**: Plugins load/unload correctly
- **Performance Benchmarks**: 
  - Module import: <200ms
  - Configuration loading: <10ms
  - Security analysis: <1ms per network

### Performance Benchmarks

The test suite includes performance validation:

```bash
# Performance metrics (from comprehensive test suite)
Module Import Speed: ~110ms
Configuration Loading: <1ms
Security Analysis (100x): ~3ms total (0.03ms average)
```

**Performance Standards:**
- ✅ Module imports should complete under 200ms
- ✅ Security analysis should process 1000+ networks per second
- ✅ Configuration loading should be under 10ms
- ✅ Memory usage should remain stable across test runs

### Testing Best Practices

#### Before Contributing
```bash
# Always run core tests before submitting changes
python3 test_system.py
python3 test_integration.py
python3 test_security_validation.py
```

#### Continuous Integration
```bash
# Automated test sequence for CI/CD
python3 run_all_tests.py > test_results.log 2>&1
```

#### Development Testing
```bash
# During active development
python3 quick_test.py  # Fast feedback
python3 test_system.py  # Core validation
python3 comprehensive_test_suite.py --category core  # Quick comprehensive check
```

### Test Coverage Areas

#### Functional Testing
- ✅ WiFi scanning and parsing
- ✅ Security analysis algorithms
- ✅ Distance calculation formulas
- ✅ Vendor identification logic
- ✅ Configuration management
- ✅ Plugin system architecture

#### Integration Testing
- ✅ End-to-end data workflows
- ✅ Module interdependencies
- ✅ Plugin interactions
- ✅ Configuration propagation
- ✅ Error handling chains

#### Security Testing
- ✅ Threat level accuracy
- ✅ Vulnerability detection
- ✅ Attack vector identification
- ✅ Security scoring algorithms
- ✅ Recommendation generation

#### Performance Testing
- ✅ Import speed optimization
- ✅ Analysis throughput validation
- ✅ Memory usage monitoring
- ✅ Scalability verification

### Troubleshooting Test Issues

#### Common Test Failures

**Import Errors:**
```bash
# Fix: Install missing dependencies
pip install -r requirements.txt
```

**Display Issues (GUI tests):**
```bash
# Fix: Use virtual display
DISPLAY=:99 xvfb-run -a python3 test_gui_non_display.py
```

**Permission Issues:**
```bash
# Note: Some tests may require network interfaces
# Tests are designed to work without actual WiFi hardware
```

**Plugin Test Failures:**
```bash
# Fix: Ensure plugin directory structure is correct
ls -la plugins/
python3 test_plugin_system.py --verbose
```

### Test Reports

Tests generate detailed reports in multiple formats:

- **JSON Reports**: `test_report.json` - Machine-readable results
- **Console Output**: Real-time progress and results
- **Performance Metrics**: Timing and resource usage
- **Error Logs**: Detailed failure information

#### Sample Test Report Structure
```json
{
  "timestamp": "2025-08-06T13:43:26",
  "total_tests": 8,
  "passed_tests": 7,
  "success_rate": 87.5,
  "categories": {
    "core": {"passed": 2, "total": 2},
    "security": {"passed": 6, "total": 6},
    "integration": {"passed": 5, "total": 5}
  },
  "performance": [
    {"test": "Module Import Speed", "value": 0.11, "unit": "seconds"},
    {"test": "Security Analysis", "value": 0.0003, "unit": "seconds"}
  ]
}
```

### Quality Assurance

The comprehensive test suite ensures:

- **🔒 Security Analysis Accuracy**: Validated against known threat patterns
- **🔌 Plugin System Reliability**: Tested plugin lifecycle management
- **⚡ Performance Standards**: Benchmarked speed and efficiency
- **🔗 Integration Integrity**: Verified component interactions
- **🛡️ Error Resilience**: Validated graceful failure handling

This testing infrastructure provides confidence in the system's reliability, security assessment accuracy, and overall quality for professional security analysis work.

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
