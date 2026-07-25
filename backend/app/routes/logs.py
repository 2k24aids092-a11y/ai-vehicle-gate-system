from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from app.schemas import EntryLogCreate, EntryLogResponse
from app.services import EntryLogService
from app.middleware import verify_token_middleware

router = APIRouter()

@router.get("/", response_model=list[EntryLogResponse])
async def get_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    days: int = Query(7, ge=1),
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token_middleware)
):
    """Get entry/exit logs"""
    logs, total = EntryLogService.get_logs(db, skip, limit, days)
    return logs

@router.post("/", response_model=EntryLogResponse)
async def create_log(
    log_data: EntryLogCreate,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token_middleware)
):
    """Create entry log"""
    return EntryLogService.create_log(db, log_data)

@router.post("/{log_id}/exit", response_model=EntryLogResponse)
async def mark_exit(
    log_id: int,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token_middleware)
):
    """Mark vehicle exit"""
    return EntryLogService.mark_exit(db, log_id)

@router.get("/stats/today")
async def get_today_stats(
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token_middleware)
):
    """Get today's entry/exit statistics"""
    return EntryLogService.get_today_stats(db)
