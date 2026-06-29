"""Main entry point for the Edge AI Earthquake Detection Application."""

import logging
from app.config import Config
from app.sensor import Sensor
from app.preprocessing import Preprocessing
from app.inference import Inference
from app.mqtt_client import MQTTClient
from app.consensus import Consensus
from app.alert import Alert
from app.storage import Storage
from app.api import create_app

logger = logging.getLogger(__name__)


def main():
    """Initialize and run the main application."""
    config = Config()
    logger.info("Starting Edge AI Earthquake Detection System")
    
    # Initialize components
    sensor = Sensor(config)
    preprocessor = Preprocessing(config)
    inference_engine = Inference(config)
    mqtt_client = MQTTClient(config)
    consensus = Consensus(config)
    alert_system = Alert(config)
    storage = Storage(config)
    
    logger.info("All components initialized successfully")


if __name__ == "__main__":
    main()
