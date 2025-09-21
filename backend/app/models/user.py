from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=True)  # Nullable for OAuth users
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    firebase_uid = Column(String, unique=True, index=True, nullable=True)  # For Firebase Auth
    
    # Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    last_login = Column(DateTime, nullable=True)
    
    # Profile information
    company = Column(String, nullable=True)
    role = Column(String, nullable=True)
    preferred_language = Column(String, default="en")
    
    # Usage statistics
    documents_processed = Column(Integer, default=0)
    api_calls_count = Column(Integer, default=0)
    
    # Relationships
    documents = relationship("Document", back_populates="user", cascade="all, delete-orphan")
    analyses = relationship("Analysis", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"