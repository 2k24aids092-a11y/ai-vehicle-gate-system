from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from database import Base

class UnauthorizedAttempt(Base):
    __tablename__ = "unauthorized_attempts"

    id = Column(Integer, primary_key=True, index=True)
    plate_number = Column(String(50), index=True)
    vehicle_type = Column(String(50))
    detection_confidence = Column(Float)
    gate_number = Column(Integer, default=1)
    attempt_time = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    image_url = Column(String(500))
    status = Column(String(50), index=True)
    resolved_by = Column(Integer, ForeignKey("users.id"))
    resolved_at = Column(DateTime(timezone=True))
    notes = Column(String(1000))
