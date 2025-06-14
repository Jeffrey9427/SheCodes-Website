from sqlalchemy import Column, Integer, String, Enum, DateTime, Text, Table, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from database import Base
from datetime import datetime

event_mentor_association = Table(
    "event_mentor_association",
    Base.metadata,
    Column("event_id", Integer, ForeignKey("events.id")),
    Column("mentor_id", Integer, ForeignKey("mentors.id"))
)

# /models/event.py

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    event_type = Column(Enum("Workshop", "Seminar", "Webinar", "Mentorship", name="event_type_enum"), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    # --- Updated Fields ---
    status = Column(Enum("upcoming", "past", "ongoing", name="event_status_enum"), nullable=False, default="upcoming")
    image_src = Column(String, nullable=True) # Renamed from imageSrc
    image_alt = Column(String, nullable=True)
    tags = Column(JSONB, nullable=True)
    long_description = Column(Text, nullable=True) # Renamed from longDescription
    register_link = Column(String, nullable=True) # Renamed from registerLink
    tools = Column(JSONB, nullable=True)
    key_points = Column(JSONB, nullable=True)
    group_link = Column(String, nullable=True) # Renamed from groupLink
    
    # Relationships (no changes here)
    mentors = relationship("Mentor", secondary=event_mentor_association, back_populates="events")
    skills = relationship("Skill", cascade="all, delete-orphan", backref="event")
    benefits = relationship("Benefit", cascade="all, delete-orphan", backref="event")
    sessions = relationship("Session", cascade="all, delete-orphan", backref="event")
    participants = relationship("Participant", back_populates="event")

class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)

class Benefit(Base):
    __tablename__ = "benefits"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)

class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)