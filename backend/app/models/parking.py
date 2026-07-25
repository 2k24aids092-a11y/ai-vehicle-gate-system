from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from database import Base
import enum

class ParkingStatus(str, enum.Enum):
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    RESERVED = "reserved"
    MAINTENANCE = "maintenance"

class ParkingSlot(Base):
    __tablename__ = "parking_slots"

    id = Column(Integer, primary_key=True, index=True)
    slot_number = Column(String(10), unique=True, index=True)
    floor = Column(Integer, default=1)
    section = Column(String(5))
    status = Column(Enum(ParkingStatus), default=ParkingStatus.AVAILABLE, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    reserved_until = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
