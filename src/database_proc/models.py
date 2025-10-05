# models.py
from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    trust_level = Column(Integer, default=0)
    points = Column(Integer, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

class Hazard(Base):
    __tablename__ = "hazards"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    problem = Column(String, nullable=False)  # 👈 замість title
    description = Column(String, nullable=True)
    delay_sec = Column(Integer, nullable=True)
    vehicle_id = Column(String, nullable=True)
    trip_id = Column(String, nullable=True)
    route_id = Column(String, nullable=True)
    source = Column(String, default="user")
    reporter_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    status = Column(String, default="new")
    severity_num = Column(Integer, default=0)
    confidence = Column(Float, default=0.5)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    valid_until = Column(DateTime, nullable=True)

