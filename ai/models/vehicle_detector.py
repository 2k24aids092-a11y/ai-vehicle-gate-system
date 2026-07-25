import cv2
import numpy as np
from ultralytics import YOLO
import logging

logger = logging.getLogger(__name__)

class VehicleDetector:
    """YOLOv8 based vehicle detection"""
    
    def __init__(self, model_path='models/yolov8s.pt', confidence_threshold=0.5):
        """
        Initialize vehicle detector
        
        Args:
            model_path: Path to YOLOv8 model
            confidence_threshold: Detection confidence threshold
        """
        self.model = YOLO(model_path)
        self.confidence_threshold = confidence_threshold
        self.vehicle_classes = ['car', 'motorcycle', 'truck', 'bus', 'bicycle', 'van']
        logger.info(f"Vehicle detector initialized with model: {model_path}")
    
    def detect(self, frame):
        """
        Detect vehicles in frame
        
        Args:
            frame: Input frame (numpy array)
            
        Returns:
            dict: Detection results with vehicles and annotated frame
        """
        try:
            # Run detection
            results = self.model(frame, verbose=False, conf=self.confidence_threshold)
            
            detections = []
            annotated_frame = frame.copy()
            
            # Process results
            for result in results:
                for box in result.boxes:
                    class_id = int(box.cls[0])
                    class_name = self.model.names[class_id]
                    confidence = float(box.conf[0])
                    
                    # Check if detected object is a vehicle
                    if class_name.lower() in self.vehicle_classes and confidence >= self.confidence_threshold:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        
                        detection = {
                            'class': class_name,
                            'confidence': round(confidence, 3),
                            'bbox': {
                                'x1': x1,
                                'y1': y1,
                                'x2': x2,
                                'y2': y2,
                                'width': x2 - x1,
                                'height': y2 - y1
                            }
                        }
                        detections.append(detection)
                        
                        # Draw bounding box
                        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
                        cv2.putText(
                            annotated_frame,
                            f"{class_name} {confidence:.2f}",
                            (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (0, 255, 255),
                            2
                        )
            
            return {
                'detections': detections,
                'total_vehicles': len(detections),
                'annotated_frame': annotated_frame,
                'success': True
            }
        
        except Exception as e:
            logger.error(f"Error in vehicle detection: {str(e)}")
            return {
                'detections': [],
                'total_vehicles': 0,
                'annotated_frame': frame,
                'success': False,
                'error': str(e)
            }
    
    def get_vehicle_type(self, class_name):
        """
        Map YOLO class to vehicle type
        """
        class_mapping = {
            'car': 'Car',
            'motorcycle': 'Bike',
            'truck': 'Truck',
            'bus': 'Bus',
            'bicycle': 'Bike',
            'van': 'Van'
        }
        return class_mapping.get(class_name.lower(), 'Unknown')
    
    def update_confidence_threshold(self, threshold):
        """Update confidence threshold"""
        self.confidence_threshold = threshold
        logger.info(f"Confidence threshold updated to {threshold}")
