from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import json
from typing import Dict, Any, List
import uuid
from datetime import datetime, timezone
import structlog

# Configure structured logging
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
    title="LegalDocAI API (Demo Mode)",
    description="AI-powered legal document simplification platform - Demo Version",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for demo
demo_documents = {}
demo_analyses = {}

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to LegalDocAI API - Demo Mode",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "note": "This is running in demo mode without database"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "mode": "demo",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.post("/api/v1/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    """Demo document upload endpoint."""
    
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
        "filename": f"demo_{file.filename}",
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
    
    logger.info("Demo document uploaded", document_id=doc_id, filename=file.filename)
    
    return document

@app.get("/api/v1/documents/")
async def list_documents():
    """List demo documents."""
    return {
        "documents": list(demo_documents.values()),
        "total": len(demo_documents),
        "skip": 0,
        "limit": 100
    }

@app.get("/api/v1/documents/{document_id}")
async def get_document(document_id: str):
    """Get demo document."""
    if document_id not in demo_documents:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return demo_documents[document_id]

@app.post("/api/v1/analysis/analyze/{document_id}")
async def analyze_document(document_id: str, request: Dict[str, Any]):
    """Demo document analysis endpoint."""
    
    if document_id not in demo_documents:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Create mock analysis based on document type
    document = demo_documents[document_id]
    analysis_id = str(uuid.uuid4())
    
    # Mock analysis results
    if document["document_type"] == "rental_agreement":
        analysis_result = {
            "id": analysis_id,
            "analysis_type": request.get("analysis_type", "full_summary"),
            "status": "completed",
            "summary": "This is a standard residential lease agreement with monthly rent of $1,200. The lease term is 12 months starting January 1, 2024. Key provisions include a $1,800 security deposit, pet restrictions, and standard maintenance responsibilities.",
            "simplified_explanation": "This rental agreement means you'll pay $1,200 every month for rent. You need to put down $1,800 as a security deposit (you'll get this back if you don't damage the place). The lease lasts for one year. You can't have pets without permission, and you're responsible for keeping the place clean while the landlord handles major repairs.",
            "key_points": [
                "Monthly rent: $1,200 due on the 1st of each month",
                "Security deposit: $1,800 (refundable with conditions)",
                "Lease term: 12 months",
                "No pets allowed without written permission",
                "Tenant responsible for utilities except water/sewer"
            ],
            "risk_assessment": {
                "high_risk_items": ["No grace period for late rent payment"],
                "medium_risk_items": ["Automatic lease renewal clause", "Tenant pays for minor repairs"],
                "protective_clauses": ["30-day notice required for landlord entry", "Security deposit return procedure outlined"]
            },
            "legal_implications": {
                "rights": ["Right to quiet enjoyment", "Right to habitable premises", "Right to privacy"],
                "obligations": ["Pay rent on time", "Maintain cleanliness", "Follow building rules"],
                "consequences": ["Eviction for non-payment", "Loss of security deposit for damages", "Legal action for lease violations"]
            },
            "confidence_score": 0.92,
            "processing_time_seconds": 2.3,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "completed_at": datetime.now(timezone.utc).isoformat()
        }
    else:
        analysis_result = {
            "id": analysis_id,
            "analysis_type": request.get("analysis_type", "full_summary"),
            "status": "completed",
            "summary": "This appears to be a general legal document with standard terms and conditions. The document contains typical legal language and clauses commonly found in agreements of this type.",
            "simplified_explanation": "This is a legal agreement that sets out the rules and terms between the parties involved. It includes what each side needs to do and what happens if someone doesn't follow the rules.",
            "key_points": [
                "Document establishes legal relationship between parties",
                "Contains standard terms and conditions",
                "Includes dispute resolution procedures",
                "Specifies obligations and rights of each party"
            ],
            "risk_assessment": {
                "high_risk_items": ["Review needed for specific clause analysis"],
                "medium_risk_items": ["Standard legal language requires careful reading"],
                "protective_clauses": ["Dispute resolution clause present"]
            },
            "confidence_score": 0.75,
            "processing_time_seconds": 1.8,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "completed_at": datetime.now(timezone.utc).isoformat()
        }
    
    demo_analyses[analysis_id] = analysis_result
    
    logger.info("Demo analysis completed", analysis_id=analysis_id, document_id=document_id)
    
    return analysis_result

@app.post("/api/v1/analysis/question/{document_id}")
async def ask_question(document_id: str, request: Dict[str, Any]):
    """Demo Q&A endpoint."""
    
    if document_id not in demo_documents:
        raise HTTPException(status_code=404, detail="Document not found")
    
    question = request.get("question", "")
    
    # Mock Q&A responses
    mock_answers = {
        "rent": "Based on the document, the monthly rent is $1,200 and is due on the 1st of each month. Late payments may incur additional fees.",
        "deposit": "The security deposit is $1,800. This will be returned within 30 days after you move out, minus any deductions for damages beyond normal wear and tear.",
        "pets": "Pets are not allowed without written permission from the landlord. If you want to have a pet, you'll need to ask for approval first.",
        "maintenance": "You are responsible for basic maintenance and cleanliness. The landlord handles major repairs and structural issues.",
        "termination": "The lease can be terminated with proper notice as specified in the agreement. Early termination may result in penalties."
    }
    
    # Simple keyword matching for demo
    answer = "I'd be happy to help answer your question about the document. "
    for keyword, response in mock_answers.items():
        if keyword.lower() in question.lower():
            answer = response
            break
    else:
        answer = "Based on the document analysis, this appears to be a standard legal agreement. For specific details about your question, I recommend reviewing the relevant sections of the document or consulting with a legal professional."
    
    response = {
        "question": question,
        "answer": answer,
        "confidence_score": 0.85,
        "analysis_id": str(uuid.uuid4())
    }
    
    logger.info("Demo question answered", question=question[:50])
    
    return response

@app.get("/api/v1/analysis/")
async def list_analyses():
    """List demo analyses."""
    return {
        "analyses": list(demo_analyses.values()),
        "total": len(demo_analyses),
        "skip": 0,
        "limit": 100
    }

# Demo auth endpoints
@app.post("/api/v1/auth/login")
async def demo_login(credentials: Dict[str, str]):
    """Demo login endpoint."""
    return {
        "access_token": "demo-jwt-token-12345",
        "token_type": "bearer",
        "expires_in": 3600,
        "user": {
            "id": "demo-user-id",
            "email": credentials.get("email", "demo@example.com"),
            "full_name": "Demo User",
            "is_active": True,
            "documents_processed": len(demo_documents),
            "api_calls_count": len(demo_analyses)
        }
    }

@app.post("/api/v1/auth/register")
async def demo_register(user_data: Dict[str, str]):
    """Demo registration endpoint."""
    return {
        "id": "demo-user-id",
        "email": user_data.get("email", "demo@example.com"),
        "full_name": user_data.get("full_name", "Demo User"),
        "is_active": True,
        "created_at": datetime.now(timezone.utc).isoformat()
    }

@app.get("/api/v1/users/me")
async def get_current_user():
    """Demo user info endpoint."""
    return {
        "id": "demo-user-id",
        "email": "demo@example.com",
        "full_name": "Demo User",
        "is_active": True,
        "documents_processed": len(demo_documents),
        "api_calls_count": len(demo_analyses),
        "created_at": "2024-01-01T00:00:00"
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting LegalDocAI Demo Server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)