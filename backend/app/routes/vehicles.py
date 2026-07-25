from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database import get_db
from app.schemas import VehicleCreate, VehicleUpdate, VehicleResponse
from app.services import VehicleService
from app.middleware import verify_token_middleware

router = APIRouter()

@router.get("/", response_model=list[VehicleResponse])
async def get_vehicles(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: str = Query(None),
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token_middleware)
):
    """Get all vehicles"""
    vehicles, total = VehicleService.get_vehicles(db, skip, limit, search)
    return vehicles

@router.get("/{vehicle_id}", response_model=VehicleResponse)
async def get_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token_middleware)
):
    """Get vehicle by ID"""
    return VehicleService.get_vehicle_by_id(db, vehicle_id)

@router.post("/", response_model=VehicleResponse)
async def create_vehicle(
    vehicle: VehicleCreate,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token_middleware)
):
    """Create new vehicle (Admin only)"""
    if payload.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create vehicles"
        )
    return VehicleService.create_vehicle(db, vehicle, payload.get("user_id"))

@router.put("/{vehicle_id}", response_model=VehicleResponse)
async def update_vehicle(
    vehicle_id: int,
    vehicle_data: VehicleUpdate,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token_middleware)
):
    """Update vehicle information (Admin only)"""
    if payload.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can update vehicles"
        )
    return VehicleService.update_vehicle(db, vehicle_id, vehicle_data)

@router.delete("/{vehicle_id}")
async def delete_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token_middleware)
):
    """Delete vehicle (Admin only)"""
    if payload.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete vehicles"
        )
    return VehicleService.delete_vehicle(db, vehicle_id)
