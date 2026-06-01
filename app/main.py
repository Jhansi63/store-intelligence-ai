from fastapi import FastAPI
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine
from app.models import Base, Event, EventCreate
from sqlalchemy import func
app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "API Running"
    }


@app.post("/events/ingest")
def ingest_event(event: EventCreate):

    db: Session = SessionLocal()

    new_event = Event(
        event_id=str(event.event_id),
        store_id=event.store_id,
        camera_id=event.camera_id,
        visitor_id=event.visitor_id,
        event_type=event.event_type,
        timestamp=str(event.timestamp),
        zone_id=event.zone_id,
        dwell_ms=event.dwell_ms,
        is_staff=event.is_staff,
        confidence=event.confidence
    )

    db.add(new_event)
    db.commit()

    return {
        "status": "saved to database"
    }
@app.get("/stores/{store_id}/metrics")
def get_metrics(store_id: str):

    db: Session = SessionLocal()

    # Total events
    total_events = db.query(Event).filter(
        Event.store_id == store_id
    ).count()

    # Unique visitors excluding staff
    unique_visitors = db.query(
        func.count(func.distinct(Event.visitor_id))
    ).filter(
        Event.store_id == store_id,
        Event.is_staff == False
    ).scalar()

    # Purchasing visitors
    purchasing_visitors = db.query(
        func.count(func.distinct(Event.visitor_id))
    ).filter(
        Event.store_id == store_id,
        Event.event_type == "PURCHASE",
        Event.is_staff == False
    ).scalar()

    # Conversion rate
    conversion_rate = 0

    if unique_visitors > 0:
        conversion_rate = (
            purchasing_visitors / unique_visitors
        ) * 100

    return {
        "store_id": store_id,
        "total_events": total_events,
        "unique_visitors": unique_visitors,
        "purchasing_visitors": purchasing_visitors,
        "conversion_rate": round(conversion_rate, 2)
    }
@app.get("/stores/{store_id}/funnel")
def get_funnel(store_id: str):

    db: Session = SessionLocal()

    # ENTRY visitors
    entry_visitors = db.query(
        func.count(func.distinct(Event.visitor_id))
    ).filter(
        Event.store_id == store_id,
        Event.event_type == "ENTRY",
        Event.is_staff == False
    ).scalar()

    # ZONE visitors
    zone_visitors = db.query(
        func.count(func.distinct(Event.visitor_id))
    ).filter(
        Event.store_id == store_id,
        Event.event_type == "ZONE_ENTER",
        Event.is_staff == False
    ).scalar()

    # BILLING visitors
    billing_visitors = db.query(
        func.count(func.distinct(Event.visitor_id))
    ).filter(
        Event.store_id == store_id,
        Event.zone_id == "BILLING",
        Event.is_staff == False
    ).scalar()

    # PURCHASE visitors
    purchase_visitors = db.query(
        func.count(func.distinct(Event.visitor_id))
    ).filter(
        Event.store_id == store_id,
        Event.event_type == "PURCHASE",
        Event.is_staff == False
    ).scalar()

    return {
        "store_id": store_id,

        "funnel": {
            "entry": entry_visitors,
            "zone_visit": zone_visitors,
            "billing": billing_visitors,
            "purchase": purchase_visitors
        }
    }
@app.get("/stores/{store_id}/anomalies")
def get_anomalies(store_id: str):

    db: Session = SessionLocal()

    anomalies = []

    # Queue spike detection
    billing_count = db.query(Event).filter(
        Event.store_id == store_id,
        Event.zone_id == "BILLING"
    ).count()

    if billing_count > 5:
        anomalies.append({
            "type": "QUEUE_SPIKE",
            "severity": "WARN",
            "message": "Billing queue unusually high",
            "suggested_action": "Open additional billing counter"
        })

    # Low conversion detection
    unique_visitors = db.query(
        func.count(func.distinct(Event.visitor_id))
    ).filter(
        Event.store_id == store_id,
        Event.is_staff == False
    ).scalar()

    purchasing_visitors = db.query(
        func.count(func.distinct(Event.visitor_id))
    ).filter(
        Event.store_id == store_id,
        Event.event_type == "PURCHASE",
        Event.is_staff == False
    ).scalar()

    conversion_rate = 0

    if unique_visitors > 0:
        conversion_rate = (
            purchasing_visitors / unique_visitors
        ) * 100

    if conversion_rate < 20:
        anomalies.append({
            "type": "LOW_CONVERSION",
            "severity": "CRITICAL",
            "message": "Conversion rate below expected threshold",
            "suggested_action": "Inspect staffing and customer engagement"
        })

    # Empty store detection
    if unique_visitors == 0:
        anomalies.append({
            "type": "EMPTY_STORE",
            "severity": "INFO",
            "message": "No visitors detected",
            "suggested_action": "Verify store traffic and camera feed"
        })

    return {
        "store_id": store_id,
        "anomalies": anomalies
    }