import re
from typing import List
import logging
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import ValidationError
from models import Event, SessionLocal, EventCreate, EventResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()


def validate_event_data(event_data: EventCreate):
    try:
        return EventCreate(**event_data.dict())
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e.errors()))


def log_event_details(operation, event_bucket, event_id=None, event=None):
    msg = f"{operation} request to /v1/{event_bucket}"
    if event_id:
        msg += f"/{event_id}"
    if event:
        msg += f" - Event details: {event}"
    logger.info(msg)


@app.get("/")
def read_root():
    return {"Hello": "World"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


ALLOWED_BUCKET_PATTERN = re.compile(r'^[a-zA-Z0-9_-]+$')


@app.put("/v1/{event_bucket}/", response_model=EventResponse)
def store_event(event_bucket: str, event_data: EventCreate = Depends(validate_event_data), db: Session = Depends(get_db)):
    try:
        if not ALLOWED_BUCKET_PATTERN.match(event_bucket):
            raise HTTPException(status_code=422, detail="Invalid Event Bucket name")

        db_event = Event(title=event_data.title, message=event_data.message, bucket=event_bucket)
        db.add(db_event)
        db.commit()
        db.refresh(db_event)

        # Logare eveniment
        log_event_details("Event stored", event_bucket, event=db_event)

        return db_event  # Returnează întregul obiect, inclusiv ID-ul
    except Exception as e:
        # Logare eroare
        logger.error(f"Internal Server Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.get("/v1/{event_bucket}/", response_model=List[int])
def get_event_ids(event_bucket: str, db: Session = Depends(get_db)):
    # Logare acces la endpoint
    log_event_details("GET", event_bucket)

    event_ids = db.query(Event.id).filter(Event.bucket == event_bucket).all()
    return [event_id[0] for event_id in event_ids]


@app.get("/v1/{event_bucket}/{event_id}", response_model=EventResponse)
def get_event_details(event_bucket: str, event_id: int, db: Session = Depends(get_db)):
    # Logare acces la endpoint
    log_event_details("GET", event_bucket, event_id)

    db_event = db.query(Event).filter(Event.bucket == event_bucket, Event.id == event_id).first()
    if db_event is None:
        # Logare eveniment negăsit
        logger.warning(f"Event not found for bucket={event_bucket}, id={event_id}")
        raise HTTPException(status_code=404, detail="Event not found")

    # Logare detalii eveniment
    log_event_details("Event details retrieved", event_bucket, event_id, db_event)
    return db_event
