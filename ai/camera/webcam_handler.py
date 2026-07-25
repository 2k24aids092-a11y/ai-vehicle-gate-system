import cv2
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class WebcamHandler:
    """Webcam camera interface"""
    
    def __init__(self, camera_id=0, width=1280, height=720, fps=30):
        """
        Initialize webcam
        
        Args:
            camera_id: Camera device ID
            width: Frame width
            height: Frame height
            fps: Frames per second
        """
        self.camera_id = camera_id
        self.width = width
        self.height = height
        self.fps = fps
        self.cap = None
        self.is_open = False
        self.connect()
    
    def connect(self):
        """Connect to webcam"""
        try:
            self.cap = cv2.VideoCapture(self.camera_id)
            
            if not self.cap.isOpened():
                raise Exception("Cannot open webcam")
            
            # Set camera properties
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            self.cap.set(cv2.CAP_PROP_FPS, self.fps)
            
            self.is_open = True
            logger.info(f"Webcam {self.camera_id} connected successfully")
        except Exception as e:
            logger.error(f"Failed to connect to webcam: {str(e)}")
            self.is_open = False
    
    def get_frame(self) -> Optional[any]:
        """
        Get current frame from webcam
        
        Returns:
            Frame or None if error
        """
        if not self.is_open or self.cap is None:
            return None
        
        try:
            ret, frame = self.cap.read()
            if not ret:
                logger.warning("Failed to read frame from webcam")
                return None
            return frame
        except Exception as e:
            logger.error(f"Error getting frame: {str(e)}")
            return None
    
    def release(self):
        """Release camera resources"""
        if self.cap:
            self.cap.release()
            self.is_open = False
            logger.info("Webcam released")
    
    def __del__(self):
        """Cleanup"""
        self.release()
