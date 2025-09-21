from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON, Float
from datetime import datetime, timezone
import uuid

from app.core.database import Base

class LegalTemplate(Base):
    __tablename__ = "legal_templates"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Template identification
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)  # rental_agreement, loan_contract, employment, etc.
    subcategory = Column(String, nullable=True)  # residential_lease, commercial_lease, etc.
    
    # Template content
    description = Column(Text, nullable=False)
    common_clauses = Column(JSON, nullable=False)  # Array of typical clauses
    risk_factors = Column(JSON, nullable=False)  # Common risks to look for
    
    # Analysis guidelines
    key_terms_to_check = Column(JSON, nullable=False)  # Important terms to highlight
    red_flags = Column(JSON, nullable=False)  # Warning signs to flag
    standard_protections = Column(JSON, nullable=True)  # What protections should exist
    
    # Explanation templates
    simplified_language = Column(JSON, nullable=True)  # Plain language explanations
    question_templates = Column(JSON, nullable=True)  # Common questions users ask
    
    # Jurisdictional information
    jurisdiction = Column(String, default="US")  # Legal jurisdiction
    applicable_laws = Column(JSON, nullable=True)  # Relevant laws and regulations
    
    # Template metadata
    version = Column(String, default="1.0")
    is_active = Column(Boolean, default=True)
    usage_count = Column(Integer, default=0)
    effectiveness_score = Column(Float, nullable=True)  # Based on user feedback
    
    # Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    last_used = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<LegalTemplate(id={self.id}, name={self.name}, category={self.category})>"