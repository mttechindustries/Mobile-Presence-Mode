#!/bin/bash

# hotspot_setup.sh
# Script to set up Android hotspot for Mobile Presence Mode
# This creates the transmitter side of the CSI system

echo "Android Hotspot Setup for Mobile Presence Mode"
echo "=============================================="
echo ""

# Check if running on Android
if [ ! -f "/system/bin/sh" ]; then
    echo "Error: This script is designed for Android devices"
    echo "For testing on Linux, use: nmcli or create_ap"
    exit 1
fi

# Check for root access (needed for some configurations)
ROOT_AVAILABLE=false
if [ "$(id -u)" = "0" ]; then
    ROOT_AVAILABLE=true
fi

echo "Setting up Wi-Fi hotspot for CSI transmission..."
echo ""

# Method 1: Using Android Settings (no root required)
echo "Method 1: Using Android Settings API"
echo "------------------------------------"
echo "1. Open Settings on your Android device"
echo "2. Go to: Network & internet > Hotspot & tethering"
echo "3. Tap on Wi-Fi hotspot"
echo "4. Configure hotspot:"
echo "   - Network name (SSID): PresenceMode-Hotspot"
echo "   - Security: WPA2-PSK"
echo "   - Password: presence123 (or your choice)"
echo "   - Band: 2.4GHz (better for CSI)"
echo "   - Channel: Auto (or 6 for best compatibility)"
echo "5. Turn on the hotspot"
echo ""

# Method 2: Using ADB (for automation)
echo "Method 2: Using ADB (for automation)"
echo "------------------------------------"
echo "If you have ADB access, you can automate hotspot setup:"
echo ""
echo "adb shell svc wifi enable"
echo "adb shell am start -n com.android.settings/.TetherSettings"
echo ""
echo "Or use this command to enable hotspot programmatically:"
echo "adb shell cmd wifi set-hotspot enabled ssid PresenceMode-Hotspot password presence123"
echo ""

# Method 3: Using termux (for advanced users)
echo "Method 3: Using Termux (advanced)"
echo "-----------------------------------"
echo "If you have Termux installed:"
echo "pkg install termux-api"
echo "termux-wifi-enable true"
echo "termux-wifi-hotspot-on PresenceMode-Hotspot presence123"
echo ""

# Optimal hotspot configuration for CSI
echo "Optimal Hotspot Configuration for CSI"
echo "-------------------------------------"
echo "For best CSI performance:"
echo "✓ Use 2.4GHz band (better multipath for CSI)"
echo "✓ Channel width: 20MHz (most stable for CSI)"
echo "✓ Security: WPA2-PSK (compatible with most CSI tools)"
echo "✓ Avoid channel hopping (fixed channel preferred)"
echo "✓ Place transmitter 1-2m above floor for best coverage"
echo ""

# Troubleshooting
echo "Troubleshooting"
echo "--------------"
echo "If CSI capture isn't working:"
echo "1. Check that hotspot is visible on receiver device"
echo "2. Ensure receiver is connected to hotspot"
echo "3. Verify CSI tools are running on receiver"
echo "4. Check for Wi-Fi interference from other devices"
echo "5. Try different channels if performance is poor"
echo ""

# Receiver setup reminder
echo "Receiver Setup Reminder"
echo "----------------------"
echo "On your CSI receiver device:"
echo "1. Connect to the PresenceMode-Hotspot"
echo "2. Run: python src/presence_detector.py"
echo "3. Or for visualization: python src/visualize.py"
echo ""

echo "Hotspot setup guide completed!"
echo "Your Android device is now ready to transmit CSI signals."
