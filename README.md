# Mobile Presence Mode

Portable Wi‑Fi CSI presence detection using a dedicated portable hotspot or a phone hotspot as transmitter, and a receiver running CSI capture and processing. Detects humans and pets via breathing, motion, and micro‑vibrations with no extra hardware beyond commodity Wi‑Fi devices.

Contents
- Overview
- Hardware recommendations
- Software stack
- Quickstart (capture → detect → visualize)
- OpenWrt / hotspot setup (script provided)
- Implementation notes and algorithms
- Tests and development
- License & citation

## Overview

Mobile Presence Mode turns a Wi‑Fi transmitter (phone hotspot or a small portable hotspot running OpenWrt) and a CSI‑capable receiver into a portable presence sensor. The system processes Channel State Information (CSI) to detect low‑amplitude motion such as breathing and micro‑vibrations.

### Why use a dedicated portable hotspot?
- Stability & uptime: dedicated devices run 24/7 without phone thermal/battery limitations.
- More models with supported chipsets (MediaTek, some Atheros) can run OpenWrt and CSI tools.
- Better control over channels and transmit power; easier to configure and maintain.

## Hardware recommendations (2024–2026)
- GL.iNet GL‑MT3000 (Beryl AX) — Wi‑Fi 6, strong OpenWrt support.
- GL.iNet GL‑AR750S (Slate) — compact and widely used.
- TP‑Link TL‑WR902AC — inexpensive portable router.
- Banana Pi / other small single‑board routers for power users.

### Receiver
- Laptop running Linux or an Android device with CSI capture capability (nexmon, linux‑80211n variants). The receiver must be able to capture raw CSI frames from the Wi‑Fi driver or via a patched firmware.

## Software stack
- Python 3 (use python3 and create a virtualenv or `.venv` when needed)
- Dependencies: `numpy`, `scipy`, `matplotlib`, `pyyaml`, `scikit-learn`, `pandas`, `pytest` (see `requirements.txt`)
- CSI capture tools: commonly used projects include `nexmon_csi` or `linux-80211n`/`linux-80211ng` variants for different chipsets.

## Quickstart

1. Prepare hotspot (phone or dedicated OpenWrt device). For a dedicated hotspot, follow `tools/openwrt_setup.sh`.
2. On receiver, create and activate a Python virtual environment and install requirements:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

3. Capture CSI (example using simulated capture provided with this repo):

```bash
python3 src/csi_capture.py --duration 60 --output data/csi_capture.npy
```

4. Run single detection test:

```bash
```bash
python3 src/presence_detector.py --test --duration 10
```

5. Continuous detection:

```bash
```bash
python3 src/presence_detector.py --interval 2
```

6. Visualize last capture:

```bash
```bash
python3 src/visualize.py --input data/csi_capture.npy
```

## OpenWrt / Hotspot setup

For dedicated portable hotspots we recommend flashing OpenWrt when supported by the vendor. The included `tools/openwrt_setup.sh` provides opkg commands and configuration hints to install CSI capture tools and configure a stable transmission SSID and fixed channel.

## Important implementation notes

- CSI parsing: real CSI capture requires parsing vendor/firmware specific binary formats. `src/utils/csi_parser.py` contains parsing stubs; implementing a `nexmon_csi` or OpenWrt driver parser is required for real deployments.
- Preprocessing: common pipeline steps are subcarrier averaging, detrending, normalization, bandpass filtering in the breathing band (commonly 0.1–0.5 Hz), and outlier removal.
- Algorithms: bandpass filters + peak detection or spectral peak estimation are effective for breathing rate estimation; PCA/ICA and ML models (CNN/Transformer) are used for more complex activity recognition.
- Sampling: many breathing studies use ~20 Hz sampling; high‑resolution tasks may capture hundreds to thousands of packets/sec if hardware allows.
- Robustness: add calibration and dynamic thresholding; `presence_threshold` and `breathing_threshold` in `src/presence_detector.py` are tunable parameters.

## Development and tests

- Tests: basic unit tests added under `tests/` (run with `python3 -m pytest`).
- Lint and format using your preferred tools.

## Security, privacy, and ethics

- Processing is intended to run on the receiver device; do not send raw CSI off‑device unless explicitly authorized by the user.
- The framework detects presence and breathing only; it does not store or transmit identity unless you add such features.

## Citation

If you use this framework in research, cite:

```
@misc{mobile-presence-mode,
  author = {MT Tech Industries},
  title = {Mobile Presence Mode: Portable Wi‑Fi CSI Presence Detection},
  year = {2024},
  url = {https://github.com/mttechindustries/mobile-presence-mode}
}
```

## License

See the `LICENSE` file for licensing information.

## Contributing

Contributions welcome. Recommended next work items:
- Implement `src/utils/csi_parser.py` for your target CSI source (nexmon/OpenWrt driver).
- Add CI to run tests automatically.
- Add demonstrator scripts and a small dataset for calibration.
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
pip3 install -r requirements.txt
```

## Usage

### Basic presence detection
```bash
python3 src/presence_detector.py
```

### Visualize breathing patterns
```bash
python3 src/visualize.py
```

### Capture CSI data
```bash
python3 src/csi_capture.py --duration 60 --output data/csi_capture.npy
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
