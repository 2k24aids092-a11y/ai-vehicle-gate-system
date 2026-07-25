from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models import Vehicle
from app.schemas import VehicleCreate, VehicleUpdate
from fastapi import HTTPException, status

class VehicleService:
    """Vehicle management service"""
    
    @staticmethod
    def create_vehicle(db: Session, vehicle: VehicleCreate, user_id: int):
        """Create new vehicle"""
        # Check if plate already exists
        existing = db.query(Vehicle).filter(Vehicle.plate_number == vehicle.plate_number).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Plate number already exists"
            )
        
        db_vehicle = Vehicle(
            plate_number=vehicle.plate_number,
            owner_name=vehicle.owner_name,
            department=vehicle.department,
            phone=vehicle.phone,
            vehicle_type=vehicle.vehicle_type,
            access_level=vehicle.access_level,
            status=vehicle.status,
            notes=vehicle.notes,
            created_by=user_id
        )
        db.add(db_vehicle)
        db.commit()
        db.refresh(db_vehicle)
        return db_vehicle
    
    @staticmethod
    def get_vehicles(db: Session, skip: int = 0, limit: int = 10, search: str = None):
        """Get all vehicles with optional search"""
        query = db.query(Vehicle)
        
        if search:
            query = query.filter(
                or_(
                    Vehicle.plate_number.ilike(f"%{search}%"),
                    Vehicle.owner_name.ilike(f"%{search}%")
                )
            )
        
        total = query.count()
        vehicles = query.offset(skip).limit(limit).all()
        return vehicles, total
    
    @staticmethod
    def get_vehicle_by_id(db: Session, vehicle_id: int):
        """Get vehicle by ID"""
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not vehicle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vehicle not found"
            )
        return vehicle
    
    @staticmethod
    def get_vehicle_by_plate(db: Session, plate_number: str):
        """Get vehicle by plate number"""
        return db.query(Vehicle).filter(Vehicle.plate_number == plate_number).first()
    
    @staticmethod
    def update_vehicle(db: Session, vehicle_id: int, vehicle_data: VehicleUpdate):
        """Update vehicle information"""
        vehicle = VehicleService.get_vehicle_by_id(db, vehicle_id)
        
        update_data = vehicle_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(vehicle, field, value)
        
        db.add(vehicle)
        db.commit()
        db.refresh(vehicle)
        return vehicle
    
    @staticmethod
    def delete_vehicle(db: Session, vehicle_id: int):
        """Delete vehicle"""
        vehicle = VehicleService.get_vehicle_by_id(db, vehicle_id)
        db.delete(vehicle)
        db.commit()
        return {"message": "Vehicle deleted successfully"}
