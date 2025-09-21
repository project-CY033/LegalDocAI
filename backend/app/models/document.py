from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from app.core.database import Base

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    # Document metadata
    filename = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)  # in bytes
    file_type = Column(String, nullable=False)  # pdf, docx, txt
    mime_type = Column(String, nullable=False)
    
    # Document content
    extracted_text = Column(Text, nullable=True)
    page_count = Column(Integer, nullable=True)
    word_count = Column(Integer, nullable=True)
    
    # Processing status
    status = Column(String, default="uploaded")  # uploaded, processing, completed, failed
    processing_started_at = Column(DateTime, nullable=True)
    processing_completed_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Document classification
    document_type = Column(String, nullable=True)  # rental_agreement, loan_contract, tos, etc.
    confidence_score = Column(Float, nullable=True)
    language = Column(String, default="en")
    
    # Security and privacy
    is_sensitive = Column(Boolean, default=True)
    retention_days = Column(Integer, default=30)
    
    # Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="documents")
    analyses = relationship("Analysis", back_populates="document", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Document(id={self.id}, filename={self.filename}, status={self.status})>"