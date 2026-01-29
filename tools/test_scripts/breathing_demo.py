#!/usr/bin/env python3
"""
Breathing Detection Demo
Demonstrates breathing detection using simulated CSI data
"""

import time
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def simulate_breathing_csi(duration=10, breathing_rate=15):
    """
    Simulate CSI data with breathing pattern
    
    Args:
        duration (int): Duration in seconds
        breathing_rate (float): Breathing rate in breaths per minute
        
    Returns:
        numpy.ndarray: Simulated CSI data with breathing pattern
    """
    # Calculate parameters
    fs = 20  # Sampling frequency (Hz)
    num_samples = duration * fs
    breathing_freq = breathing_rate / 60.0  # Convert to Hz
    
    # Create time array
    t = np.arange(num_samples) / fs
    
    # Simulate breathing signal (sine wave)
    breathing_signal = np.sin(2 * np.pi * breathing_freq * t)
    
    # Add some noise
    noise = np.random.normal(0, 0.1, num_samples)
    breathing_signal += noise
    
    # Simulate CSI data with 30 subcarriers
    num_subcarriers = 30
    csi_data = np.zeros((num_samples, num_subcarriers))
    
    # Each subcarrier has the breathing signal with different amplitudes
    for i in range(num_subcarriers):
        amplitude = 1.0 + 0.1 * i  # Different amplitudes for each subcarrier
        csi_data[:, i] = amplitude * breathing_signal + np.random.normal(0, 0.05, num_samples)
    
    return csi_data

def detect_breathing(csi_data, fs=20):
    """
    Detect breathing from CSI data
    
    Args:
        csi_data (numpy.ndarray): CSI amplitude data
        fs (float): Sampling frequency (Hz)
        
    Returns:
        dict: Detection results including breathing rate and signal
    """
    # Average across subcarriers
    mean_signal = np.mean(csi_data, axis=1)
    
    # Normalize
    mean_signal = (mean_signal - np.mean(mean_signal)) / np.std(mean_signal)
    
    # Bandpass filter for breathing range (0.1-0.5 Hz)
    lowcut = 0.1
    highcut = 0.5
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    
    b, a = signal.butter(4, [low, high], btype='band')
    filtered_signal = signal.filtfilt(b, a, mean_signal)
    
    # Find peaks
    peaks, _ = signal.find_peaks(filtered_signal, distance=5)
    
    # Calculate breathing rate
    if len(peaks) >= 2:
        peak_times = np.arange(len(filtered_signal))[peaks]
        time_diffs = np.diff(peak_times)
        avg_time_diff = np.mean(time_diffs)
        breathing_rate = 60.0 / (avg_time_diff / fs)
    else:
        breathing_rate = 0.0
    
    return {
        'breathing_rate': breathing_rate,
        'filtered_signal': filtered_signal,
        'peaks': peaks,
        'num_peaks': len(peaks)
    }

def plot_results(csi_data, detection_results, fs=20):
    """
    Plot CSI data and detection results
    
    Args:
        csi_data (numpy.ndarray): Original CSI data
        detection_results (dict): Detection results
        fs (float): Sampling frequency (Hz)
    """
    plt.figure(figsize=(15, 10))
    
    # Plot raw CSI data
    plt.subplot(3, 1, 1)
    for i in range(min(3, csi_data.shape[1])):
        plt.plot(csi_data[:, i], alpha=0.7, label=f'Subcarrier {i+1}')
    plt.title('Raw CSI Data (First 3 Subcarriers)')
    plt.xlabel('Samples')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot filtered breathing signal
    plt.subplot(3, 1, 2)
    plt.plot(detection_results['filtered_signal'], 'g-', linewidth=2)
    plt.plot(detection_results['peaks'], 
             detection_results['filtered_signal'][detection_results['peaks']], 
             'ro', markersize=8)
    plt.title(f'Filtered Breathing Signal ({detection_results["breathing_rate"]:.1f} BPM)')
    plt.xlabel('Samples')
    plt.ylabel('Normalized Amplitude')
    plt.grid(True, alpha=0.3)
    
    # Plot frequency spectrum
    plt.subplot(3, 1, 3)
    fft_result = np.fft.fft(detection_results['filtered_signal'])
    frequencies = np.fft.fftfreq(len(detection_results['filtered_signal']), 1/fs)
    magnitude = np.abs(fft_result)
    
    # Only plot positive frequencies
    pos_freq_mask = frequencies >= 0
    plt.plot(frequencies[pos_freq_mask], magnitude[pos_freq_mask])
    plt.title('Frequency Spectrum')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.xlim(0, 1.0)  # Focus on breathing frequency range
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def main():
    print("Breathing Detection Demo")
    print("======================")
    print("")
    
    # Test different breathing rates
    breathing_rates = [12, 15, 18, 22]
    
    for rate in breathing_rates:
        print(f"Testing breathing rate: {rate} BPM")
        
        # Simulate CSI data with breathing
        csi_data = simulate_breathing_csi(duration=10, breathing_rate=rate)
        
        # Detect breathing
        results = detect_breathing(csi_data)
        
        print(f"Detected breathing rate: {results['breathing_rate']:.1f} BPM")
        print(f"Number of peaks detected: {results['num_peaks']}")
        print("")
        
        # Plot results
        plot_results(csi_data, results)
        
        # Wait for user to continue
        input("Press Enter to continue to next test...")
    
    print("Demo completed!")

if __name__ == '__main__':
    main()
