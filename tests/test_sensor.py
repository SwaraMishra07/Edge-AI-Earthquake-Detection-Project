"""Tests for sensor functionality."""

import pytest
from app.sensor import Sensor


class TestSensor:
    """Test sensor reading and processing."""
    
    @pytest.fixture
    def sensor(self):
        """Create sensor for testing."""
        config = {'SENSOR_SAMPLE_RATE': 100}
        return Sensor(config)
    
    def test_sensor_initialization(self, sensor):
        """Test sensor initialization."""
        assert sensor is not None
    
    def test_sensor_reading(self, sensor):
        """Test reading sensor data."""
        reading = sensor.read()
        assert reading is not None
