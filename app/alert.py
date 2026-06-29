from datetime import datetime


def build_alert(event_id: str, confidence: float, message: str) -> dict:
    return {
        "event_id": event_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "confidence": confidence,
        "message": message,
    }


def should_alert(local_confidence: float, threshold: float) -> bool:
    return local_confidence >= threshold
