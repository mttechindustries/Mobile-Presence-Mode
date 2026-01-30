import sys
import os
import numpy as np

# Ensure src/ is on sys.path so imports in the project work during tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from presence_detector import PresenceDetector


def test_breathing_detection_and_rate():
    # Synthetic breathing signal: 0.25 Hz => 15 BPM
    fs = 20.0
    duration = 30.0
    t = np.arange(0, duration, 1.0 / fs)
    breath_freq = 0.25
    single_channel = 0.5 * np.sin(2 * np.pi * breath_freq * t)

    # Construct CSI data with 30 subcarriers: same breathing signal across subcarriers + small noise
    num_subcarriers = 30
    noise = 0.01 * np.random.randn(len(t), num_subcarriers)
    csi_data = np.tile(single_channel.reshape(-1, 1), (1, num_subcarriers)) + noise

    detector = PresenceDetector()

    presence, breathing, variance = detector.detect_presence(csi_data)

    assert not presence
    assert breathing

    breathing_signal = detector.extract_breathing_signal(csi_data)
    bpm = detector.estimate_breathing_rate(breathing_signal)

    assert bpm > 12 and bpm < 18


def test_presence_detection_motion():
    # High variance across subcarriers to simulate motion
    samples = 200
    num_subcarriers = 30
    csi_data = np.random.uniform(0, 5.0, size=(samples, num_subcarriers))

    detector = PresenceDetector()
    presence, breathing, variance = detector.detect_presence(csi_data)
    assert presence
    # High variance should yield mean variance above presence threshold
    assert variance > detector.presence_threshold
