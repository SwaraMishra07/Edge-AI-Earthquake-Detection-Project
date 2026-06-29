"""Signal preprocessing and feature extraction for seismic data."""

import logging
from typing import Tuple

import numpy as np

logger = logging.getLogger(__name__)


def normalize_signal(window: np.ndarray) -> np.ndarray:
    """Normalize seismic signal using Z-score normalization."""
    if window.size == 0:
        logger.warning("Empty window provided to normalize_signal")
        return window

    mean = np.mean(window, axis=0)
    std = np.std(window, axis=0)

    # Avoid division by zero
    std = np.where(std == 0, 1.0, std)

    normalized = (window - mean) / std

    logger.debug(
        f"Normalized signal: "
        f"mean={np.mean(normalized):.6f}, "
        f"std={np.std(normalized):.6f}"
    )

    return normalized


def create_sliding_window(
    samples: np.ndarray,
    window_size: int
) -> np.ndarray:
    """Create sliding windows from seismic samples."""
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
        f"Created {result.shape[0]} windows "
        f"of size {window_size}"
    )

    return result


def extract_features(
    window: np.ndarray
) -> Tuple[np.ndarray, dict]:
    """Extract statistical features from waveform."""

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