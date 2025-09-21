from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import json
from typing import Dict, Any, List
import uuid
from datetime import datetime, timezone
import structlog

# Configure structured logging for Vercel
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.dev.ConsoleRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Initialize FastAPI app
app = FastAPI(
    title="LegalDocAI API",
    description="AI-powered legal document simplification platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware - configured for Vercel deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this based on your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for demo (use a real database in production)
demo_documents = {}
demo_analyses = {}

@app.get("/")
@app.get("/api")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to LegalDocAI API",
        "version": "1.0.0",
        "docs": "/api/docs",
        "health": "/api/health",
        "status": "running",
        "environment": "production"
    }

@app.get("/api/health")
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "environment": "vercel",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.post("/api/v1/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    """Document upload endpoint for Vercel deployment."""
    
    # Validate file type
    allowed_types = [".pdf", ".docx", ".txt"]
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Supported types: {', '.join(allowed_types)}"
        )
    
    # Create mock document
    doc_id = str(uuid.uuid4())
    document = {
        "id": doc_id,
        "filename": f"vercel_{file.filename}",
        "original_filename": file.filename,
        "file_size": file.size or 1024,
        "file_type": file_extension,
        "document_type": "rental_agreement" if "lease" in file.filename.lower() else "general_legal",
        "status": "completed",
        "page_count": 5,
        "word_count": 1200,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    
    demo_documents[doc_id] = document
    
    logger.info("Document uploaded on Vercel", document_id=doc_id, filename=file.filename)
    
    return document

@app.get("/api/v1/documents/")
async def list_documents():
    """List documents."""
    return {
        "documents": list(demo_documents.values()),
        "total": len(demo_documents),
        "skip": 0,
        "limit": 100
    }

@app.get("/api/v1/documents/{document_id}")
async def get_document(document_id: str):
    """Get specific document."""
    if document_id not in demo_documents:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return demo_documents[document_id]

@app.post("/api/v1/analysis/analyze/{document_id}")
async def analyze_document(document_id: str, request: Dict[str, Any]):
    """Document analysis endpoint."""
    
    if document_id not in demo_documents:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Create mock analysis based on document type
    document = demo_documents[document_id]
    analysis_id = str(uuid.uuid4())
    
    # Mock analysis results optimized for Vercel
    analysis_result = {
        "id": analysis_id,
        "analysis_type": request.get("analysis_type", "full_summary"),
        "status": "completed",
        "summary": "This is a comprehensive legal document analysis performed on Vercel serverless infrastructure. The document has been processed using AI-powered analysis to provide clear, accessible explanations.",
        "simplified_explanation": "This document contains legal terms that have been simplified for better understanding. All key provisions have been analyzed and explained in plain language.",
        "key_points": [
            "Document processed successfully on Vercel",
            "AI analysis completed with high confidence",
            "All major clauses identified and explained",
            "Risk assessment performed on key terms"
        ],
        "risk_assessment": {
            "high_risk_items": ["Complex legal language requiring careful review"],
            "medium_risk_items": ["Standard clauses with typical conditions"],
            "protective_clauses": ["User rights and protections clearly outlined"]
        },
        "confidence_score": 0.88,
        "processing_time_seconds": 1.2,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "completed_at": datetime.now(timezone.utc).isoformat()
    }
    
    demo_analyses[analysis_id] = analysis_result
    
    logger.info("Analysis completed on Vercel", analysis_id=analysis_id, document_id=document_id)
    
    return analysis_result

@app.post("/api/v1/analysis/question/{document_id}")
async def ask_question(document_id: str, request: Dict[str, Any]):
    """Q&A endpoint for document questions."""
    
    if document_id not in demo_documents:
        raise HTTPException(status_code=404, detail="Document not found")
    
    question = request.get("question", "")
    
    # Mock Q&A responses optimized for Vercel
    mock_answers = {
        "rent": "Based on the document analysis performed on Vercel, the rental terms are clearly defined with specific payment schedules.",
        "deposit": "The security deposit information has been extracted and analyzed. All conditions for deposit return are outlined.",
        "terms": "The key terms have been identified and simplified for your understanding using our AI analysis.",
        "rights": "Your rights under this document have been analyzed and are clearly explained in plain language.",
        "obligations": "Your obligations have been identified and summarized for easy understanding."
    }
    
    # Simple keyword matching for demo
    answer = "Based on our Vercel-powered AI analysis, this document has been thoroughly reviewed. "
    for keyword, response in mock_answers.items():
        if keyword.lower() in question.lower():
            answer = response
            break
    else:
        answer = "Your question has been processed using our AI analysis system. Based on the document review, I can provide specific insights about the terms and conditions outlined in your document."
    
    response = {
        "question": question,
        "answer": answer,
        "confidence_score": 0.85,
        "analysis_id": str(uuid.uuid4())
    }
    
    logger.info("Question answered on Vercel", question=question[:50])
    
    return response

@app.get("/api/v1/analysis/")
async def list_analyses():
    """List all analyses."""
    return {
        "analyses": list(demo_analyses.values()),
        "total": len(demo_analyses),
        "skip": 0,
        "limit": 100
    }

# Auth endpoints for demo
@app.post("/api/v1/auth/login")
async def demo_login(credentials: Dict[str, str]):
    """Demo login endpoint."""
    return {
        "access_token": "vercel-demo-jwt-token-12345",
        "token_type": "bearer",
        "expires_in": 3600,
        "user": {
            "id": "vercel-demo-user-id",
            "email": credentials.get("email", "demo@legaldocai.com"),
            "full_name": "Vercel Demo User",
            "is_active": True,
            "documents_processed": len(demo_documents),
            "api_calls_count": len(demo_analyses)
        }
    }

@app.post("/api/v1/auth/register")
async def demo_register(user_data: Dict[str, str]):
    """Demo registration endpoint."""
    return {
        "id": "vercel-demo-user-id",
        "email": user_data.get("email", "demo@legaldocai.com"),
        "full_name": user_data.get("full_name", "Vercel Demo User"),
        "is_active": True,
        "created_at": datetime.now(timezone.utc).isoformat()
    }

@app.get("/api/v1/users/me")
async def get_current_user():
    """Demo user info endpoint."""
    return {
        "id": "vercel-demo-user-id",
        "email": "demo@legaldocai.com",
        "full_name": "Vercel Demo User",
        "is_active": True,
        "documents_processed": len(demo_documents),
        "api_calls_count": len(demo_analyses),
        "created_at": "2024-01-01T00:00:00",
        "platform": "vercel"
    }

# This is the handler function for Vercel
def handler(request, response):
    """Vercel serverless function handler."""
    return app(request, response)

# For local development
if __name__ == "__main__":
    import uvicorn
    logger.info("Starting LegalDocAI on Vercel...")
    uvicorn.run(app, host="0.0.0.0", port=8000)