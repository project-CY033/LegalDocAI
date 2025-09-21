from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import structlog

from app.core.database import get_db
from app.core.auth import create_access_token, get_password_hash, verify_password
from app.models.user import User
from app.schemas import UserCreate, UserResponse, LoginRequest, LoginResponse
from app.core.config import settings

logger = structlog.get_logger()
router = APIRouter()
security = HTTPBearer()

@router.post("/register", response_model=UserResponse)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Register a new user."""
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    try:
        # Create new user
        hashed_password = get_password_hash(user_data.password) if user_data.password else None
        
        user = User(
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=hashed_password,
            firebase_uid=user_data.firebase_uid,
            company=user_data.company,
            role=user_data.role,
            preferred_language=user_data.preferred_language or "en"
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        logger.info("User registered successfully", user_id=user.id, email=user.email)
        
        return UserResponse.from_orm(user)
        
    except Exception as e:
        logger.error("User registration failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )

@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """Login user and return access token."""
    
    # Find user by email
    user = db.query(User).filter(User.email == login_data.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # For Firebase users, we might handle authentication differently
    if user.firebase_uid and not login_data.password:
        # Firebase authentication would be handled on the frontend
        # Here we just create a token for the authenticated user
        pass
    elif user.hashed_password and login_data.password:
        # Verify password for email/password users
        if not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication method"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is disabled"
        )
    
    # Update last login
    user.last_login = datetime.now(timezone.utc)
    db.commit()
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    
    logger.info("User logged in successfully", user_id=user.id, email=user.email)
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse.from_orm(user)
    )

@router.post("/firebase-auth", response_model=LoginResponse)
async def firebase_auth(
    firebase_token: str,
    db: Session = Depends(get_db)
):
    """Authenticate user with Firebase token."""
    
    # This would typically verify the Firebase token
    # For now, we'll create a placeholder implementation
    # In production, you would:
    # 1. Verify the Firebase ID token
    # 2. Extract user information
    # 3. Create or update user in database
    # 4. Return JWT token for API access
    
    try:
        # Placeholder - in production, verify Firebase token here
        # firebase_user = verify_firebase_token(firebase_token)
        
        # For now, we'll create a demo response
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Firebase authentication not yet implemented"
        )
        
    except Exception as e:
        logger.error("Firebase authentication failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Firebase authentication failed"
        )

@router.post("/refresh")
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Refresh access token."""
    
    # This would typically handle token refresh
    # For now, return not implemented
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Token refresh not yet implemented"
    )

@router.post("/logout")
async def logout():
    """Logout user (primarily for token invalidation on client side)."""
    
    return {"message": "Logged out successfully"}

@router.post("/forgot-password")
async def forgot_password(email: str, db: Session = Depends(get_db)):
    """Send password reset email."""
    
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        # Don't reveal whether email exists or not
        return {"message": "If email exists, password reset instructions have been sent"}
    
    # In production, you would:
    # 1. Generate password reset token
    # 2. Send email with reset link
    # 3. Store reset token in database with expiry
    
    logger.info("Password reset requested", email=email)
    
    return {"message": "If email exists, password reset instructions have been sent"}