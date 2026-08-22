import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, String, Uuid
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)


class Emotion(Base):
    __tablename__ = "emotions"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id"))
    emotion = Column(String, index=True)
    emotion_score = Column(Float)
    emotion_keywords = Column(String)
    created_at = Column(DateTime, default=datetime.now)


class ActivityType(Base):
    __tablename__ = "activity_types"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True)


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id"))
    activity_type_id = Column(Uuid(as_uuid=True), ForeignKey("activity_types.id"))
    description = Column(String)
    created_at = Column(DateTime, default=datetime.now)


class FlowCurve(Base):
    __tablename__ = "flow_curve"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id"))
    time_spent = Column(Float)
    satisfaction = Column(Float)
    created_at = Column(DateTime, default=datetime.now)
