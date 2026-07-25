import logging
import time
from typing import Optional
import json

logger = logging.getLogger(__name__)

class GateSimulator:
    """Gate simulator for development and testing"""
    
    def __init__(self, opening_delay=2, closing_delay=5):
        """
        Initialize gate simulator
        
        Args:
            opening_delay: Delay for gate opening animation
            closing_delay: Delay for gate closing
        """
        self.opening_delay = opening_delay
        self.closing_delay = closing_delay
        self.is_open = False
        self.state = 'closed'  # closed, opening, open, closing
        logger.info("Gate simulator initialized")
    
    def open(self) -> dict:
        """
        Open gate (simulated)
        
        Returns:
            dict: Operation result
        """
        try:
            self.state = 'opening'
            logger.info("Gate opening...")
            
            # Simulate opening delay
            time.sleep(self.opening_delay)
            
            self.state = 'open'
            self.is_open = True
            logger.info("Gate opened successfully")
            
            return {
                'success': True,
                'status': 'open',
                'message': 'Gate opened successfully',
                'timestamp': time.time()
            }
        except Exception as e:
            logger.error(f"Error opening gate: {str(e)}")
            return {
                'success': False,
                'status': 'error',
                'message': str(e)
            }
    
    def close(self) -> dict:
        """
        Close gate (simulated)
        
        Returns:
            dict: Operation result
        """
        try:
            self.state = 'closing'
            logger.info("Gate closing...")
            
            # Simulate closing delay
            time.sleep(self.closing_delay)
            
            self.state = 'closed'
            self.is_open = False
            logger.info("Gate closed successfully")
            
            return {
                'success': True,
                'status': 'closed',
                'message': 'Gate closed successfully',
                'timestamp': time.time()
            }
        except Exception as e:
            logger.error(f"Error closing gate: {str(e)}")
            return {
                'success': False,
                'status': 'error',
                'message': str(e)
            }
    
    def get_status(self) -> dict:
        """
        Get gate status
        
        Returns:
            Current gate status
        """
        return {
            'is_open': self.is_open,
            'state': self.state,
            'timestamp': time.time()
        }
    
    def emergency_stop(self) -> dict:
        """
        Emergency stop gate
        
        Returns:
            dict: Operation result
        """
        self.state = 'closed'
        self.is_open = False
        logger.warning("Emergency stop activated")
        return {
            'success': True,
            'message': 'Emergency stop activated',
            'status': 'closed'
        }
