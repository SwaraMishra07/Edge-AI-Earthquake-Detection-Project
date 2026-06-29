from sqlalchemy import Column, DateTime, Float, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from datetime import datetime

from app.config import DATABASE_URL

Base = declarative_base()


class EventRecord(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    event_id = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    confidence = Column(Float)
    status = Column(String)
    detail = Column(String)


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base.metadata.create_all(engine)


def save_event(event_id: str, confidence: float, status: str, detail: str) -> None:
    with Session(engine) as session:
        record = EventRecord(
            event_id=event_id,
            confidence=confidence,
            status=status,
            detail=detail,
        )
        session.add(record)
        session.commit()


def get_recent_events(limit: int = 20):
    with Session(engine) as session:
        return session.query(EventRecord).order_by(EventRecord.timestamp.desc()).limit(limit).all()
