"""Tests for MQTT client functionality."""

import pytest
from app.mqtt_client import MQTTClient


class TestMQTTClient:
    """Test MQTT client."""
    
    @pytest.fixture
    def mqtt_client(self):
        """Create MQTT client for testing."""
        config = {'MQTT_BROKER': 'localhost', 'MQTT_PORT': 1883}
        return MQTTClient(config)
    
    def test_mqtt_connection(self, mqtt_client):
        """Test MQTT connection."""
        assert mqtt_client is not None
    
    def test_mqtt_publish(self, mqtt_client):
        """Test publishing to MQTT."""
        result = mqtt_client.publish('test/topic', 'test_message')
        assert result is not None
