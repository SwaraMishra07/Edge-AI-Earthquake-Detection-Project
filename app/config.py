"""Application configuration with research metadata and environment management.

This module provides centralized configuration for the Edge AI Earthquake Detection system,
including model parameters, sensor configuration, and research tracking settings.
"""

import os
import logging
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
NOTEBOOKS_DIR = BASE_DIR / "notebooks"
ARTIFACTS_DIR = BASE_DIR / ".research_artifacts"

# Ensure directories exist
for dir_path in [LOGS_DIR, DATA_DIR, ARTIFACTS_DIR]:
    dir_path.mkdir(exist_ok=True, parents=True)


@dataclass
class SensorConfig:
    """Sensor configuration and parameters."""
    sample_rate: int = int(os.getenv("SENSOR_SAMPLE_RATE", "100"))  # Hz
    channels: int = int(os.getenv("SENSOR_CHANNELS", "3"))  # X, Y, Z
    window_seconds: float = float(os.getenv("WINDOW_SECONDS", "2"))
    
    @property
    def window_size(self) -> int:
        """Calculate window size in samples."""
        return int(self.sample_rate * self.window_seconds)


@dataclass
class ModelConfig:
    """Model configuration and parameters."""
    model_path: Path = field(default_factory=lambda: MODEL_DIR / "earthquake_model.tflite")
    model_version: str = os.getenv("MODEL_VERSION", "1.0.0")
    quantization_aware: bool = os.getenv("QUANTIZATION_AWARE", "true").lower() == "true"
    inference_threshold: float = float(os.getenv("INFERENCE_THRESHOLD", "0.7"))
    
    def __post_init__(self):
        if not self.model_path.exists():
            logger.warning(f"Model not found at {self.model_path}")


@dataclass
class MQTTConfig:
    """MQTT broker configuration."""
    broker: str = os.getenv("MQTT_BROKER", "localhost")
    port: int = int(os.getenv("MQTT_PORT", "1883"))
    topic_alerts: str = os.getenv("MQTT_TOPIC_ALERTS", "edge/earthquake/alerts")
    topic_sensors: str = os.getenv("MQTT_TOPIC_SENSORS", "edge/earthquake/sensors")
    username: Optional[str] = os.getenv("MQTT_USERNAME")
    password: Optional[str] = os.getenv("MQTT_PASSWORD")
    keepalive: int = int(os.getenv("MQTT_KEEPALIVE", "60"))
    reconnect_delay: int = int(os.getenv("MQTT_RECONNECT_DELAY", "5"))


@dataclass
class AlertConfig:
    """Alert generation configuration."""
    magnitude_threshold: float = float(os.getenv("MAGNITUDE_THRESHOLD", "4.5"))
    confidence_threshold: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.8"))
    peer_confirmation_count: int = int(os.getenv("PEER_CONFIRMATION_COUNT", "2"))
    alert_timeout_seconds: int = int(os.getenv("ALERT_TIMEOUT", "300"))


@dataclass
class DatabaseConfig:
    """Database configuration."""
    url: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'earthquake.db'}")
    echo: bool = os.getenv("DB_ECHO", "false").lower() == "true"
    pool_size: int = int(os.getenv("DB_POOL_SIZE", "5"))
    max_overflow: int = int(os.getenv("DB_MAX_OVERFLOW", "10"))


@dataclass
class ResearchConfig:
    """Research and experiment tracking configuration."""
    experiment_id: str = os.getenv("EXPERIMENT_ID", f"exp_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    random_seed: int = int(os.getenv("RANDOM_SEED", "42"))
    track_experiments: bool = os.getenv("TRACK_EXPERIMENTS", "true").lower() == "true"
    save_intermediate_results: bool = os.getenv("SAVE_INTERMEDIATE", "true").lower() == "true"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    enable_profiling: bool = os.getenv("ENABLE_PROFILING", "false").lower() == "true"


# Global configuration instances
sensor_config = SensorConfig()
model_config = ModelConfig()
mqtt_config = MQTTConfig()
alert_config = AlertConfig()
database_config = DatabaseConfig()
research_config = ResearchConfig()

# Backward compatibility
DATABASE_URL = database_config.url
MQTT_BROKER = mqtt_config.broker
MQTT_PORT = mqtt_config.port
MQTT_TOPIC = mqtt_config.topic_alerts
SAMPLE_RATE = sensor_config.sample_rate
WINDOW_SECONDS = sensor_config.window_seconds
WINDOW_SIZE = sensor_config.window_size
ALERT_THRESHOLD = alert_config.confidence_threshold
PEER_CONFIRMATION_COUNT = alert_config.peer_confirmation_count
