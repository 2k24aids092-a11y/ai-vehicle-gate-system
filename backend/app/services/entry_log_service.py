from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.models import EntryLog
from app.schemas import EntryLogCreate

class EntryLogService:
    """Entry/Exit log service"""
    
    @staticmethod
    def create_log(db: Session, log_data: EntryLogCreate):
        """Create entry log"""
        db_log = EntryLog(
            vehicle_id=log_data.vehicle_id,
            plate_number=log_data.plate_number,
            parking_slot=log_data.parking_slot,
            gate_number=log_data.gate_number,
            detection_confidence=log_data.detection_confidence,
            access_status=log_data.access_status
        )
        db.add(db_log)
        db.commit()
        db.refresh(db_log)
        return db_log
    
    @staticmethod
    def get_logs(db: Session, skip: int = 0, limit: int = 10, days: int = 7):
        """Get entry logs with pagination"""
        date_from = datetime.utcnow() - timedelta(days=days)
        
        query = db.query(EntryLog).filter(EntryLog.entry_time >= date_from)
        total = query.count()
        logs = query.offset(skip).limit(limit).order_by(EntryLog.entry_time.desc()).all()
        
        return logs, total
    
    @staticmethod
    def mark_exit(db: Session, log_id: int):
        """Mark vehicle exit"""
        log = db.query(EntryLog).filter(EntryLog.id == log_id).first()
        if not log:
            return None
        
        log.exit_time = datetime.utcnow()
        if log.entry_time:
            duration = log.exit_time - log.entry_time
            log.duration_minutes = int(duration.total_seconds() / 60)
        
        db.add(log)
        db.commit()
        db.refresh(log)
        return log
    
    @staticmethod
    def get_today_stats(db: Session):
        """Get today's statistics"""
        today = datetime.utcnow().date()
        
        entries = db.query(func.count(EntryLog.id)).filter(
            func.date(EntryLog.entry_time) == today,
            EntryLog.access_status == "granted"
        ).scalar()
        
        exits = db.query(func.count(EntryLog.id)).filter(
            func.date(EntryLog.exit_time) == today
        ).scalar()
        
        inside = db.query(func.count(EntryLog.id)).filter(
            func.date(EntryLog.entry_time) == today,
            EntryLog.exit_time.is_(None),
            EntryLog.access_status == "granted"
        ).scalar()
        
        return {
            "entries": entries,
            "exits": exits,
            "inside": inside
        }
