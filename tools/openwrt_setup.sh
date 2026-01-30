#!/bin/sh
# OpenWrt setup helper for Mobile Presence Mode
# This script runs on an OpenWrt-capable hotspot (GL.iNet, similar devices).
# It performs safe package installs and configures a stable SSID and channel.
#
# IMPORTANT: Building and installing firmware-level CSI tools (nexmon_csi) often
# requires compiling driver/firmware components and cannot be fully automated
# here. This script prepares the device and provides the exact commands and
# links you should run to fetch and build CSI tools.

set -e

echo "OpenWrt setup helper — preparing hotspot for CSI capture"

echo "Updating package lists..."
opkg update || { echo "opkg update failed"; exit 1; }

echo "Installing useful packages (git, curl, python3)..."
opkg install git curl ca-certificates python3 python3-pip || echo "Some packages may be unavailable on this image; install manually via opkg" 

echo "Configuring Wi-Fi: fixed SSID and channel"
# Configure SSID and channel (set to 5 GHz channel 36 by default if supported)
SSID="PresenceMode"
CHANNEL="36"

uci set wireless.@wifi-iface[0].ssid="$SSID" || true
uci set wireless.@wifi-device[0].channel="$CHANNEL" || true
uci commit wireless || true
wifi reload || true

echo "Wi-Fi configured: SSID=$SSID CHANNEL=$CHANNEL"

echo "Recommended next steps (manual):"
cat <<'EOF'
1) Install or build CSI capture tools (nexmon_csi or linux-80211ng variants):

   - Many CSI tool projects require building patched firmware/drivers.
   - See the nexmon_csi project for Broadcom-based devices (example):
     https://github.com/seemoo-lab/nexmon_csi

   - For MediaTek/MTK devices running OpenWrt, look for vendor-specific
     CSI extraction projects or consult OpenWrt community pages for your
     router SoC.

   Typical manual steps:
   git clone https://github.com/seemoo-lab/nexmon_csi.git
   cd nexmon_csi
   <follow repository build instructions; may require SDK/toolchain>

2) If you successfully build kernel modules or firmware patches, install
   them via `opkg` or by copying files to the device and restarting the
   wireless stack.

3) On the receiver (laptop or rooted Android), configure CSI capture to
   join this hotspot SSID and start packet capture using the installed
   CSI tool. Store captured CSI to a file and transfer it to the analysis
   host if needed.

4) Use the repository's `src/` tools to analyze captures:
   python3 src/csi_capture.py --load data/csi_capture.npy
   python3 src/presence_detector.py --test --duration 10

EOF

echo "OpenWrt setup helper complete. See README.md for usage examples and next steps."
