#!/bin/bash

# nexmon_csi_install.sh
# Script to install nexmon_csi on rooted Android devices
# This enables CSI capture on supported Wi-Fi chips

echo "nexmon_csi Installation Script"
echo "============================"
echo ""

# Check if running on Android
if [ ! -f "/system/bin/sh" ]; then
    echo "Error: This script must be run on an Android device"
    exit 1
fi

# Check for root access
if [ "$(id -u)" != "0" ]; then
    echo "Error: Root access required. Please run as root."
    exit 1
fi

# Check device architecture
ARCH=$(getprop ro.product.cpu.abi)
echo "Detected architecture: $ARCH"

# Install dependencies
echo "Installing dependencies..."
apt-get update
apt-get install -y git make gcc clang python3

# Clone nexmon repository
echo "Cloning nexmon repository..."
cd /data/local/tmp
rm -rf nexmon_csi
git clone https://github.com/seemoo-lab/nexmon_csi.git
cd nexmon_csi

# Build nexmon
echo "Building nexmon..."
make

# Install nexmon
echo "Installing nexmon..."
make install

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "nexmon_csi installation completed successfully!"
    echo ""
    echo "To use nexmon_csi:"
    echo "1. Reboot your device"
    echo "2. Run: nexmon_csi -h for help"
    echo "3. Start CSI capture: nexmon_csi -i wlan0 -o csi.log"
    echo ""
    echo "Supported devices:"
    echo "- Nexus 5X (bullhead)"
    echo "- Pixel 2/2 XL (walleye/taimen)"
    echo "- Pixel 3/3 XL (blueline/crosshatch)"
    echo "- Pixel 4/4 XL (flame/coral)"
    echo "- Some Xiaomi devices"
else
    echo "Error: nexmon_csi installation failed"
    echo "Your device may not be supported"
    exit 1
fi
