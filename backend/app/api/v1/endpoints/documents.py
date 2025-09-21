from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import aiofiles
import uuid
from datetime import datetime, timedelta
import structlog

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.models.document import Document
from app.services.document_processor import DocumentProcessor
from app.schemas import DocumentCreate, DocumentResponse, DocumentList
from app.core.config import settings

logger = structlog.get_logger()
router = APIRouter()

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload a legal document for analysis."""
    
    # Validate file type
    if not file.filename.lower().endswith(tuple(settings.ALLOWED_FILE_TYPES)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Supported types: {', '.join(settings.ALLOWED_FILE_TYPES)}"
        )
    
    # Check file size
    if file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE / 1024 / 1024}MB"
        )
    
    try:
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
        
        # Save file
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Create document record
        document = Document(
            user_id=current_user.id,
            filename=unique_filename,
            original_filename=file.filename,
            file_path=file_path,
            file_size=file.size,
            file_type=file_extension.lower(),
            mime_type=file.content_type,
            status="uploaded"
        )
        
        db.add(document)
        db.commit()
        db.refresh(document)
        
        # Start background processing
        processor = DocumentProcessor()
        await processor.process_document_async(document.id, db)
        
        logger.info("Document uploaded successfully", 
                   document_id=document.id, 
                   filename=file.filename,
                   user_id=current_user.id)
        
        return DocumentResponse.from_orm(document)
        
    except Exception as e:
        logger.error("Document upload failed", error=str(e))
        # Clean up file if it was created
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload document"
        )

@router.get("/", response_model=DocumentList)
async def list_documents(
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List user's documents."""
    
    query = db.query(Document).filter(Document.user_id == current_user.id)
    
    if status_filter:
        query = query.filter(Document.status == status_filter)
    
    total = query.count()
    documents = query.offset(skip).limit(limit).all()
    
    return DocumentList(
        documents=[DocumentResponse.from_orm(doc) for doc in documents],
        total=total,
        skip=skip,
        limit=limit
    )

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific document."""
    
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    return DocumentResponse.from_orm(document)

@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a document and its associated file."""
    
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
        # Remove physical file
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
        
        # Delete from database (cascades to analyses)
        db.delete(document)
        db.commit()
        
        logger.info("Document deleted successfully", 
                   document_id=document_id,
                   user_id=current_user.id)
        
        return {"message": "Document deleted successfully"}
        
    except Exception as e:
        logger.error("Document deletion failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete document"
        )

@router.get("/{document_id}/download")
async def download_document(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Download the original document file."""
    
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    if not os.path.exists(document.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document file not found"
        )
    
    return FileResponse(
        path=document.file_path,
        filename=document.original_filename,
        media_type=document.mime_type
    )