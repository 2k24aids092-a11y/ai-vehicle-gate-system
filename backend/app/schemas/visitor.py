from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class VisitorCreate(BaseModel):
    visitor_name: str
    visitor_phone: Optional[str] = None
    vehicle_number: str
    vehicle_type: str
    purpose: str
    valid_from: datetime
    valid_until: datetime

class VisitorUpdate(BaseModel):
    approval_status: Optional[str] = None
    notes: Optional[str] = None

class VisitorResponse(BaseModel):
    id: int
    visitor_name: str
    visitor_phone: Optional[str]
    vehicle_number: str
    vehicle_type: str
    purpose: str
    approval_status: str
    valid_from: datetime
    valid_until: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
