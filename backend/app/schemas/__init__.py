from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# User schemas
class UserCreate(BaseModel):
    email: str = Field(..., description="User email address")
    full_name: str = Field(..., description="User's full name")
    password: Optional[str] = Field(None, description="Password for email/password auth")
    firebase_uid: Optional[str] = Field(None, description="Firebase UID for OAuth users")
    company: Optional[str] = Field(None, description="User's company")
    role: Optional[str] = Field(None, description="User's role")
    preferred_language: Optional[str] = Field(default="en", description="Preferred language")

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    is_active: bool
    is_verified: bool
    company: Optional[str]
    role: Optional[str]
    preferred_language: str
    created_at: datetime
    last_login: Optional[datetime]
    documents_processed: int
    api_calls_count: int
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    company: Optional[str] = None
    role: Optional[str] = None
    preferred_language: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: Optional[str] = None  # Optional for Firebase auth
    firebase_token: Optional[str] = None

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse

# Document schemas
class DocumentCreate(BaseModel):
    filename: str
    description: Optional[str] = None

class DocumentResponse(BaseModel):
    id: str
    filename: str
    original_filename: str
    file_size: int
    file_type: str
    document_type: Optional[str]
    status: str
    page_count: Optional[int]
    word_count: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class DocumentList(BaseModel):
    documents: List[DocumentResponse]
    total: int
    skip: int
    limit: int

# Analysis schemas
class AnalysisRequest(BaseModel):
    analysis_type: str = Field(..., description="Type of analysis: full_summary, risk_assessment, clause_explanation")
    language: Optional[str] = Field(default="en", description="Language for the analysis")
    focus_areas: Optional[List[str]] = Field(default=None, description="Specific areas to focus on")

class AnalysisResponse(BaseModel):
    id: str
    analysis_type: str
    status: str
    summary: Optional[str]
    simplified_explanation: Optional[str]
    key_points: Optional[List[str]]
    risk_assessment: Optional[Dict[str, Any]]
    legal_implications: Optional[Dict[str, Any]]
    clauses_analyzed: Optional[List[Dict[str, Any]]]
    problematic_clauses: Optional[List[Dict[str, Any]]]
    confidence_score: Optional[float]
    processing_time_seconds: Optional[float]
    created_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class AnalysisList(BaseModel):
    analyses: List[AnalysisResponse]
    total: int
    skip: int
    limit: int

class QuestionRequest(BaseModel):
    question: str = Field(..., description="Question about the document")
    language: Optional[str] = Field(default="en", description="Language for the response")

class QuestionResponse(BaseModel):
    question: str
    answer: str
    confidence_score: Optional[float]
    analysis_id: str