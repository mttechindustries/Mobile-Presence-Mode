# Mobile Presence Mode

**Portable Wi-Fi CSI presence detection using only a phone hotspot as transmitter and receiver.**

Detects humans/pets via breathing, movement, and micro-vibrations. Zero extra hardware required.

## Overview

Mobile Presence Mode turns any Android phone hotspot into a portable, passive presence detector using Wi-Fi Channel State Information (CSI). This approach is stronger than traditional radar in terms of cost ($0 vs $50-$500), portability (pocket-sized), and privacy (owner-controlled signal).

### Key Advantages
- **Cost**: Zero extra hardware beyond phones
- **Portability**: Hotspot in pocket = instant radar anywhere
- **Privacy**: Signal owned by user, processing on-device
- **Resolution**: Detects mm-scale motion via CSI subcarrier changes
- **Multipath advantage**: Indoor reflections provide richer data than radar's line-of-sight

## Setup Requirements

### Hardware
- **Transmitter**: Any Android/iOS phone with hotspot capability
- **Receiver**: Rooted Android phone with Wi-Fi chip supporting CSI capture (Nexus 5X, Pixel 2-5, some Xiaomi models)

### Software
- Rooted receiver with **nexmon_csi** installed
- Python 3.10+ on receiver or paired device
- Required libraries: numpy, scipy, matplotlib, pyyaml

## Installation

### 1. Root your Android receiver device
```bash
# Use appropriate rooting method for your device
# Pixel devices: https://developers.google.com/android/images
# Nexus devices: https://developer.android.com/studio/run/device
```

### 2. Install nexmon_csi on receiver
```bash
./tools/nexmon_csi_install.sh
```

### 3. Set up Python environment
```bash
pip install -r requirements.txt
```

## Usage

### Basic presence detection
```bash
python src/presence_detector.py
```

### Visualize breathing patterns
```bash
python src/visualize.py
```

### Capture CSI data
```bash
python src/csi_capture.py --duration 60 --output data/csi_capture.npy
```

## Performance Benchmarks

Based on 2023-2026 research papers:
- **Breathing detection accuracy**: 92-96%
- **Range**: 3-5 meters (indoors)
- **Resolution**: mm-scale motion detection
- **Power consumption**: Minimal (uses existing Wi-Fi)

## Privacy & Ethics

- All CSI capture and processing is on-device
- No cloud transmission unless explicitly opted in
- Only presence/breathing detected - no identity or recording
- See [docs/privacy_policy.md](docs/privacy_policy.md) for details

## Comparison with Traditional Radar

| Feature | Mobile Presence Mode | Traditional Radar |
|---------|----------------------|-------------------|
| Cost | $0 (phones only) | $50-$500 |
| Portability | Pocket-sized | Bulky sensor |
| Privacy | Owner-controlled | Potential privacy concerns |
| Indoor performance | Excellent (multipath) | Good (line-of-sight) |
| Outdoor performance | Limited | Excellent |
| Power consumption | Low (Wi-Fi) | High (dedicated sensor) |

## License

MIT License - See [LICENSE](LICENSE) file

## Contributing

Contributions welcome! Please open issues for bugs/feature requests and submit pull requests for improvements.

## Citation

If you use this framework in research, please cite:
```
@misc{mobile-presence-mode,
  author = {MT Tech Industries},
  title = {Mobile Presence Mode: Portable Wi-Fi CSI Presence Detection},
  year = {2024},
  url = {https://github.com/mttechindustries/mobile-presence-mode}
}
```
