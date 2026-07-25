from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ParkingResponse(BaseModel):
    id: int
    slot_number: str
    floor: int
    section: str
    status: str
    vehicle_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ParkingAssignRequest(BaseModel):
    vehicle_id: int
    slot_number: str

class ParkingSummary(BaseModel):
    total_slots: int
    occupied_slots: int
    available_slots: int
    reserved_slots: int
    occupancy_percentage: float
