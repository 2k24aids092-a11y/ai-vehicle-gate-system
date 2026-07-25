from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from app.utils import verify_token

security = HTTPBearer()

async def verify_token_middleware(credentials: HTTPAuthCredentials = Depends(security)):
    """Verify JWT token from Authorization header"""
    token = credentials.credentials
    payload = verify_token(token)
    
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return payload
