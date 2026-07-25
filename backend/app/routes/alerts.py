from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from app.models import Alert
from app.middleware import verify_token_middleware
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/")
async def get_alerts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    severity: str = Query(None),
    resolved: bool = Query(None),
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token_middleware)
):
    """Get alerts with filtering"""
    query = db.query(Alert)
    
    if severity:
        query = query.filter(Alert.severity == severity)
    
    if resolved is not None:
        query = query.filter(Alert.is_resolved == resolved)
    
    total = query.count()
    alerts = query.order_by(Alert.created_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "alerts": alerts,
        "total": total,
        "page": skip // limit + 1,
        "limit": limit
    }

@router.get("/recent")
async def get_recent_alerts(
    hours: int = Query(24, ge=1),
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token_middleware)
):
    """Get recent alerts"""
    since = datetime.utcnow() - timedelta(hours=hours)
    alerts = db.query(Alert).filter(
        Alert.created_at >= since
    ).order_by(Alert.created_at.desc()).all()
    
    return {
        "alerts": alerts,
        "total": len(alerts)
    }

@router.post("/{alert_id}/resolve")
async def resolve_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token_middleware)
):
    """Resolve an alert"""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        return {"success": False, "message": "Alert not found"}
    
    alert.is_resolved = True
    alert.resolved_by = payload.get("user_id")
    alert.resolved_at = datetime.utcnow()
    
    db.add(alert)
    db.commit()
    db.refresh(alert)
    
    return {"success": True, "alert": alert}

@router.get("/stats")
async def get_alert_stats(
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token_middleware)
):
    """Get alert statistics"""
    total = db.query(Alert).count()
    unresolved = db.query(Alert).filter(Alert.is_resolved == False).count()
    critical = db.query(Alert).filter(Alert.severity == "critical").count()
    
    by_type = {}
    alerts = db.query(Alert).all()
    for alert in alerts:
        alert_type = alert.alert_type
        by_type[alert_type] = by_type.get(alert_type, 0) + 1
    
    return {
        "total": total,
        "unresolved": unresolved,
        "critical": critical,
        "by_type": by_type
    }
