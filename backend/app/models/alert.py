from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean, ForeignKey
from sqlalchemy.sql import func
from database import Base
import enum

class AlertType(str, enum.Enum):
    UNAUTHORIZED_VEHICLE = "unauthorized_vehicle"
    BLACKLISTED_VEHICLE = "blacklisted_vehicle"
    CAMERA_OFFLINE = "camera_offline"
    PARKING_FULL = "parking_full"
    GATE_ERROR = "gate_error"
    CUSTOM = "custom"

class AlertSeverity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    alert_type = Column(Enum(AlertType), default=AlertType.CUSTOM)
    severity = Column(Enum(AlertSeverity), default=AlertSeverity.MEDIUM)
    title = Column(String(255))
    message = Column(String(1000))
    related_vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    related_attempt_id = Column(Integer, ForeignKey("unauthorized_attempts.id"))
    is_resolved = Column(Boolean, default=False, index=True)
    resolved_by = Column(Integer, ForeignKey("users.id"))
    resolved_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
