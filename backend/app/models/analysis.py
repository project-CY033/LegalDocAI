from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from app.core.database import Base

class Analysis(Base):
    __tablename__ = "analyses"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    document_id = Column(String, ForeignKey("documents.id"), nullable=False)
    
    # Analysis type and configuration
    analysis_type = Column(String, nullable=False)  # full_summary, risk_assessment, clause_explanation, qa
    request_data = Column(JSON, nullable=True)  # Store original request parameters
    
    # AI Model information
    model_used = Column(String, nullable=False)  # gemini-pro, gemini-pro-vision, etc.
    model_version = Column(String, nullable=True)
    prompt_template = Column(Text, nullable=True)
    
    # Analysis results
    summary = Column(Text, nullable=True)
    simplified_explanation = Column(Text, nullable=True)
    key_points = Column(JSON, nullable=True)  # Array of important points
    risk_assessment = Column(JSON, nullable=True)  # Risk levels and explanations
    legal_implications = Column(JSON, nullable=True)  # Legal consequences and advice
    
    # Clause-specific analysis
    clauses_analyzed = Column(JSON, nullable=True)  # Array of clause objects
    problematic_clauses = Column(JSON, nullable=True)  # Highlighted concerning clauses
    
    # Q&A specific
    question = Column(Text, nullable=True)
    answer = Column(Text, nullable=True)
    confidence_score = Column(Float, nullable=True)
    
    # Translation and localization
    source_language = Column(String, default="en")
    target_language = Column(String, default="en")
    
    # Processing metadata
    processing_time_seconds = Column(Float, nullable=True)
    token_count_input = Column(Integer, nullable=True)
    token_count_output = Column(Integer, nullable=True)
    
    # Status and quality
    status = Column(String, default="pending")  # pending, processing, completed, failed
    quality_score = Column(Float, nullable=True)  # AI-generated quality assessment
    human_reviewed = Column(Boolean, default=False)
    
    # User feedback
    user_rating = Column(Integer, nullable=True)  # 1-5 rating
    user_feedback = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="analyses")
    document = relationship("Document", back_populates="analyses")
    
    def __repr__(self):
        return f"<Analysis(id={self.id}, type={self.analysis_type}, status={self.status})>"