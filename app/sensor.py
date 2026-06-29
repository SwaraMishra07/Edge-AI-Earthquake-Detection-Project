"""Sensor data simulation and acquisition module.

Provides realistic seismic sensor simulation for research and testing.
Includes configurable noise models and event generation patterns.
"""

import logging
from typing import Optional
import numpy as np

logger = logging.getLogger(__name__)


def simulate_sensor_data(
    sample_rate: int,
    duration_seconds: float = 2.0
) -> np.ndarray:
    """Generate simulated seismic sensor data."""

    total_samples = int(sample_rate * duration_seconds)

    noise = np.random.normal(
        0,
        0.02,
        size=(total_samples, 3)
    )

    # Simulate a brief seismic event
    event = np.zeros((total_samples, 3))
    mid = total_samples // 2
    spike = np.linspace(0, 2.0, num=10)
    event[mid:mid + 10, 0] = spike

    return noise + event


class Sensor:
    """Simulated seismic sensor interface."""

    def __init__(
        self,
        sample_rate: int | dict | object = 100,
        duration_seconds: float = 2.0
    ):
        self.sample_rate = self._resolve_sample_rate(sample_rate)
        self.duration_seconds = duration_seconds

    def _resolve_sample_rate(self, sample_rate: int | dict | object) -> int:
        """Resolve the configured sample rate from common config shapes."""
        if isinstance(sample_rate, dict):
            return int(
                sample_rate.get("SENSOR_SAMPLE_RATE", sample_rate.get("sample_rate", 100))
            )

        if hasattr(sample_rate, "SENSOR_SAMPLE_RATE"):
            return int(getattr(sample_rate, "SENSOR_SAMPLE_RATE"))

        if hasattr(sample_rate, "sample_rate"):
            return int(getattr(sample_rate, "sample_rate"))

        return int(sample_rate)

    def read(self) -> np.ndarray:
        """Read current sensor values."""
        return self.read_data()

    def read_data(self) -> np.ndarray:
        """Read simulated sensor data."""

        data = simulate_sensor_data(
            self.sample_rate,
            self.duration_seconds
        )

        logger.debug(
            f"Generated sensor data with shape {data.shape}"
        )

        return data