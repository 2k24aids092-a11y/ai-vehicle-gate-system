from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database import get_db
from app.schemas import VisitorCreate, VisitorUpdate, VisitorResponse
from app.models import Visitor
from app.middleware import verify_token_middleware
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=list[VisitorResponse])
async def get_visitors(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token_middleware)
):
    """Get all visitor requests"""
    visitors = db.query(Visitor).offset(skip).limit(limit).all()
    return visitors

@router.post("/", response_model=VisitorResponse)
async def create_visitor(
    visitor: VisitorCreate,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token_middleware)
):
    """Create visitor request"""
    db_visitor = Visitor(
        visitor_name=visitor.visitor_name,
        visitor_phone=visitor.visitor_phone,
        vehicle_number=visitor.vehicle_number,
        vehicle_type=visitor.vehicle_type,
        purpose=visitor.purpose,
        valid_from=visitor.valid_from,
        valid_until=visitor.valid_until,
        approval_status="pending"
    )
    db.add(db_visitor)
    db.commit()
    db.refresh(db_visitor)
    return db_visitor

@router.put("/{visitor_id}", response_model=VisitorResponse)
async def update_visitor(
    visitor_id: int,
    visitor_data: VisitorUpdate,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token_middleware)
):
    """Update visitor request (approve/reject)"""
    if payload.get("role") not in ["admin", "security"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins and security can approve visitors"
        )
    
    visitor = db.query(Visitor).filter(Visitor.id == visitor_id).first()
    if not visitor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Visitor not found"
        )
    
    if visitor_data.approval_status:
        visitor.approval_status = visitor_data.approval_status
        if visitor_data.approval_status == "approved":
            visitor.approved_by = payload.get("user_id")
            visitor.approved_at = datetime.utcnow()
    
    if visitor_data.notes:
        visitor.notes = visitor_data.notes
    
    db.add(visitor)
    db.commit()
    db.refresh(visitor)
    return visitor

@router.get("/active")
async def get_active_visitors(
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token_middleware)
):
    """Get currently active visitors"""
    now = datetime.utcnow()
    active = db.query(Visitor).filter(
        Visitor.approval_status == "approved",
        Visitor.valid_from <= now,
        Visitor.valid_until >= now
    ).all()
    return active
