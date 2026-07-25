from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from app.models import EntryLog, Vehicle, Visitor, UnauthorizedAttempt
from app.middleware import verify_token_middleware
from datetime import datetime, timedelta
import json

router = APIRouter()

@router.get("/daily")
async def get_daily_report(
    date: str = Query(None),
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token_middleware)
):
    """Get daily report"""
    if not date:
        report_date = datetime.utcnow().date()
    else:
        report_date = datetime.strptime(date, "%Y-%m-%d").date()
    
    # Calculate statistics
    entries = db.query(func.count(EntryLog.id)).filter(
        func.date(EntryLog.entry_time) == report_date,
        EntryLog.access_status == "granted"
    ).scalar() or 0
    
    exits = db.query(func.count(EntryLog.id)).filter(
        func.date(EntryLog.exit_time) == report_date
    ).scalar() or 0
    
    unauthorized = db.query(func.count(UnauthorizedAttempt.id)).filter(
        func.date(UnauthorizedAttempt.attempt_time) == report_date
    ).scalar() or 0
    
    inside = db.query(func.count(EntryLog.id)).filter(
        func.date(EntryLog.entry_time) == report_date,
        EntryLog.exit_time.is_(None),
        EntryLog.access_status == "granted"
    ).scalar() or 0
    
    return {
        "report_type": "daily",
        "date": str(report_date),
        "total_entries": entries,
        "total_exits": exits,
        "vehicles_inside": inside,
        "unauthorized_attempts": unauthorized
    }

@router.get("/monthly")
async def get_monthly_report(
    month: str = Query(None),
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token_middleware)
):
    """Get monthly report"""
    if not month:
        now = datetime.utcnow()
        start_date = datetime(now.year, now.month, 1).date()
        end_date = (datetime(now.year, now.month + 1, 1) if now.month < 12 
                   else datetime(now.year + 1, 1, 1)).date() - timedelta(days=1)
    else:
        start_date = datetime.strptime(month, "%Y-%m").date()
        end_date = (datetime(start_date.year, start_date.month + 1, 1) if start_date.month < 12
                   else datetime(start_date.year + 1, 1, 1)).date() - timedelta(days=1)
    
    entries = db.query(func.count(EntryLog.id)).filter(
        func.date(EntryLog.entry_time).between(start_date, end_date),
        EntryLog.access_status == "granted"
    ).scalar() or 0
    
    exits = db.query(func.count(EntryLog.id)).filter(
        func.date(EntryLog.exit_time).between(start_date, end_date)
    ).scalar() or 0
    
    unauthorized = db.query(func.count(UnauthorizedAttempt.id)).filter(
        func.date(UnauthorizedAttempt.attempt_time).between(start_date, end_date)
    ).scalar() or 0
    
    avg_duration = db.query(func.avg(EntryLog.duration_minutes)).filter(
        func.date(EntryLog.entry_time).between(start_date, end_date),
        EntryLog.duration_minutes.isnot(None)
    ).scalar() or 0
    
    return {
        "report_type": "monthly",
        "period": f"{start_date.year}-{start_date.month:02d}",
        "total_entries": entries,
        "total_exits": exits,
        "unauthorized_attempts": unauthorized,
        "avg_duration_minutes": round(avg_duration, 2)
    }

@router.get("/vehicle/{vehicle_id}")
async def get_vehicle_report(
    vehicle_id: int,
    days: int = Query(30, ge=1),
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token_middleware)
):
    """Get vehicle activity report"""
    since = datetime.utcnow() - timedelta(days=days)
    
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        return {"error": "Vehicle not found"}
    
    logs = db.query(EntryLog).filter(
        EntryLog.vehicle_id == vehicle_id,
        EntryLog.entry_time >= since
    ).order_by(EntryLog.entry_time.desc()).all()
    
    total_entries = len(logs)
    total_duration = sum([log.duration_minutes or 0 for log in logs if log.duration_minutes])
    
    return {
        "vehicle_id": vehicle_id,
        "plate_number": vehicle.plate_number,
        "owner_name": vehicle.owner_name,
        "period_days": days,
        "total_entries": total_entries,
        "total_duration_minutes": total_duration,
        "logs": logs
    }

@router.get("/summary")
async def get_summary_report(
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token_middleware)
):
    """Get system summary report"""
    today = datetime.utcnow().date()
    
    today_entries = db.query(func.count(EntryLog.id)).filter(
        func.date(EntryLog.entry_time) == today,
        EntryLog.access_status == "granted"
    ).scalar() or 0
    
    today_exits = db.query(func.count(EntryLog.id)).filter(
        func.date(EntryLog.exit_time) == today
    ).scalar() or 0
    
    total_vehicles = db.query(func.count(Vehicle.id)).scalar() or 0
    active_vehicles = db.query(func.count(Vehicle.id)).filter(
        Vehicle.status == "active"
    ).scalar() or 0
    
    blacklisted = db.query(func.count(Vehicle.id)).filter(
        Vehicle.status == "blacklisted"
    ).scalar() or 0
    
    unauthorized_today = db.query(func.count(UnauthorizedAttempt.id)).filter(
        func.date(UnauthorizedAttempt.attempt_time) == today
    ).scalar() or 0
    
    pending_visitors = db.query(func.count(Visitor.id)).filter(
        Visitor.approval_status == "pending"
    ).scalar() or 0
    
    return {
        "today_entries": today_entries,
        "today_exits": today_exits,
        "total_vehicles": total_vehicles,
        "active_vehicles": active_vehicles,
        "blacklisted_vehicles": blacklisted,
        "unauthorized_attempts_today": unauthorized_today,
        "pending_visitors": pending_visitors
    }
