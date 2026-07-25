from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import ParkingSlot, Vehicle
from fastapi import HTTPException, status

class ParkingService:
    """Parking management service"""
    
    @staticmethod
    def get_parking_status(db: Session):
        """Get overall parking status"""
        total_slots = db.query(func.count(ParkingSlot.id)).scalar()
        occupied = db.query(func.count(ParkingSlot.id)).filter(
            ParkingSlot.status == "occupied"
        ).scalar()
        available = db.query(func.count(ParkingSlot.id)).filter(
            ParkingSlot.status == "available"
        ).scalar()
        reserved = db.query(func.count(ParkingSlot.id)).filter(
            ParkingSlot.status == "reserved"
        ).scalar()
        
        occupancy_percentage = (occupied / total_slots * 100) if total_slots > 0 else 0
        
        return {
            "total_slots": total_slots,
            "occupied_slots": occupied,
            "available_slots": available,
            "reserved_slots": reserved,
            "occupancy_percentage": round(occupancy_percentage, 2)
        }
    
    @staticmethod
    def get_all_slots(db: Session):
        """Get all parking slots with details"""
        slots = db.query(ParkingSlot).all()
        result = []
        
        for slot in slots:
            slot_data = {
                "id": slot.id,
                "slot_number": slot.slot_number,
                "floor": slot.floor,
                "section": slot.section,
                "status": slot.status,
                "vehicle_id": slot.vehicle_id
            }
            
            if slot.vehicle_id:
                vehicle = db.query(Vehicle).filter(Vehicle.id == slot.vehicle_id).first()
                if vehicle:
                    slot_data["plate_number"] = vehicle.plate_number
                    slot_data["owner_name"] = vehicle.owner_name
            
            result.append(slot_data)
        
        return result
    
    @staticmethod
    def assign_parking(db: Session, vehicle_id: int, slot_number: str):
        """Assign parking slot to vehicle"""
        # Get slot
        slot = db.query(ParkingSlot).filter(ParkingSlot.slot_number == slot_number).first()
        if not slot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parking slot not found"
            )
        
        if slot.status == "occupied":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Parking slot already occupied"
            )
        
        # Update slot
        slot.vehicle_id = vehicle_id
        slot.status = "occupied"
        
        db.add(slot)
        db.commit()
        db.refresh(slot)
        return slot
    
    @staticmethod
    def release_parking(db: Session, slot_id: int):
        """Release parking slot"""
        slot = db.query(ParkingSlot).filter(ParkingSlot.id == slot_id).first()
        if not slot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parking slot not found"
            )
        
        slot.vehicle_id = None
        slot.status = "available"
        
        db.add(slot)
        db.commit()
        db.refresh(slot)
        return slot
