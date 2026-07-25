import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class CameraInterface(ABC):
    """Abstract camera interface for hardware abstraction"""
    
    @abstractmethod
    def connect(self):
        """Connect to camera"""
        pass
    
    @abstractmethod
    def get_frame(self):
        """Get frame from camera"""
        pass
    
    @abstractmethod
    def release(self):
        """Release camera resources"""
        pass
    
    @abstractmethod
    def is_connected(self):
        """Check if camera is connected"""
        pass
