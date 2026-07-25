from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate, LoginRequest
from app.utils import hash_password, verify_password, create_access_token
from fastapi import HTTPException, status

class AuthService:
    """Authentication service"""
    
    @staticmethod
    def create_user(db: Session, user: UserCreate):
        """Create new user"""
        # Check if user exists
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )
        
        # Create new user
        db_user = User(
            email=user.email,
            password_hash=hash_password(user.password),
            name=user.name,
            role=user.role
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def login(db: Session, credentials: LoginRequest):
        """Authenticate user and return token"""
        # Find user by email
        user = db.query(User).filter(User.email == credentials.email).first()
        
        if not user or not verify_password(credentials.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
        
        # Create token
        access_token = create_access_token(
            data={"sub": user.email, "user_id": user.id, "role": user.role}
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }
    
    @staticmethod
    def get_user_by_email(db: Session, email: str):
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
