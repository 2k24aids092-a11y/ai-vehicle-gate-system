import re

def validate_plate_number(plate: str) -> bool:
    """Validate vehicle plate number format"""
    # Indian plate format: TN37AB1234
    pattern = r'^[A-Z]{2}\d{2}[A-Z]{2}\d{4}$'
    return bool(re.match(pattern, plate))

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
