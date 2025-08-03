#!/bin/bash

# WiFi Security Radar Suite Launch Script
# Automated launcher with dependency checking

echo "WiFi Security Radar Suite v5.0"
echo "=================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Error: This application requires root privileges for WiFi scanning."
    echo "Please run with sudo: sudo ./launch.sh"
    exit 1
fi

# Check Python dependencies
echo "Checking dependencies..."

if ! command -v python3 &> /dev/null; then
    echo "Python3 not found. Please install Python3."
    exit 1
fi

if ! python3 -c "import PyQt5" &> /dev/null; then
    echo "PyQt5 not found. Installing..."
    apt update
    apt install -y python3-pyqt5 python3-pyqt5-dev
fi

# Check wireless tools
if ! command -v iw &> /dev/null && ! command -v iwlist &> /dev/null; then
    echo "Wireless tools not found. Installing..."
    apt install -y wireless-tools iw
fi

echo "Dependencies checked successfully!"
echo ""

# Launch the main application
echo "Launching WiFi Security Radar Suite..."
python3 main_launcher.py

echo ""
echo "Thank you for using WiFi Security Radar Suite!"
