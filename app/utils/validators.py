"""Validation utilities for the application."""

from typing import Any, List


def validate_sensor_data(data: List[float], min_length: int = 1) -> bool:
    """Validate sensor data format and length."""
    if not isinstance(data, list):
        return False
    if len(data) < min_length:
        return False
    return all(isinstance(x, (int, float)) for x in data)


def validate_confidence_score(score: float) -> bool:
    """Validate that confidence score is between 0 and 1."""
    return 0 <= score <= 1


def validate_required_fields(data: dict, required_fields: List[str]) -> bool:
    """Check if all required fields are present in data."""
    return all(field in data for field in required_fields)
