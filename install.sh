#!/bin/bash

# WiFi Security Radar Suite - Installation Script
# Automated installation for Ubuntu/Debian systems

set -e  # Exit on any error

echo "==============================================="
echo "WiFi Security Radar Suite v5.0 - Installer"
echo "==============================================="
echo

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
    print_error "This script should not be run as root!"
    print_status "Run as regular user, sudo will be used when needed."
    exit 1
fi

# Detect OS
if [[ -f /etc/os-release ]]; then
    . /etc/os-release
    OS=$ID
    OS_VERSION=$VERSION_ID
else
    print_error "Cannot detect operating system"
    exit 1
fi

print_status "Detected OS: $PRETTY_NAME"

# Check for supported OS
case $OS in
    ubuntu|debian|kali)
        PACKAGE_MANAGER="apt"
        ;;
    arch|manjaro)
        PACKAGE_MANAGER="pacman"
        ;;
    fedora|centos|rhel)
        PACKAGE_MANAGER="dnf"
        ;;
    *)
        print_warning "Unsupported OS detected. Continuing with apt..."
        PACKAGE_MANAGER="apt"
        ;;
esac

print_status "Using package manager: $PACKAGE_MANAGER"
echo

# Step 1: Update package manager
print_status "Updating package manager..."
case $PACKAGE_MANAGER in
    apt)
        sudo apt update && sudo apt upgrade -y
        ;;
    pacman)
        sudo pacman -Syu --noconfirm
        ;;
    dnf)
        sudo dnf update -y
        ;;
esac
print_success "Package manager updated"

# Step 2: Install system dependencies
print_status "Installing system dependencies..."
case $PACKAGE_MANAGER in
    apt)
        sudo apt install -y python3 python3-pip python3-pyqt5 python3-pyqt5-dev \
                           wireless-tools iw build-essential python3-dev \
                           fonts-jetbrains-mono git
        ;;
    pacman)
        sudo pacman -S --noconfirm python python-pip python-pyqt5 wireless_tools \
                                   iw base-devel git ttf-jetbrains-mono
        ;;
    dnf)
        sudo dnf install -y python3 python3-pip python3-qt5 wireless-tools \
                           iw @development-tools python3-devel git \
                           jetbrains-mono-fonts
        ;;
esac
print_success "System dependencies installed"

# Step 3: Check Python version
print_status "Checking Python version..."
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1-2)
if python3 -c "import sys; exit(0 if sys.version_info >= (3, 6) else 1)"; then
    print_success "Python $PYTHON_VERSION is compatible"
else
    print_error "Python 3.6+ is required, found $PYTHON_VERSION"
    exit 1
fi

# Step 4: Install Python dependencies
print_status "Installing Python dependencies..."
pip3 install --user -r requirements.txt
print_success "Python dependencies installed"

# Step 5: Check wireless interfaces
print_status "Checking wireless interfaces..."
if command -v iwconfig &> /dev/null; then
    INTERFACES=$(iwconfig 2>/dev/null | grep -E "wlan|wlp|wlo" | cut -d' ' -f1 || true)
    if [[ -n "$INTERFACES" ]]; then
        print_success "Wireless interfaces detected: $INTERFACES"
    else
        print_warning "No wireless interfaces detected"
        print_status "This may be normal if running in a VM or without WiFi hardware"
    fi
else
    print_warning "iwconfig not available, skipping interface check"
fi

# Step 6: Test installation
print_status "Testing installation..."
if python3 quick_test.py; then
    print_success "Installation test completed successfully"
else
    print_error "Installation test failed"
    echo "Check the error messages above and run the test manually:"
    echo "  python3 quick_test.py"
    exit 1
fi

# Step 7: Final instructions
echo
echo "==============================================="
print_success "Installation completed successfully!"
echo "==============================================="
echo
print_status "Next steps:"
echo "  1. Run the application: sudo python3 main_launcher.py"
echo "  2. For first-time setup, see the README.md"
echo "  3. Ensure you have permission to scan networks"
echo
print_warning "Important security note:"
echo "  - Only scan networks you own or have permission to test"
echo "  - Follow all applicable laws and regulations"
echo "  - Use responsibly for educational/authorized testing only"
echo
print_status "For troubleshooting, see the comprehensive guide in README.md"
echo

# Optional: Create desktop shortcut
read -p "Create desktop shortcut? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    DESKTOP_FILE="$HOME/Desktop/WiFi-Security-Radar.desktop"
    cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=WiFi Security Radar Suite
Comment=Professional WiFi Security Analysis Tools
Exec=sudo python3 $(pwd)/main_launcher.py
Icon=network-wireless
Terminal=true
Categories=Network;Security;
EOF
    chmod +x "$DESKTOP_FILE"
    print_success "Desktop shortcut created: $DESKTOP_FILE"
fi

print_success "Setup complete! Happy scanning!"