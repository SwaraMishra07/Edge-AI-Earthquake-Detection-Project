"""MQTT client for distributed earthquake detection system communication.

Provides pub/sub functionality for sensor data, alerts, and consensus messages
across the edge network. Includes automatic reconnection, error handling,
and comprehensive logging for research reproducibility.
"""

import json
import logging
from typing import Optional, Callable, Dict, Any
from functools import wraps

from paho.mqtt import client as mqtt

from app.config import mqtt_config, research_config
from app.utils.logger import setup_logger

logger = setup_logger(__name__, logging.getLevelName(research_config.log_level))


class MQTTConnectionError(Exception):
    """Raised when MQTT connection fails."""
    pass


class MQTTPublishError(Exception):
    """Raised when MQTT publish operation fails."""
    pass


def handle_mqtt_errors(func: Callable) -> Callable:
    """Decorator for handling MQTT errors with logging and retries."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except mqtt.MQTTException as e:
            logger.error(f"MQTT error in {func.__name__}: {e}", exc_info=True)
            raise MQTTConnectionError(f"MQTT operation failed: {e}") from e
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {e}", exc_info=True)
            raise
    return wrapper


class MQTTClient:
    """Managed MQTT client with automatic reconnection and error handling."""
    
    def __init__(self, client_id: str, on_message: Optional[Callable] = None):
        """Initialize MQTT client.
        
        Args:
            client_id: Unique identifier for this client
            on_message: Optional callback for received messages
        """
        self.client_id = client_id
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
        self._setup_callbacks(on_message)
        self._connected = False
        logger.info(f"MQTT client '{client_id}' initialized")
    
    def _setup_callbacks(self, on_message: Optional[Callable]) -> None:
        """Configure callback functions."""
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_publish = self._on_publish
        if on_message:
            self.client.on_message = on_message
    
    def _on_connect(self, client, userdata, connect_flags, reason_code, properties):
        """Handle connection callback."""
        if reason_code == 0:
            self._connected = True
            logger.info(f"MQTT connected: {self.client_id}")
        else:
            logger.error(f"MQTT connection failed with code {reason_code}")
    
    def _on_disconnect(self, client, userdata, disconnect_flags, reason_code, properties):
        """Handle disconnection callback."""
        self._connected = False
        logger.warning(f"MQTT disconnected: code={reason_code}")
    
    def _on_publish(self, client, userdata, mid, reason_code, properties):
        """Handle publish callback."""
        logger.debug(f"Message published: mid={mid}, reason_code={reason_code}")
    
    @property
    def is_connected(self) -> bool:
        """Check connection status."""
        return self._connected
    
    @handle_mqtt_errors
    def connect(self, hostname: Optional[str] = None, port: Optional[int] = None) -> None:
        """Connect to MQTT broker.
        
        Args:
            hostname: MQTT broker hostname (uses config if not provided)
            port: MQTT broker port (uses config if not provided)
        """
        hostname = hostname or mqtt_config.broker
        port = port or mqtt_config.port
        
        if mqtt_config.username and mqtt_config.password:
            self.client.username_pw_set(mqtt_config.username, mqtt_config.password)
        
        logger.info(f"Connecting to {hostname}:{port}")
        self.client.connect(hostname, port, mqtt_config.keepalive)
        self.client.loop_start()
    
    @handle_mqtt_errors
    def disconnect(self) -> None:
        """Disconnect from MQTT broker."""
        logger.info(f"Disconnecting MQTT client: {self.client_id}")
        self.client.loop_stop()
        self.client.disconnect()
        self._connected = False
    
    @handle_mqtt_errors
    def subscribe(self, topic: str, qos: int = 1) -> None:
        """Subscribe to a topic.
        
        Args:
            topic: Topic to subscribe to
            qos: Quality of service (0, 1, or 2)
        """
        logger.info(f"Subscribing to topic: {topic}")
        self.client.subscribe(topic, qos=qos)
    
    @handle_mqtt_errors
    def publish(self, topic: str, payload: Dict[str, Any], qos: int = 1, retain: bool = False) -> int:
        """Publish message to topic.
        
        Args:
            topic: Target topic
            payload: Message payload as dictionary
            qos: Quality of service
            retain: Whether to retain the message
        
        Returns:
            Message ID
        
        Raises:
            MQTTPublishError: If publish fails
        """
        message = json.dumps(payload)
        logger.debug(f"Publishing to {topic}: {message[:100]}...")
        
        result = self.client.publish(topic, message, qos=qos, retain=retain)
        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            raise MQTTPublishError(f"Publish failed with code {result.rc}")
        
        return result.mid


# Backward compatibility functions
def create_client(client_id: str, on_message: Optional[Callable] = None) -> MQTTClient:
    """Create and return an MQTT client.
    
    Deprecated: Use MQTTClient class directly.
    """
    return MQTTClient(client_id, on_message)


def connect_and_subscribe(client: MQTTClient, topic: Optional[str] = None) -> MQTTClient:
    """Connect to broker and subscribe to topic.
    
    Deprecated: Use MQTTClient.connect() and subscribe() methods directly.
    """
    client.connect()
    client.subscribe(topic or mqtt_config.topic_alerts)
    return client


def publish_alert(client: MQTTClient, payload: Dict[str, Any]) -> int:
    """Publish alert message.
    
    Deprecated: Use MQTTClient.publish() method directly.
    """
    return client.publish(mqtt_config.topic_alerts, payload)
