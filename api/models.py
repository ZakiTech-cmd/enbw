import uuid

from sqlalchemy import create_engine, Column, Integer, String, StaticPool
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False}, poolclass=StaticPool)

Base = declarative_base()


class Event(Base):
    __tablename__ = 'events'

    id = Column(String, primary_key=True, default=str(uuid.uuid4()), index=True)
    title = Column(String, index=True)
    message = Column(String)
    bucket = Column(String, index=True)


Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class EventBase(BaseModel):
    title: str
    message: str
    bucket: str


class EventCreate(EventBase):
    pass


class EventResponse(BaseModel):
    id: str
    title: str
    message: str
    bucket: str

    class Config:
        from_attributes = True
