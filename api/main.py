import re
import uuid
from typing import List
import logging
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from api.models import Event, SessionLocal, EventCreate, EventResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()


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
def store_event(event_bucket: str, event_data: EventCreate, db: Session = Depends(get_db)):
    try:
        if not ALLOWED_BUCKET_PATTERN.match(event_bucket):
            raise HTTPException(status_code=422, detail="Invalid Event Bucket name")

        new_uuid = str(uuid.uuid4())

        db_event = Event(id=new_uuid, title=event_data.title, message=event_data.message, bucket=event_bucket)
        db.add(db_event)
        db.commit()
        db.refresh(db_event)

        logger.info(f"Event stored: {db_event.__dict__}")

        return db_event
    except Exception as e:
        logger.error(f"Internal Server Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.get("/v1/{event_bucket}/", response_model=List[str])
def get_event_ids(event_bucket: str, db: Session = Depends(get_db)):
    logger.info(f"GET request to /v1/{event_bucket}/")

    event_ids = db.query(Event.id).filter(Event.bucket == event_bucket).all()
    return [str(event_id[0]) for event_id in event_ids]


@app.get("/v1/{event_bucket}/{event_id}", response_model=EventResponse)
def get_event_details(event_bucket: str, event_id: str, db: Session = Depends(get_db)):
    logger.info(f"GET request to /v1/{event_bucket}/{event_id}")

    db_event = db.query(Event).filter(Event.bucket == event_bucket, Event.id == event_id).first()
    if db_event is None:
        logger.warning(f"Event not found for bucket={event_bucket}, id={event_id}")
        raise HTTPException(status_code=404, detail="Event not found")

    logger.info(f"Event details retrieved: {db_event.__dict__}")
    return db_event
