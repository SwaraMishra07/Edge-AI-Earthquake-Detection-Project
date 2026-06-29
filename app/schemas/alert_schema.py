"""Schema for alert data."""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AlertSchema(BaseModel):
    """Schema for earthquake alert."""
    
    alert_id: str
    timestamp: datetime
    event_id: str
    magnitude: float
    urgency_level: str
    message: str
    affected_areas: list
    metadata: Optional[dict] = None
    
    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "alert_id": "ALR001",
                "timestamp": "2024-01-01T12:00:00Z",
                "event_id": "EVT001",
                "magnitude": 5.2,
                "urgency_level": "high",
                "message": "Earthquake detected",
                "affected_areas": ["Bay Area", "San Francisco"]
            }
        }
