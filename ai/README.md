# AI Module - Vehicle Detection & Plate Recognition

## Models

### Vehicle Detector (YOLOv8)
```python
from models.vehicle_detector import VehicleDetector

detector = VehicleDetector('models/yolov8s.pt', confidence_threshold=0.5)
result = detector.detect(frame)
```

### Plate Recognizer (EasyOCR)
```python
from models.plate_recognizer import PlateRecognizer

recognizer = PlateRecognizer(languages=['en'])
result = recognizer.recognize_plate(plate_image)
```

## Camera Interfaces

### Webcam
```python
from camera.webcam_handler import WebcamHandler

camera = WebcamHandler(camera_id=0, width=1280, height=720)
frame = camera.get_frame()
```

### CCTV (Future)
```python
from camera.cctv_handler import CCTVCamera

camera = CCTVCamera(ip='192.168.1.100')
camera.connect()
```

## Gate Control

### Simulator (Development)
```python
from hardware.gate_simulator import GateSimulator

gate = GateSimulator(opening_delay=2)
gate.open()
```

### ESP32 (Production)
```python
from hardware.esp32_controller import ESP32GateController

gate = ESP32GateController(port='COM3')
gate.connect()
gate.open_gate()
```
