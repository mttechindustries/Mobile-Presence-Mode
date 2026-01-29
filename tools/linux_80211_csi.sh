#!/bin/bash

# linux_80211_csi.sh
# Script to set up CSI capture on Linux using 802.11n CSI tools
# This provides an alternative to Android-based CSI capture

echo "Linux 802.11n CSI Setup Script"
echo "=============================="
echo ""

# Check if running as root
if [ "$(id -u)" != "0" ]; then
    echo "Error: Root access required. Please run with sudo."
    exit 1
fi

# Check if running on Linux
if [ ! -f "/etc/os-release" ]; then
    echo "Error: This script must be run on a Linux system"
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
apt-get update
apt-get install -y git make gcc g++ libpcap-dev python3 python3-pip

# Install Python dependencies
pip3 install numpy scipy matplotlib

# Clone linux-80211n-csitool repository
echo "Cloning linux-80211n-csitool repository..."
cd /opt
rm -rf linux-80211n-csitool
git clone https://github.com/dhalperi/linux-80211n-csitool.git
cd linux-80211n-csitool

# Build the tool
echo "Building linux-80211n-csitool..."
make

# Check if build was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "linux-80211n-csitool setup completed successfully!"
    echo ""
    echo "To use the CSI tool:"
    echo "1. Make sure you have a compatible Wi-Fi card (Intel 5300 recommended)"
    echo "2. Put your Wi-Fi interface in monitor mode:"
    echo "   sudo ifconfig wlan0 down"
    echo "   sudo iwconfig wlan0 mode monitor"
    echo "   sudo ifconfig wlan0 up"
    echo "3. Start CSI capture:"
    echo "   sudo ./csitool wlan0"
    echo ""
    echo "Note: CSI capture on Linux requires specific Wi-Fi hardware."
    echo "Intel 5300 series cards are known to work well."
else
    echo "Error: linux-80211n-csitool build failed"
    exit 1
fi
