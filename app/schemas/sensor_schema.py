"""Schema for sensor data."""

from pydantic import BaseModel
from datetime import datetime
from typing import List


class SensorReadingSchema(BaseModel):
    """Schema for sensor reading."""
    
    sensor_id: str
    timestamp: datetime
    acceleration_x: float
    acceleration_y: float
    acceleration_z: float
    temperature: float
    
    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "sensor_id": "SENSOR001",
                "timestamp": "2024-01-01T12:00:00Z",
                "acceleration_x": 0.1,
                "acceleration_y": 0.2,
                "acceleration_z": 0.15,
                "temperature": 25.5
            }
        }
