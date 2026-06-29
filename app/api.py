from fastapi import FastAPI
from app.storage import get_recent_events

app = FastAPI(title="Edge AI Earthquake Early Alerts")


@app.get("/")
def root():
    return {"status": "running", "service": "edge-ai-earthquake"}


@app.get("/events")
def events():
    records = get_recent_events()
    return [
        {
            "event_id": record.event_id,
            "timestamp": record.timestamp.isoformat(),
            "confidence": record.confidence,
            "status": record.status,
            "detail": record.detail,
        }
        for record in records
    ]
