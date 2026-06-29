"""Signal preprocessing and feature extraction for seismic data.

Research-focused preprocessing pipeline for earthquake detection with:
- Statistical normalization for noise reduction
- Sliding window segmentation for temporal feature extraction
- Multi-scale feature engineering
- Research reproducibility via logging and configuration tracking

References:
- Bandpass filtering range: 0.1-25 Hz (seismic frequency band)
- Normalization: Z-score normalization (mean removal, std division)
- Features: statistical measures (mean, std, max, min, RMS, energy)
"""

import logging
from typing import Tuple

import numpy as np

logger = logging.getLogger(__name__)


def normalize_signal(window: np.ndarray) -> np.ndarray:
    """Normalize a window of accelerometer readings.

    Applies Z-score normalization (standardization) to remove DC offset
    and scale to unit variance.

    Args:
        window: Input signal array of shape (n_samples, n_channels)

    Returns:
        Normalized signal with zero mean and unit variance
    """
    if window.size == 0:
        logger.warning("Empty window provided to normalize_signal")
        return window

    mean = np.mean(window, axis=0)
    std = np.std(window, axis=0)

    # Avoid division by zero
    std = np.where(std == 0, 1.0, std)

    normalized = (window - mean) / std

    logger.debug(
        f"Normalized signal: mean={np.mean(normalized):.6f}, "
        f"std={np.std(normalized):.6f}"
    )

    return normalized


def create_sliding_window(
    samples: np.ndarray,
    window_size: int
) -> np.ndarray:
    """Extract fixed-length sliding windows from raw samples.

    Args:
        samples: Input samples of shape (n_samples, n_channels)
        window_size: Number of samples per window

    Returns:
        Array of windows with shape
        (n_windows, window_size, n_channels)
    """
    if samples.shape[0] < window_size:
        logger.warning(
            f"Insufficient samples ({samples.shape[0]}) "
            f"for window size {window_size}"
        )

        return np.empty((0, window_size, samples.shape[1]))

    windows = np.lib.stride_tricks.sliding_window_view(
        samples,
        window_shape=(window_size, samples.shape[1])
    )

    result = windows.reshape(
        -1,
        window_size,
        samples.shape[1]
    )

    logger.debug(
        f"Created {result.shape[0]} windows of size {window_size}"
    )

    return result


def extract_features(
    window: np.ndarray
) -> Tuple[np.ndarray, dict]:
    """Extract lightweight waveform features for inference.

    Features:
    - Mean
    - Standard deviation
    - Maximum
    - Minimum
    - RMS energy
    - Total energy

    Args:
        window: Signal window of shape
                (n_samples, n_channels)

    Returns:
        Tuple of:
        - feature vector
        - feature metadata dictionary
    """

    features = np.hstack([
        np.mean(window, axis=0),
        np.std(window, axis=0),
        np.max(window, axis=0),
        np.min(window, axis=0),
    ])

    feature_dict = {
        "rms": float(np.sqrt(np.mean(window ** 2))),
        "energy": float(np.sum(window ** 2)),
        "peak_amplitude": float(np.max(np.abs(window))),
    }

    logger.debug(
        f"Extracted features: "
        f"shape={features.shape}, "
        f"energy={feature_dict['energy']:.4f}"
    )

    return features, feature_dict
