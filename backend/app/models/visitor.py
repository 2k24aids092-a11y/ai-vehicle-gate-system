from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from database import Base
import enum

class ApprovalStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"

class VehicleType(str, enum.Enum):
    CAR = "Car"
    BIKE = "Bike"
    BUS = "Bus"
    TRUCK = "Truck"
    VAN = "Van"

class Visitor(Base):
    __tablename__ = "visitors"

    id = Column(Integer, primary_key=True, index=True)
    visitor_name = Column(String(255))
    visitor_phone = Column(String(20))
    vehicle_number = Column(String(50), index=True)
    vehicle_type = Column(Enum(VehicleType))
    purpose = Column(String(500))
    approval_status = Column(Enum(ApprovalStatus), default=ApprovalStatus.PENDING, index=True)
    approved_by = Column(Integer, ForeignKey("users.id"))
    approved_at = Column(DateTime(timezone=True))
    valid_from = Column(DateTime(timezone=True))
    valid_until = Column(DateTime(timezone=True))
    photo_url = Column(String(500))
    notes = Column(String(1000))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
