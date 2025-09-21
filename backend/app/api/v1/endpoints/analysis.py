from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone
import structlog

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.models.document import Document
from app.models.analysis import Analysis
from app.services.ai_analyzer import AIAnalyzer
from app.schemas import (
    AnalysisRequest, AnalysisResponse, AnalysisList,
    QuestionRequest, QuestionResponse
)

logger = structlog.get_logger()
router = APIRouter()

@router.post("/analyze/{document_id}", response_model=AnalysisResponse)
async def analyze_document(
    document_id: str,
    request: AnalysisRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Perform AI analysis on a document."""
    
    # Verify document exists and belongs to user
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    if document.status != "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Document processing not completed"
        )
    
    try:
        # Create analysis record
        analysis = Analysis(
            user_id=current_user.id,
            document_id=document_id,
            analysis_type=request.analysis_type,
            request_data=request.dict(),
            status="processing"
        )
        
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        
        # Perform AI analysis
        analyzer = AIAnalyzer()
        result = await analyzer.analyze_document(
            document=document,
            analysis_type=request.analysis_type,
            language=request.language or "en",
            focus_areas=request.focus_areas
        )
        
        # Update analysis with results
        analysis.status = "completed"
        analysis.summary = result.get("summary")
        analysis.simplified_explanation = result.get("simplified_explanation")
        analysis.key_points = result.get("key_points")
        analysis.risk_assessment = result.get("risk_assessment")
        analysis.legal_implications = result.get("legal_implications")
        analysis.clauses_analyzed = result.get("clauses_analyzed")
        analysis.problematic_clauses = result.get("problematic_clauses")
        analysis.processing_time_seconds = result.get("processing_time")
        analysis.confidence_score = result.get("confidence_score")
        analysis.completed_at = datetime.now(timezone.utc)
        
        db.commit()
        db.refresh(analysis)
        
        logger.info("Document analysis completed", 
                   analysis_id=analysis.id,
                   document_id=document_id,
                   analysis_type=request.analysis_type)
        
        return AnalysisResponse.from_orm(analysis)
        
    except Exception as e:
        logger.error("Document analysis failed", error=str(e))
        if 'analysis' in locals():
            analysis.status = "failed"
            analysis.error_message = str(e)
            db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Analysis failed"
        )

@router.post("/question/{document_id}", response_model=QuestionResponse)
async def ask_question(
    document_id: str,
    request: QuestionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Ask a specific question about a document."""
    
    # Verify document exists and belongs to user
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    try:
        # Create Q&A analysis record
        analysis = Analysis(
            user_id=current_user.id,
            document_id=document_id,
            analysis_type="qa",
            question=request.question,
            status="processing"
        )
        
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        
        # Get answer from AI
        analyzer = AIAnalyzer()
        result = await analyzer.answer_question(
            document=document,
            question=request.question,
            language=request.language or "en"
        )
        
        # Update analysis with answer
        analysis.status = "completed"
        analysis.answer = result.get("answer")
        analysis.confidence_score = result.get("confidence_score")
        analysis.processing_time_seconds = result.get("processing_time")
        analysis.completed_at = datetime.now(timezone.utc)
        
        db.commit()
        db.refresh(analysis)
        
        logger.info("Question answered", 
                   analysis_id=analysis.id,
                   document_id=document_id)
        
        return QuestionResponse(
            question=analysis.question,
            answer=analysis.answer,
            confidence_score=analysis.confidence_score,
            analysis_id=analysis.id
        )
        
    except Exception as e:
        logger.error("Question answering failed", error=str(e))
        if 'analysis' in locals():
            analysis.status = "failed"
            db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to answer question"
        )

@router.get("/", response_model=AnalysisList)
async def list_analyses(
    document_id: Optional[str] = None,
    analysis_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List user's analyses."""
    
    query = db.query(Analysis).filter(Analysis.user_id == current_user.id)
    
    if document_id:
        query = query.filter(Analysis.document_id == document_id)
    
    if analysis_type:
        query = query.filter(Analysis.analysis_type == analysis_type)
    
    total = query.count()
    analyses = query.order_by(Analysis.created_at.desc()).offset(skip).limit(limit).all()
    
    return AnalysisList(
        analyses=[AnalysisResponse.from_orm(analysis) for analysis in analyses],
        total=total,
        skip=skip,
        limit=limit
    )

@router.get("/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(
    analysis_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific analysis."""
    
    analysis = db.query(Analysis).filter(
        Analysis.id == analysis_id,
        Analysis.user_id == current_user.id
    ).first()
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    return AnalysisResponse.from_orm(analysis)

@router.post("/{analysis_id}/feedback")
async def submit_feedback(
    analysis_id: str,
    rating: int,
    feedback: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit feedback for an analysis."""
    
    if not 1 <= rating <= 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating must be between 1 and 5"
        )
    
    analysis = db.query(Analysis).filter(
        Analysis.id == analysis_id,
        Analysis.user_id == current_user.id
    ).first()
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    analysis.user_rating = rating
    analysis.user_feedback = feedback
    
    db.commit()
    
    logger.info("Analysis feedback submitted", 
               analysis_id=analysis_id,
               rating=rating)
    
    return {"message": "Feedback submitted successfully"}