import cv2
import numpy as np
import easyocr
import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

class PlateRecognizer:
    """License plate recognition using EasyOCR"""
    
    def __init__(self, languages=['en'], gpu=False):
        """
        Initialize plate recognizer
        
        Args:
            languages: OCR languages
            gpu: Use GPU for inference
        """
        self.reader = easyocr.Reader(languages, gpu=gpu)
        self.languages = languages
        logger.info(f"Plate recognizer initialized with languages: {languages}")
    
    def recognize_plate(self, frame):
        """
        Recognize text from license plate
        
        Args:
            frame: License plate image (numpy array)
            
        Returns:
            dict: Recognition results
        """
        try:
            # Preprocess image
            processed = self._preprocess_image(frame)
            
            # Run OCR
            results = self.reader.readtext(processed)
            
            if not results:
                return {
                    'plate_number': None,
                    'confidence': 0.0,
                    'success': False,
                    'message': 'No text detected'
                }
            
            # Extract and combine text
            texts = []
            confidences = []
            
            for (bbox, text, confidence) in results:
                texts.append(text.upper())
                confidences.append(confidence)
            
            plate_number = ''.join(texts)
            avg_confidence = np.mean(confidences) if confidences else 0.0
            
            # Validate plate format (Indian format: TN37AB1234)
            is_valid = self._validate_plate_format(plate_number)
            
            return {
                'plate_number': plate_number,
                'confidence': round(avg_confidence, 3),
                'is_valid': is_valid,
                'raw_detections': results,
                'success': True
            }
        
        except Exception as e:
            logger.error(f"Error in plate recognition: {str(e)}")
            return {
                'plate_number': None,
                'confidence': 0.0,
                'success': False,
                'error': str(e)
            }
    
    def detect_and_recognize_plate(self, frame, vehicle_bbox: Optional[Tuple] = None):
        """
        Detect license plate region and recognize text
        
        Args:
            frame: Input frame
            vehicle_bbox: Optional vehicle bounding box (x1, y1, x2, y2)
            
        Returns:
            dict: Detection and recognition results
        """
        try:
            # If vehicle bbox provided, focus on that region
            if vehicle_bbox:
                x1, y1, x2, y2 = vehicle_bbox
                roi = frame[max(0, y1):min(frame.shape[0], y2), max(0, x1):min(frame.shape[1], x2)]
            else:
                roi = frame
            
            # Detect plate region
            plate_roi = self._detect_plate_region(roi)
            
            if plate_roi is None:
                return {
                    'plate_detected': False,
                    'plate_number': None,
                    'confidence': 0.0
                }
            
            # Recognize plate text
            result = self.recognize_plate(plate_roi)
            result['plate_detected'] = True
            result['plate_image'] = plate_roi
            
            return result
        
        except Exception as e:
            logger.error(f"Error in plate detection and recognition: {str(e)}")
            return {
                'plate_detected': False,
                'plate_number': None,
                'error': str(e)
            }
    
    def _preprocess_image(self, image):
        """
        Preprocess image for better OCR results
        
        Args:
            image: Input image
            
        Returns:
            Preprocessed image
        """
        # Convert to grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Resize for better OCR (plate should be large enough)
        height = max(gray.shape[0], 100)
        scale = height / gray.shape[0] if gray.shape[0] > 0 else 1
        resized = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(resized)
        
        # Thresholding
        _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return binary
    
    def _detect_plate_region(self, frame):
        """
        Detect license plate region in vehicle image
        
        Args:
            frame: Vehicle image
            
        Returns:
            Plate region or None
        """
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if len(frame.shape) == 3 else frame
            
            # Find edges
            edges = cv2.Canny(gray, 100, 200)
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            # Find plate-like contours (rectangular)
            for contour in contours:
                area = cv2.contourArea(contour)
                if area < 500:
                    continue
                
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = float(w) / h if h > 0 else 0
                
                # License plates have aspect ratio between 2.5 and 5
                if 2.5 < aspect_ratio < 5 and area > 500:
                    # Found likely plate region
                    return frame[y:y+h, x:x+w]
            
            # If no plate detected by contours, focus on bottom-center (typical plate location)
            h, w = gray.shape
            plate_height = int(h * 0.15)
            plate_width = int(w * 0.7)
            y_start = int(h * 0.7)
            x_start = int((w - plate_width) / 2)
            
            return frame[y_start:y_start+plate_height, x_start:x_start+plate_width]
        
        except Exception as e:
            logger.error(f"Error detecting plate region: {str(e)}")
            return None
    
    def _validate_plate_format(self, plate_number: str) -> bool:
        """
        Validate Indian license plate format
        Example: TN37AB1234
        
        Args:
            plate_number: Plate text
            
        Returns:
            True if valid format
        """
        import re
        # Pattern: 2 letters, 2 digits, 2 letters, 4 digits
        pattern = r'^[A-Z]{2}\d{2}[A-Z]{2}\d{4}$'
        return bool(re.match(pattern, plate_number))
