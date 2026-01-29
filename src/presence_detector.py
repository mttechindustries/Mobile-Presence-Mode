#!/usr/bin/env python3
"""
Presence Detector Module
Real-time presence and breathing detection using CSI data
"""

import time
import argparse
import numpy as np
from scipy import signal
from csi_capture import CSICapture

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
        mean_variance = np.mean(variance)
        
        # Presence detection
        presence_detected = mean_variance > self.presence_threshold
        
        # Breathing detection (more subtle changes)
        breathing_detected = mean_variance > self.breathing_threshold and mean_variance < self.presence_threshold
        
        return presence_detected, breathing_detected, mean_variance
    
    def extract_breathing_signal(self, csi_data):
        """
        Extract breathing signal from CSI data using bandpass filtering
        
        Args:
            csi_data (numpy.ndarray): CSI amplitude data
            
        Returns:
            numpy.ndarray: Filtered breathing signal
        """
        if len(csi_data) == 0:
            return np.array([])
            
        # Average across subcarriers to get overall signal
        mean_signal = np.mean(csi_data, axis=1)
        
        # Normalize signal
        mean_signal = (mean_signal - np.mean(mean_signal)) / np.std(mean_signal)
        
        # Bandpass filter for breathing frequency range (0.1-0.5 Hz)
        fs = 20  # Sampling frequency (Hz)
        lowcut = 0.1  # Low cutoff frequency (Hz)
        highcut = 0.5  # High cutoff frequency (Hz)
        
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        
        # Design bandpass filter
        b, a = signal.butter(4, [low, high], btype='band')
        filtered_signal = signal.filtfilt(b, a, mean_signal)
        
        return filtered_signal
    
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
            
        # Find peaks in the breathing signal
        peaks, _ = signal.find_peaks(breathing_signal, distance=5)
        
        if len(peaks) < 2:
            return 0.0
            
        # Calculate time between peaks
        peak_times = np.arange(len(breathing_signal))[peaks]
        time_diffs = np.diff(peak_times)
        
        # Convert to breaths per minute
        avg_time_diff = np.mean(time_diffs)
        if avg_time_diff > 0:
            bpm = 60.0 / (avg_time_diff / 20.0)  # 20 Hz sampling rate
            return bpm
        else:
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
