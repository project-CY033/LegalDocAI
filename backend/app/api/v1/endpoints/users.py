from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import structlog

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.schemas import UserResponse, UserUpdate

logger = structlog.get_logger()
router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user's information."""
    return UserResponse.from_orm(current_user)

@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user's information."""
    
    try:
        # Update user fields
        if user_data.full_name is not None:
            current_user.full_name = user_data.full_name
        if user_data.company is not None:
            current_user.company = user_data.company
        if user_data.role is not None:
            current_user.role = user_data.role
        if user_data.preferred_language is not None:
            current_user.preferred_language = user_data.preferred_language
        
        db.commit()
        db.refresh(current_user)
        
        logger.info("User updated successfully", user_id=current_user.id)
        
        return UserResponse.from_orm(current_user)
        
    except Exception as e:
        logger.error("User update failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Update failed"
        )

@router.get("/stats")
async def get_user_stats(current_user: User = Depends(get_current_user)):
    """Get user usage statistics."""
    
    return {
        "documents_processed": current_user.documents_processed,
        "api_calls_count": current_user.api_calls_count,
        "member_since": current_user.created_at,
        "last_login": current_user.last_login
    }

@router.delete("/me")
async def delete_current_user(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete current user account."""
    
    try:
        # In production, you might want to:
        # 1. Soft delete instead of hard delete
        # 2. Clean up associated files
        # 3. Send confirmation email
        # 4. Add grace period for account recovery
        
        db.delete(current_user)
        db.commit()
        
        logger.info("User account deleted", user_id=current_user.id)
        
        return {"message": "Account deleted successfully"}
        
    except Exception as e:
        logger.error("User deletion failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Account deletion failed"
        )