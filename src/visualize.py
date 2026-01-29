#!/usr/bin/env python3
"""
Visualization Module
Plot CSI data, breathing signals, and detection results
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
from csi_capture import CSICapture
from presence_detector import PresenceDetector

class CSIVisualizer:
    def __init__(self):
        """Initialize visualizer"""
        plt.style.use('seaborn-v0_8')
        self.fig, self.axes = plt.subplots(3, 1, figsize=(12, 10))
        
    def plot_raw_csi(self, csi_data, ax):
        """
        Plot raw CSI amplitude data
        
        Args:
            csi_data (numpy.ndarray): CSI amplitude data
            ax (matplotlib.axes): Axis to plot on
        """
        if len(csi_data) == 0:
            return
            
        ax.clear()
        ax.set_title('Raw CSI Amplitude Data')
        ax.set_xlabel('Time (samples)')
        ax.set_ylabel('Amplitude')
        
        # Plot each subcarrier
        for i in range(min(5, csi_data.shape[1])):  # Plot first 5 subcarriers
            ax.plot(csi_data[:, i], alpha=0.7, label=f'Subcarrier {i+1}')
            
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def plot_breathing_signal(self, breathing_signal, ax):
        """
        Plot extracted breathing signal
        
        Args:
            breathing_signal (numpy.ndarray): Filtered breathing signal
            ax (matplotlib.axes): Axis to plot on
        """
        if len(breathing_signal) == 0:
            return
            
        ax.clear()
        ax.set_title('Extracted Breathing Signal')
        ax.set_xlabel('Time (samples)')
        ax.set_ylabel('Normalized Amplitude')
        ax.plot(breathing_signal, color='green', linewidth=2)
        ax.grid(True, alpha=0.3)
    
    def plot_variance_analysis(self, csi_data, ax):
        """
        Plot variance analysis across subcarriers
        
        Args:
            csi_data (numpy.ndarray): CSI amplitude data
            ax (matplotlib.axes): Axis to plot on
        """
        if len(csi_data) == 0:
            return
            
        ax.clear()
        variance = np.var(csi_data, axis=0)
        mean_variance = np.mean(variance)
        
        ax.set_title(f'CSI Variance Analysis (Mean: {mean_variance:.4f})')
        ax.set_xlabel('Subcarrier Index')
        ax.set_ylabel('Variance')
        ax.bar(range(len(variance)), variance, alpha=0.7, color='purple')
        ax.axhline(y=0.15, color='red', linestyle='--', label='Presence Threshold')
        ax.axhline(y=0.05, color='orange', linestyle='--', label='Breathing Threshold')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def update_plots(self, csi_data, breathing_signal):
        """
        Update all plots with new data
        
        Args:
            csi_data (numpy.ndarray): CSI amplitude data
            breathing_signal (numpy.ndarray): Filtered breathing signal
        """
        self.plot_raw_csi(csi_data, self.axes[0])
        self.plot_breathing_signal(breathing_signal, self.axes[1])
        self.plot_variance_analysis(csi_data, self.axes[2])
        
        plt.tight_layout()
        plt.draw()
        plt.pause(0.01)
    
    def visualize_real_time(self, interface='wlan0', duration=5):
        """
        Real-time visualization of CSI data and detection
        
        Args:
            interface (str): Network interface
            duration (int): Capture duration per cycle
        """
        print("Starting real-time CSI visualization...")
        print("Press Ctrl+C to stop")
        
        capture = CSICapture(interface)
        detector = PresenceDetector(interface, capture_duration=duration)
        
        plt.ion()
        plt.show()
        
        try:
            while True:
                # Capture CSI data
                csi_data = capture.capture_csi(duration=duration)
                
                # Detect presence and extract breathing signal
                presence, breathing, variance = detector.detect_presence(csi_data)
                breathing_signal = detector.extract_breathing_signal(csi_data)
                breathing_rate = detector.estimate_breathing_rate(breathing_signal)
                
                # Update plots
                self.update_plots(csi_data, breathing_signal)
                
                # Update title with detection status
                status = "No presence"
                if presence:
                    status = "Presence detected (motion)"
                elif breathing:
                    status = f"Breathing detected ({breathing_rate:.1f} BPM)"
                
                self.fig.suptitle(f"CSI Analysis - {status} | Variance: {variance:.4f}", 
                                fontsize=14, fontweight='bold')
                
        except KeyboardInterrupt:
            print("\nVisualization stopped")
        
        plt.ioff()
        plt.close()
    
    def visualize_from_file(self, filename):
        """
        Visualize CSI data from file
        
        Args:
            filename (str): File containing CSI data
        """
        print(f"Loading CSI data from {filename}...")
        
        capture = CSICapture()
        csi_data = capture.load_csi_data(filename)
        
        detector = PresenceDetector()
        breathing_signal = detector.extract_breathing_signal(csi_data)
        
        # Create figure
        fig, axes = plt.subplots(3, 1, figsize=(12, 10))
        
        # Plot data
        self.plot_raw_csi(csi_data, axes[0])
        self.plot_breathing_signal(breathing_signal, axes[1])
        self.plot_variance_analysis(csi_data, axes[2])
        
        # Add overall title
        presence, breathing, variance = detector.detect_presence(csi_data)
        breathing_rate = detector.estimate_breathing_rate(breathing_signal)
        
        status = "No presence"
        if presence:
            status = "Presence detected (motion)"
        elif breathing:
            status = f"Breathing detected ({breathing_rate:.1f} BPM)"
        
        fig.suptitle(f"CSI Analysis - {status} | Variance: {variance:.4f}", 
                    fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.show()

def main():
    parser = argparse.ArgumentParser(description='CSI Visualization Tool')
    parser.add_argument('--interface', type=str, default='wlan0',
                       help='Network interface for CSI capture')
    parser.add_argument('--duration', type=int, default=5,
                       help='Capture duration in seconds')
    parser.add_argument('--file', type=str,
                       help='Load CSI data from file instead of real-time capture')
    parser.add_argument('--real-time', action='store_true',
                       help='Run real-time visualization')
    
    args = parser.parse_args()
    
    visualizer = CSIVisualizer()
    
    if args.file:
        # Visualize from file
        visualizer.visualize_from_file(args.file)
    elif args.real_time:
        # Real-time visualization
        visualizer.visualize_real_time(interface=args.interface, duration=args.duration)
    else:
        # Default: real-time visualization
        visualizer.visualize_real_time(interface=args.interface, duration=args.duration)

if __name__ == '__main__':
    main()
