from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from app.schemas import ParkingResponse, ParkingAssignRequest, ParkingSummary
from app.services import ParkingService
from app.middleware import verify_token_middleware

router = APIRouter()

@router.get("/status", response_model=ParkingSummary)
async def get_parking_status(
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token_middleware)
):
    """Get parking occupancy status"""
    return ParkingService.get_parking_status(db)

@router.get("/slots", response_model=list[dict])
async def get_parking_slots(
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token_middleware)
):
    """Get all parking slots"""
    return ParkingService.get_all_slots(db)

@router.post("/assign")
async def assign_parking(
    request: ParkingAssignRequest,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token_middleware)
):
    """Assign parking slot to vehicle"""
    return ParkingService.assign_parking(db, request.vehicle_id, request.slot_number)

@router.post("/release/{slot_id}")
async def release_parking(
    slot_id: int,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token_middleware)
):
    """Release parking slot"""
    return ParkingService.release_parking(db, slot_id)
