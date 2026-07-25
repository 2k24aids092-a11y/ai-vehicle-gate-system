from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from app.services import EntryLogService, ParkingService
from app.middleware import verify_token_middleware

router = APIRouter()

@router.get("/overview")
async def get_dashboard_overview(
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token_middleware)
):
    """Get dashboard overview data"""
    stats = EntryLogService.get_today_stats(db)
    parking = ParkingService.get_parking_status(db)
    
    return {
        "today_entries": stats["entries"],
        "today_exits": stats["exits"],
        "vehicles_inside": stats["inside"],
        "parking_total": parking["total_slots"],
        "parking_occupied": parking["occupied_slots"],
        "parking_available": parking["available_slots"],
        "parking_occupancy_percentage": parking["occupancy_percentage"]
    }
