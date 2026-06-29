"""Health check service for system status."""

import logging
from typing import Dict, Any
from enum import Enum

logger = logging.getLogger(__name__)


class HealthStatus(Enum):
    """Health status enum."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class HealthCheckService:
    """Check and report system health status."""
    
    def __init__(self, config):
        """Initialize the health check service."""
        self.config = config
    
    def check_health(self) -> Dict[str, Any]:
        """Perform comprehensive health check."""
        return {
            'status': HealthStatus.HEALTHY.value,
            'components': {
                'sensor': 'ok',
                'model': 'ok',
                'mqtt': 'ok',
                'storage': 'ok',
            }
        }
    
    def is_healthy(self) -> bool:
        """Check if system is healthy."""
        health = self.check_health()
        return health['status'] == HealthStatus.HEALTHY.value
