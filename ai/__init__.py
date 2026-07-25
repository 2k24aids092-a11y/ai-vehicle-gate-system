#!/usr/bin/env python3
"""
AI Module - Vehicle Detection and Plate Recognition

This module handles:
- Vehicle detection using YOLOv8
- License plate recognition using EasyOCR
- Camera interface abstraction
- Gate control (simulated or ESP32)
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.vehicle_detector import VehicleDetector
from models.plate_recognizer import PlateRecognizer
from camera.webcam_handler import WebcamHandler
from camera.cctv_handler import CCTVCamera
from hardware.gate_simulator import GateSimulator
from hardware.esp32_controller import ESP32GateController

__all__ = [
    'VehicleDetector',
    'PlateRecognizer',
    'WebcamHandler',
    'CCTVCamera',
    'GateSimulator',
    'ESP32GateController'
]
