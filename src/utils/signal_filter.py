#!/usr/bin/env python3
"""
Signal Filter Module
Advanced signal processing for CSI data
"""

import numpy as np
from scipy import signal

def bandpass_filter(data, lowcut, highcut, fs, order=4):
    """
    Apply bandpass filter to data
    
    Args:
        data (numpy.ndarray): Input signal
        lowcut (float): Low cutoff frequency (Hz)
        highcut (float): High cutoff frequency (Hz)
        fs (float): Sampling frequency (Hz)
        order (int): Filter order
        
    Returns:
        numpy.ndarray: Filtered signal
    """
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    
    b, a = signal.butter(order, [low, high], btype='band')
    return signal.filtfilt(b, a, data)

def lowpass_filter(data, cutoff, fs, order=4):
    """
    Apply lowpass filter to data
    
    Args:
        data (numpy.ndarray): Input signal
        cutoff (float): Cutoff frequency (Hz)
        fs (float): Sampling frequency (Hz)
        order (int): Filter order
        
    Returns:
        numpy.ndarray: Filtered signal
    """
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    
    b, a = signal.butter(order, normal_cutoff, btype='low')
    return signal.filtfilt(b, a, data)

def highpass_filter(data, cutoff, fs, order=4):
    """
    Apply highpass filter to data
    
    Args:
        data (numpy.ndarray): Input signal
        cutoff (float): Cutoff frequency (Hz)
        fs (float): Sampling frequency (Hz)
        order (int): Filter order
        
    Returns:
        numpy.ndarray: Filtered signal
    """
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    
    b, a = signal.butter(order, normal_cutoff, btype='high')
    return signal.filtfilt(b, a, data)

def moving_average(data, window_size=5):
    """
    Apply moving average filter
    
    Args:
        data (numpy.ndarray): Input signal
        window_size (int): Window size for moving average
        
    Returns:
        numpy.ndarray: Smoothed signal
    """
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

def normalize_signal(data):
    """
    Normalize signal to zero mean and unit variance
    
    Args:
        data (numpy.ndarray): Input signal
        
    Returns:
        numpy.ndarray: Normalized signal
    """
    if np.std(data) > 0:
        return (data - np.mean(data)) / np.std(data)
    else:
        return data - np.mean(data)

def remove_outliers(data, threshold=3.0):
    """
    Remove outliers using z-score method
    
    Args:
        data (numpy.ndarray): Input signal
        threshold (float): Z-score threshold for outlier detection
        
    Returns:
        numpy.ndarray: Signal with outliers removed
    """
    mean = np.mean(data)
    std = np.std(data)
    
    if std > 0:
        z_scores = np.abs((data - mean) / std)
        return data[z_scores < threshold]
    else:
        return data

def extract_breathing_features(csi_data, fs=20):
    """
    Extract breathing-related features from CSI data
    
    Args:
        csi_data (numpy.ndarray): CSI amplitude data
        fs (float): Sampling frequency (Hz)
        
    Returns:
        dict: Extracted breathing features
    """
    # Average across subcarriers
    mean_signal = np.mean(csi_data, axis=1)
    
    # Normalize
    mean_signal = normalize_signal(mean_signal)
    
    # Bandpass filter for breathing range (0.1-0.5 Hz)
    breathing_signal = bandpass_filter(mean_signal, 0.1, 0.5, fs)
    
    # Calculate features
    variance = np.var(breathing_signal)
    mean_amplitude = np.mean(np.abs(breathing_signal))
    
    # Find peaks for breathing rate estimation
    peaks, _ = signal.find_peaks(breathing_signal, distance=5)
    
    features = {
        'variance': variance,
        'mean_amplitude': mean_amplitude,
        'num_peaks': len(peaks),
        'breathing_signal': breathing_signal,
        'peak_indices': peaks
    }
    
    return features

def calculate_spectral_features(signal_data, fs=20):
    """
    Calculate spectral features using FFT
    
    Args:
        signal_data (numpy.ndarray): Input signal
        fs (float): Sampling frequency (Hz)
        
    Returns:
        dict: Spectral features
    """
    # Compute FFT
    fft_result = np.fft.fft(signal_data)
    frequencies = np.fft.fftfreq(len(signal_data), 1/fs)
    
    # Get magnitude spectrum
    magnitude = np.abs(fft_result)
    
    # Find dominant frequency
    dominant_freq_idx = np.argmax(magnitude[1:len(frequencies)//2]) + 1
    dominant_freq = frequencies[dominant_freq_idx]
    
    # Calculate power in breathing band (0.1-0.5 Hz)
    breathing_band = (frequencies >= 0.1) & (frequencies <= 0.5)
    breathing_power = np.sum(magnitude[breathing_band])
    
    features = {
        'dominant_frequency': dominant_freq,
        'breathing_power': breathing_power,
        'total_power': np.sum(magnitude),
        'frequencies': frequencies,
        'magnitude': magnitude
    }
    
    return features
