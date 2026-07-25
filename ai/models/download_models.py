#!/usr/bin/env python3
"""
Download required AI models for vehicle detection and plate recognition
"""

import os
import sys
from pathlib import Path

print("="*60)
print("  AI Model Downloader")
print("="*60)

# Create models directory
models_dir = Path(__file__).parent
models_dir.mkdir(exist_ok=True)

print("\n[1/3] Downloading YOLOv8s model...")
try:
    from ultralytics import YOLO
    model = YOLO('yolov8s.pt')
    print("✓ YOLOv8s model downloaded successfully")
except Exception as e:
    print(f"✗ Error downloading YOLOv8s: {e}")
    sys.exit(1)

print("\n[2/3] Initializing EasyOCR...")
try:
    import easyocr
    reader = easyocr.Reader(['en'])
    print("✓ EasyOCR initialized successfully")
except Exception as e:
    print(f"✗ Error initializing EasyOCR: {e}")
    sys.exit(1)

print("\n[3/3] Verifying installations...")
try:
    import cv2
    print(f"✓ OpenCV {cv2.__version__} available")
    import numpy as np
    print(f"✓ NumPy {np.__version__} available")
    print("\n" + "="*60)
    print("  All models downloaded successfully!")
    print("="*60)
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)
