#!/usr/bin/env python3
"""
CSI Capture Module
Main script for capturing Wi-Fi Channel State Information (CSI) data
"""

import time
import argparse
import numpy as np
from utils.csi_parser import parse_csi_packet

class CSICapture:
    def __init__(self, interface='wlan0'):
        """Initialize CSI capture with specified network interface"""
        self.interface = interface
        self.csi_data = []
        
    def capture_csi(self, duration=60):
        """
        Capture CSI data for specified duration
        
        Args:
            duration (int): Capture duration in seconds
            
        Returns:
            numpy.ndarray: CSI amplitude data matrix
        """
        print(f"Capturing CSI on {self.interface} for {duration}s...")
        self.csi_data = []
        
        # Simulate CSI capture (in real implementation, use nexmon_csi or linux-80211ng)
        start_time = time.time()
        
        try:
            while time.time() - start_time < duration:
                # In real implementation, this would read from the CSI interface
                # For now, we'll simulate with random data for testing
                simulated_packet = self._simulate_csi_packet()
                parsed = parse_csi_packet(simulated_packet)
                self.csi_data.append(parsed['amplitude'])
                time.sleep(0.05)  # Simulate packet arrival rate
                
        except KeyboardInterrupt:
            print("CSI capture interrupted by user")
        
        return np.array(self.csi_data)
    
    def _simulate_csi_packet(self):
        """Simulate CSI packet for testing purposes"""
        # Simulate 30 subcarriers with random amplitude and phase
        num_subcarriers = 30
        amplitude = np.random.uniform(0.5, 1.5, num_subcarriers)
        phase = np.random.uniform(0, 2*np.pi, num_subcarriers)
        
        return {
            'amplitude': amplitude,
            'phase': phase,
            'timestamp': time.time(),
            'subcarriers': num_subcarriers
        }
    
    def save_csi_data(self, filename):
        """Save captured CSI data to file"""
        if self.csi_data:
            np.save(filename, np.array(self.csi_data))
            print(f"CSI data saved to {filename}")
        else:
            print("No CSI data to save")
    
    def load_csi_data(self, filename):
        """Load CSI data from file"""
        self.csi_data = np.load(filename)
        print(f"CSI data loaded from {filename}")
        return self.csi_data

def main():
    parser = argparse.ArgumentParser(description='CSI Capture Tool')
    parser.add_argument('--interface', type=str, default='wlan0', 
                       help='Network interface for CSI capture')
    parser.add_argument('--duration', type=int, default=60, 
                       help='Capture duration in seconds')
    parser.add_argument('--output', type=str, 
                       help='Output file to save CSI data')
    parser.add_argument('--load', type=str, 
                       help='Load CSI data from file instead of capturing')
    
    args = parser.parse_args()
    
    capture = CSICapture(interface=args.interface)
    
    if args.load:
        # Load existing CSI data
        csi_data = capture.load_csi_data(args.load)
    else:
        # Capture new CSI data
        csi_data = capture.capture_csi(duration=args.duration)
        
        if args.output:
            capture.save_csi_data(args.output)
    
    print(f"Captured {len(csi_data)} CSI samples")
    print(f"Data shape: {csi_data.shape}")

if __name__ == '__main__':
    main()
