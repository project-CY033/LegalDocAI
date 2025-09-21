import os
import asyncio
from typing import Optional
from datetime import datetime, timezone
import PyPDF2
from docx import Document as DocxDocument
import structlog
from sqlalchemy.orm import Session

from app.models.document import Document
from app.core.config import settings

logger = structlog.get_logger()

class DocumentProcessor:
    """Service for processing uploaded documents."""
    
    def __init__(self):
        self.max_pages = settings.MAX_DOCUMENT_PAGES
    
    async def process_document_async(self, document_id: str, db: Session):
        """Process document asynchronously."""
        # This would typically be run as a background task with Celery
        # For now, we'll simulate async processing
        await asyncio.sleep(0.1)  # Prevent blocking
        return self.process_document(document_id, db)
    
    def process_document(self, document_id: str, db: Session) -> bool:
        """Process a document and extract text content."""
        try:
            document = db.query(Document).filter(Document.id == document_id).first()
            if not document:
                logger.error("Document not found", document_id=document_id)
                return False
            
            # Update status
            document.status = "processing"
            document.processing_started_at = datetime.now(timezone.utc)
            db.commit()
            
            # Extract text based on file type
            extracted_text = ""
            page_count = 0
            word_count = 0
            
            if document.file_type == ".pdf":
                extracted_text, page_count = self._extract_from_pdf(document.file_path)
            elif document.file_type == ".docx":
                extracted_text, page_count = self._extract_from_docx(document.file_path)
            elif document.file_type == ".txt":
                extracted_text = self._extract_from_txt(document.file_path)
                page_count = 1
            else:
                raise ValueError(f"Unsupported file type: {document.file_type}")
            
            # Count words
            word_count = len(extracted_text.split()) if extracted_text else 0
            
            # Classify document type
            document_type, confidence = self._classify_document(extracted_text)
            
            # Update document with extracted information
            document.extracted_text = extracted_text
            document.page_count = page_count
            document.word_count = word_count
            document.document_type = document_type
            document.confidence_score = confidence
            document.status = "completed"
            document.processing_completed_at = datetime.now(timezone.utc)
            
            db.commit()
            
            logger.info("Document processed successfully", 
                       document_id=document_id,
                       pages=page_count,
                       words=word_count,
                       doc_type=document_type)
            
            return True
            
        except Exception as e:
            logger.error("Document processing failed", 
                        document_id=document_id, 
                        error=str(e))
            
            # Update document with error status
            if 'document' in locals():
                document.status = "failed"
                document.error_message = str(e)
                document.processing_completed_at = datetime.now(timezone.utc)
                db.commit()
            
            return False
    
    def _extract_from_pdf(self, file_path: str) -> tuple[str, int]:
        """Extract text from PDF file."""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                page_count = len(pdf_reader.pages)
                
                # Limit pages to prevent processing very large documents
                pages_to_process = min(page_count, self.max_pages)
                
                text_content = []
                for page_num in range(pages_to_process):
                    page = pdf_reader.pages[page_num]
                    text_content.append(page.extract_text())
                
                extracted_text = "\n".join(text_content)
                return extracted_text, page_count
                
        except Exception as e:
            logger.error("PDF extraction failed", file_path=file_path, error=str(e))
            raise
    
    def _extract_from_docx(self, file_path: str) -> tuple[str, int]:
        """Extract text from DOCX file."""
        try:
            doc = DocxDocument(file_path)
            paragraphs = [paragraph.text for paragraph in doc.paragraphs]
            extracted_text = "\n".join(paragraphs)
            
            # Estimate page count (rough approximation)
            page_count = max(1, len(extracted_text) // 3000)  # ~3000 chars per page
            
            return extracted_text, page_count
            
        except Exception as e:
            logger.error("DOCX extraction failed", file_path=file_path, error=str(e))
            raise
    
    def _extract_from_txt(self, file_path: str) -> str:
        """Extract text from TXT file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            # Try with different encoding
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    return file.read()
            except Exception as e:
                logger.error("TXT extraction failed", file_path=file_path, error=str(e))
                raise
    
    def _classify_document(self, text: str) -> tuple[str, float]:
        """Classify document type based on content."""
        text_lower = text.lower()
        
        # Define keywords for different document types
        classification_rules = {
            "rental_agreement": [
                "lease", "rent", "tenant", "landlord", "premises", "monthly rent",
                "security deposit", "rental agreement", "lease term"
            ],
            "loan_contract": [
                "loan", "borrower", "lender", "principal", "interest rate", "repayment",
                "default", "collateral", "loan agreement", "credit"
            ],
            "employment_contract": [
                "employee", "employer", "salary", "employment", "job", "position",
                "benefits", "termination", "employment agreement", "work"
            ],
            "terms_of_service": [
                "terms of service", "terms and conditions", "user agreement",
                "privacy policy", "acceptable use", "service", "platform"
            ],
            "purchase_agreement": [
                "purchase", "buyer", "seller", "sale", "goods", "merchandise",
                "purchase agreement", "delivery", "payment terms"
            ],
            "service_contract": [
                "service", "contractor", "client", "services", "performance",
                "service agreement", "deliverables", "scope of work"
            ]
        }
        
        scores = {}
        for doc_type, keywords in classification_rules.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            scores[doc_type] = score / len(keywords)  # Normalize by keyword count
        
        # Find the type with highest score
        if scores:
            best_type = max(scores, key=scores.get)
            confidence = scores[best_type]
            
            # Only return classification if confidence is reasonable
            if confidence > 0.2:  # At least 20% of keywords found
                return best_type, confidence
        
        return "general_legal", 0.0