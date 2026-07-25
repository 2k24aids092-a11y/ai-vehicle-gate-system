import logging
from typing import Optional, Tuple
import numpy as np
from sqlalchemy.orm import Session
from app.models import Vehicle, UnauthorizedAttempt, Alert
from config import YOLO_CONFIDENCE_THRESHOLD, OCR_CONFIDENCE_THRESHOLD

logger = logging.getLogger(__name__)

class AIService:
    """AI service for vehicle detection and plate recognition"""
    
    def __init__(self):
        """Initialize AI models"""
        try:
            from ai.models.vehicle_detector import VehicleDetector
            from ai.models.plate_recognizer import PlateRecognizer
            
            self.vehicle_detector = VehicleDetector(
                model_path='ai/models/yolov8s.pt',
                confidence_threshold=YOLO_CONFIDENCE_THRESHOLD
            )
            self.plate_recognizer = PlateRecognizer(languages=['en'])
            logger.info("AI models loaded successfully")
        except Exception as e:
            logger.error(f"Error loading AI models: {str(e)}")
            self.vehicle_detector = None
            self.plate_recognizer = None
    
    def detect_vehicle(self, frame):
        """
        Detect vehicles in frame
        
        Args:
            frame: Input frame (numpy array)
            
        Returns:
            Detection results
        """
        if not self.vehicle_detector:
            return {
                'success': False,
                'message': 'Vehicle detector not initialized'
            }
        
        try:
            result = self.vehicle_detector.detect(frame)
            return result
        except Exception as e:
            logger.error(f"Error detecting vehicle: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def recognize_plate(self, frame):
        """
        Recognize license plate in frame
        
        Args:
            frame: Input frame (numpy array)
            
        Returns:
            Recognition results
        """
        if not self.plate_recognizer:
            return {
                'success': False,
                'message': 'Plate recognizer not initialized'
            }
        
        try:
            result = self.plate_recognizer.recognize_plate(frame)
            return result
        except Exception as e:
            logger.error(f"Error recognizing plate: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def verify_vehicle_access(self, db: Session, plate_number: str) -> dict:
        """
        Verify vehicle access permission
        
        Args:
            db: Database session
            plate_number: License plate number
            
        Returns:
            Access verification result
        """
        try:
            vehicle = db.query(Vehicle).filter(
                Vehicle.plate_number == plate_number
            ).first()
            
            if not vehicle:
                return {
                    'access': False,
                    'status': 'not_found',
                    'message': 'Vehicle not found in database'
                }
            
            if vehicle.status == 'blacklisted':
                return {
                    'access': False,
                    'status': 'blacklisted',
                    'message': 'Vehicle is blacklisted',
                    'vehicle': vehicle
                }
            
            if vehicle.status == 'inactive':
                return {
                    'access': False,
                    'status': 'inactive',
                    'message': 'Vehicle is inactive',
                    'vehicle': vehicle
                }
            
            if vehicle.access_level == 'none':
                return {
                    'access': False,
                    'status': 'no_access',
                    'message': 'Vehicle has no access permission',
                    'vehicle': vehicle
                }
            
            return {
                'access': True,
                'status': 'granted',
                'message': 'Access granted',
                'vehicle': vehicle
            }
        
        except Exception as e:
            logger.error(f"Error verifying vehicle access: {str(e)}")
            return {
                'access': False,
                'status': 'error',
                'message': str(e)
            }
    
    def log_unauthorized_attempt(self, db: Session, plate_number: str, 
                                vehicle_type: str, confidence: float) -> dict:
        """
        Log unauthorized vehicle attempt
        
        Args:
            db: Database session
            plate_number: License plate
            vehicle_type: Detected vehicle type
            confidence: Detection confidence
            
        Returns:
            Log result
        """
        try:
            attempt = UnauthorizedAttempt(
                plate_number=plate_number,
                vehicle_type=vehicle_type,
                detection_confidence=confidence,
                status='open'
            )
            db.add(attempt)
            db.commit()
            db.refresh(attempt)
            
            # Create alert
            alert = Alert(
                alert_type='unauthorized_vehicle',
                severity='high',
                title='Unauthorized Vehicle Attempted Entry',
                message=f'Vehicle {plate_number} attempted entry',
                related_attempt_id=attempt.id
            )
            db.add(alert)
            db.commit()
            
            logger.warning(f"Unauthorized attempt logged: {plate_number}")
            return {
                'success': True,
                'attempt_id': attempt.id
            }
        except Exception as e:
            logger.error(f"Error logging unauthorized attempt: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
