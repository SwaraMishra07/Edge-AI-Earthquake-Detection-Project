\"\"\"Signal preprocessing and feature extraction for seismic data.

Research-focused preprocessing pipeline for earthquake detection with:
- Statistical normalization for noise reduction
- Sliding window segmentation for temporal feature extraction
- Multi-scale feature engineering
- Research reproducibility via logging and configuration tracking

References:
- Bandpass filtering range: 0.1-25 Hz (seismic frequency band)
- Normalization: Z-score normalization (mean removal, std division)
- Features: statistical measures (mean, std, max, min, RMS, energy)
\"\"\"\n\nimport logging\nimport numpy as np\nfrom typing import Tuple\n\nlogger = logging.getLogger(__name__)\n\n\ndef normalize_signal(window: np.ndarray) -> np.ndarray:\n    \"\"\"Normalize a window of accelerometer readings.\n    \n    Applies Z-score normalization (standardization) to remove DC offset\n    and scale to unit variance. This is crucial for model input consistency.\n    \n    Args:\n        window: Input signal array of shape (n_samples, n_channels)\n    \n    Returns:\n        Normalized signal with zero mean and unit variance\n    \"\"\"\n    if window.size == 0:\n        logger.warning(\"Empty window provided to normalize_signal\")\n        return window\n    \n    mean = np.mean(window, axis=0)\n    std = np.std(window, axis=0)\n    std = np.where(std == 0, 1.0, std)  # Avoid division by zero\n    normalized = (window - mean) / std\n    \n    logger.debug(f\"Normalized signal: mean={np.mean(normalized):.6f}, std={np.std(normalized):.6f}\")\n    return normalized


def create_sliding_window(samples: np.ndarray, window_size: int) -> np.ndarray:\n    \"\"\"Extract fixed-length sliding windows from raw samples.\n    \n    Uses stride tricks for memory-efficient windowing. Each window contains\n    'window_size' consecutive samples, enabling temporal analysis of seismic signals.\n    \n    Args:\n        samples: Input samples of shape (n_samples, n_channels)\n        window_size: Number of samples per window\n    \n    Returns:\n        Array of windows with shape (n_windows, window_size, n_channels)\n    \"\"\"\n    if samples.shape[0] < window_size:\n        logger.warning(f\"Insufficient samples ({samples.shape[0]}) for window size {window_size}\")\n        return np.empty((0, window_size, samples.shape[1]))\n    \n    windows = np.lib.stride_tricks.sliding_window_view(samples, window_shape=(window_size, samples.shape[1]))\n    result = windows.reshape(-1, window_size, samples.shape[1])\n    \n    logger.debug(f\"Created {result.shape[0]} windows of size {window_size}\")\n    return result


def extract_features(window: np.ndarray) -> np.ndarray:
    """Extract lightweight waveform features for inference."""
    return np.hstack([
        np.mean(window, axis=0),
        np.std(window, axis=0),
        np.max(window, axis=0),Tuple[np.ndarray, dict]:\n    \"\"\"Extract lightweight waveform features for inference.\n    \n    Computes statistical features across each channel for model input.\n    Features selected based on seismic signal characteristics:\n    - Mean: DC offset and baseline\n    - Std: Signal variability and energy content\n    - Max/Min: Peak amplitude (intensity indicator)\n    - RMS: Root-mean-square energy\n    - Energy: Summed squared amplitude\n    \n    Args:\n        window: Signal window of shape (n_samples, n_channels)\n    \n    Returns:\n        Tuple of (feature_vector, feature_dict)\n    \"\"\"\n    features = np.hstack([\n        np.mean(window, axis=0),\n        np.std(window, axis=0),\n        np.max(window, axis=0),\n        np.min(window, axis=0),\n    ])\n    \n    # Compute additional metrics for tracking\n    feature_dict = {\n        'rms': float(np.sqrt(np.mean(window ** 2))),\n        'energy': float(np.sum(window ** 2)),\n        'peak_amplitude': float(np.max(np.abs(window))),\n    }\n    \n    logger.debug(f\"Extracted features: shape={features.shape}, energy={feature_dict['energy']:.4f}\")\n    return features, feature_dict