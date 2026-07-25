from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from app.schemas import UserCreate, UserResponse, LoginRequest, LoginResponse
from app.services import AuthService
from app.middleware import verify_token_middleware

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
async def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """User login"""
    result = AuthService.login(db, credentials)
    return {
        "access_token": result["access_token"],
        "token_type": result["token_type"],
        "user": UserResponse.from_orm(result["user"])
    }

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """User registration"""
    new_user = AuthService.create_user(db, user)
    return UserResponse.from_orm(new_user)

@router.get("/me", response_model=UserResponse)
async def get_current_user(
    payload: dict = Depends(verify_token_middleware),
    db: Session = Depends(get_db)
):
    """Get current user information"""
    email = payload.get("sub")
    user = AuthService.get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserResponse.from_orm(user)
