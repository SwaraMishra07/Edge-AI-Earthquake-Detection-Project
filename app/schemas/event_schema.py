"""Schema for earthquake event data."""

from pydantic import BaseModel
from datetime import datetime
from typing import List


class EventSchema(BaseModel):
    """Schema for earthquake event."""
    
    event_id: str
    timestamp: datetime
    magnitude: float
    latitude: float
    longitude: float
    depth: float
    confidence: float
    sensor_readings: List[float]
    
    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "event_id": "EVT001",
                "timestamp": "2024-01-01T12:00:00Z",
                "magnitude": 5.2,
                "latitude": 37.5,
                "longitude": -122.3,
                "depth": 10.5,
                "confidence": 0.95,
                "sensor_readings": [0.1, 0.2, 0.15]
            }
        }
