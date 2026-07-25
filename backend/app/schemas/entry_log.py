from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EntryLogCreate(BaseModel):
    vehicle_id: int
    plate_number: str
    parking_slot: Optional[str] = None
    gate_number: int = 1
    detection_confidence: Optional[float] = None
    access_status: str = "granted"

class EntryLogResponse(BaseModel):
    id: int
    vehicle_id: int
    plate_number: str
    entry_time: datetime
    exit_time: Optional[datetime]
    duration_minutes: Optional[int]
    parking_slot: Optional[str]
    gate_number: int
    detection_confidence: Optional[float]
    access_status: str
    created_at: datetime

    class Config:
        from_attributes = True
