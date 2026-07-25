from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from database import Base
import enum

class VehicleType(str, enum.Enum):
    CAR = "Car"
    BIKE = "Bike"
    BUS = "Bus"
    TRUCK = "Truck"
    VAN = "Van"

class AccessLevel(str, enum.Enum):
    FULL = "full"
    RESTRICTED = "restricted"
    TEMPORARY = "temporary"
    NONE = "none"

class VehicleStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLACKLISTED = "blacklisted"
    PENDING = "pending"

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    plate_number = Column(String(50), unique=True, index=True)
    owner_name = Column(String(255))
    department = Column(String(255))
    phone = Column(String(20))
    vehicle_type = Column(Enum(VehicleType))
    access_level = Column(Enum(AccessLevel), default=AccessLevel.FULL)
    status = Column(Enum(VehicleStatus), default=VehicleStatus.ACTIVE, index=True)
    photo_url = Column(String(500))
    notes = Column(String(1000))
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
