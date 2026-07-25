from sqlalchemy import Column, Integer, String, DateTime, Float, Enum, ForeignKey
from sqlalchemy.sql import func
from database import Base
import enum

class AccessStatus(str, enum.Enum):
    GRANTED = "granted"
    DENIED = "denied"
    PENDING = "pending"

class EntryLog(Base):
    __tablename__ = "entry_logs"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), index=True)
    plate_number = Column(String(50), index=True)
    entry_time = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    exit_time = Column(DateTime(timezone=True))
    duration_minutes = Column(Integer)
    parking_slot = Column(String(10))
    gate_number = Column(Integer, default=1)
    detection_confidence = Column(Float)
    access_status = Column(Enum(AccessStatus), default=AccessStatus.GRANTED, index=True)
    notes = Column(String(1000))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
