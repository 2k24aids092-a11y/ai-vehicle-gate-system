import logging
from typing import Optional

logger = logging.getLogger(__name__)

class CCTVCamera:
    """CCTV camera interface (for future integration)"""
    
    def __init__(self, ip: str, port: int = 8080, username: str = None, password: str = None):
        """
        Initialize CCTV camera
        
        Args:
            ip: Camera IP address
            port: Stream port
            username: Authentication username
            password: Authentication password
        """
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.stream_url = self._build_url()
        self.cap = None
        self.is_open = False
    
    def _build_url(self) -> str:
        """Build RTSP stream URL"""
        if self.username and self.password:
            return f"rtsp://{self.username}:{self.password}@{self.ip}:{self.port}/stream"
        return f"rtsp://{self.ip}:{self.port}/stream"
    
    def connect(self):
        """Connect to CCTV camera"""
        try:
            import cv2
            self.cap = cv2.VideoCapture(self.stream_url)
            
            if not self.cap.isOpened():
                raise Exception(f"Cannot connect to CCTV at {self.ip}")
            
            self.is_open = True
            logger.info(f"Connected to CCTV camera at {self.ip}")
        except Exception as e:
            logger.error(f"Failed to connect to CCTV: {str(e)}")
            self.is_open = False
    
    def get_frame(self) -> Optional[any]:
        """
        Get current frame from CCTV
        
        Returns:
            Frame or None if error
        """
        if not self.is_open or self.cap is None:
            return None
        
        try:
            ret, frame = self.cap.read()
            if not ret:
                logger.warning("Failed to read frame from CCTV")
                return None
            return frame
        except Exception as e:
            logger.error(f"Error getting frame from CCTV: {str(e)}")
            return None
    
    def release(self):
        """Release camera resources"""
        if self.cap:
            self.cap.release()
            self.is_open = False
            logger.info("CCTV camera released")
