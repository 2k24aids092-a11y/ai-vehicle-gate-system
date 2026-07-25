from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class VehicleCreate(BaseModel):
    plate_number: str
    owner_name: str
    department: Optional[str] = None
    phone: Optional[str] = None
    vehicle_type: str
    access_level: str = "full"
    status: str = "active"
    notes: Optional[str] = None

class VehicleUpdate(BaseModel):
    owner_name: Optional[str] = None
    department: Optional[str] = None
    phone: Optional[str] = None
    vehicle_type: Optional[str] = None
    access_level: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class VehicleResponse(BaseModel):
    id: int
    plate_number: str
    owner_name: str
    department: Optional[str]
    phone: Optional[str]
    vehicle_type: str
    access_level: str
    status: str
    photo_url: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
