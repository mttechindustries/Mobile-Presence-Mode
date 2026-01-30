#!/usr/bin/env python3
"""
Presence Detector Module
Real-time presence and breathing detection using CSI data
"""

import time
import argparse
import numpy as np
from csi_capture import CSICapture
from utils.signal_filter import extract_breathing_features


class PresenceDetector:
    def __init__(self, interface='wlan0', capture_duration=5):
        """Initialize presence detector"""
        self.interface = interface
        self.capture_duration = capture_duration
        self.capture = CSICapture(interface)
        self.presence_threshold = 0.15  # Variance threshold for presence detection
        self.breathing_threshold = 0.05  # Variance threshold for breathing detection

    def detect_presence(self, csi_data):
        """
        Detect presence based on CSI variance

        Args:
            csi_data (numpy.ndarray): CSI amplitude data

        Returns:
            tuple: (presence_detected, breathing_detected, variance_score)
        """
        if len(csi_data) == 0:
            return False, False, 0.0

        # Calculate variance across subcarriers
        variance = np.var(csi_data, axis=0)
        mean_variance = float(np.mean(variance))

        # Presence detection
        presence_detected = mean_variance > self.presence_threshold

        # Breathing detection: check breathing-band features when variance is moderate
        breathing_detected = False
        try:
            features = extract_breathing_features(csi_data, fs=20)
            # breathing detected if we have at least one peak and variance in breathing band exceeds threshold
            breathing_detected = (features.get('num_peaks', 0) > 0) and (features.get('variance', 0.0) > self.breathing_threshold)
        except Exception:
            # Propagate failure implicitly by not hiding it: re-raise to caller
            raise

        return presence_detected, breathing_detected, mean_variance

    def extract_breathing_signal(self, csi_data):
        """
        Extract breathing signal from CSI data using `extract_breathing_features` helper.

        Args:
            csi_data (numpy.ndarray): CSI amplitude data

        Returns:
            numpy.ndarray: Filtered breathing signal
        """
        if len(csi_data) == 0:
            return np.array([])

        # Delegate to signal_filter.extract_breathing_features
        features = extract_breathing_features(csi_data, fs=20)
        return features.get('breathing_signal', np.array([]))

    def estimate_breathing_rate(self, breathing_signal):
        """
        Estimate breathing rate from filtered signal

        Args:
            breathing_signal (numpy.ndarray): Filtered breathing signal

        Returns:
            float: Breathing rate in breaths per minute (BPM)
        """
        if len(breathing_signal) < 10:
            return 0.0

        # Use simple peak detection to estimate rate assuming 20 Hz sampling
        from scipy import signal as _signal
        fs = 20.0
        peaks, _ = _signal.find_peaks(breathing_signal, distance=int(0.5 * fs))

        if len(peaks) < 2:
            return 0.0

        peak_times = np.array(peaks) / fs
        time_diffs = np.diff(peak_times)
        avg_time = float(np.mean(time_diffs))
        if avg_time > 0:
            bpm = 60.0 / avg_time
            return float(bpm)
        return 0.0

    def run_continuous_detection(self, interval=2):
        """
        Run continuous presence detection

        Args:
            interval (int): Detection interval in seconds
        """
        print("Starting continuous presence detection...")
        print("Press Ctrl+C to stop")

        try:
            while True:
                start_time = time.time()

                # Capture CSI data
                csi_data = self.capture.capture_csi(duration=self.capture_duration)

                # Detect presence
                presence, breathing, variance = self.detect_presence(csi_data)

                # Extract breathing signal if presence detected
                breathing_rate = 0.0
                if presence or breathing:
                    breathing_signal = self.extract_breathing_signal(csi_data)
                    breathing_rate = self.estimate_breathing_rate(breathing_signal)

                # Print results
                timestamp = time.strftime('%H:%M:%S')
                status = "No presence"

                if presence:
                    status = f"Presence detected (motion)"
                elif breathing:
                    status = f"Breathing detected ({breathing_rate:.1f} BPM)"

                print(f"[{timestamp}] {status} | Variance: {variance:.4f}")

                # Sleep for remaining interval time
                elapsed = time.time() - start_time
                sleep_time = max(0, interval - elapsed)
                time.sleep(sleep_time)

        except KeyboardInterrupt:
            print("\nPresence detection stopped")

def main():
    parser = argparse.ArgumentParser(description='Presence Detector')
    parser.add_argument('--interface', type=str, default='wlan0',
                       help='Network interface for CSI capture')
    parser.add_argument('--duration', type=int, default=5,
                       help='CSI capture duration per detection cycle')
    parser.add_argument('--interval', type=int, default=2,
                       help='Detection interval in seconds')
    parser.add_argument('--test', action='store_true',
                       help='Run a single test detection')
    
    args = parser.parse_args()
    
    detector = PresenceDetector(
        interface=args.interface,
        capture_duration=args.duration
    )
    
    if args.test:
        # Run single test
        print("Running single presence detection test...")
        csi_data = detector.capture.capture_csi(duration=args.duration)
        presence, breathing, variance = detector.detect_presence(csi_data)
        
        if presence:
            print("✓ Presence detected (motion)")
        elif breathing:
            breathing_signal = detector.extract_breathing_signal(csi_data)
            breathing_rate = detector.estimate_breathing_rate(breathing_signal)
            print(f"✓ Breathing detected ({breathing_rate:.1f} BPM)")
        else:
            print("✗ No presence detected")
            
        print(f"Variance score: {variance:.4f}")
    else:
        # Run continuous detection
        detector.run_continuous_detection(interval=args.interval)

if __name__ == '__main__':
    main()
