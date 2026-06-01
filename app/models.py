from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

from sqlalchemy import Column, String, Integer, Boolean, Float
from app.database import Base


# -----------------------------
# Pydantic Model (API Validation)
# -----------------------------
class EventCreate(BaseModel):
    event_id: UUID
    store_id: str
    camera_id: str
    visitor_id: str
    event_type: str
    timestamp: datetime
    zone_id: Optional[str] = None
    dwell_ms: int
    is_staff: bool
    confidence: float


# -----------------------------
# SQLAlchemy Model (Database)
# -----------------------------
class Event(Base):
    __tablename__ = "events"

    event_id = Column(String, primary_key=True, index=True)
    store_id = Column(String)
    camera_id = Column(String)
    visitor_id = Column(String)
    event_type = Column(String)
    timestamp = Column(String)
    zone_id = Column(String)
    dwell_ms = Column(Integer)
    is_staff = Column(Boolean)
    confidence = Column(Float)