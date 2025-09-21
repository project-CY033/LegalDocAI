from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import structlog
from app.models.legal_template import LegalTemplate
from app.core.database import get_db

logger = structlog.get_logger()

class TemplateService:
    """Service for managing legal document templates."""
    
    def __init__(self):
        pass
    
    def get_template_by_category(self, db: Session, category: str) -> Optional[LegalTemplate]:
        """Get the most relevant template for a document category."""
        template = db.query(LegalTemplate).filter(
            LegalTemplate.category == category,
            LegalTemplate.is_active == True
        ).first()
        
        if template:
            # Update usage count
            template.usage_count += 1
            template.last_used = datetime.now(timezone.utc)
            db.commit()
            
        return template
    
    def get_analysis_guidelines(self, db: Session, document_type: str) -> Dict[str, Any]:
        """Get analysis guidelines for a specific document type."""
        template = self.get_template_by_category(db, document_type)
        
        if not template:
            logger.warning("No template found for document type", document_type=document_type)
            return self._get_default_guidelines()
        
        return {
            "common_clauses": template.common_clauses,
            "risk_factors": template.risk_factors,
            "key_terms": template.key_terms_to_check,
            "red_flags": template.red_flags,
            "standard_protections": template.standard_protections,
            "question_templates": template.question_templates,
            "simplified_language": template.simplified_language
        }
    
    def get_question_templates(self, db: Session, document_type: str) -> List[str]:
        """Get pre-defined questions for a document type."""
        template = self.get_template_by_category(db, document_type)
        
        if template and template.question_templates:
            return template.question_templates
        
        return [
            "What are the main terms of this agreement?",
            "What are my rights under this document?",
            "What are my obligations?",
            "What are the potential risks?",
            "What happens if I want to terminate this agreement?"
        ]
    
    def get_simplified_explanations(self, db: Session, document_type: str) -> Dict[str, str]:
        """Get simplified explanations for common legal terms."""
        template = self.get_template_by_category(db, document_type)
        
        if template and template.simplified_language:
            return template.simplified_language
        
        return self._get_default_explanations()
    
    def create_template(self, db: Session, template_data: Dict[str, Any]) -> LegalTemplate:
        """Create a new legal template."""
        template = LegalTemplate(**template_data)
        db.add(template)
        db.commit()
        db.refresh(template)
        
        logger.info("Legal template created", template_id=template.id, category=template.category)
        return template
    
    def update_template_effectiveness(self, db: Session, template_id: str, rating: float):
        """Update template effectiveness based on user feedback."""
        template = db.query(LegalTemplate).filter(LegalTemplate.id == template_id).first()
        if template:
            # Simple moving average of effectiveness
            if template.effectiveness_score:
                template.effectiveness_score = (template.effectiveness_score + rating) / 2
            else:
                template.effectiveness_score = rating
            
            db.commit()
            logger.info("Template effectiveness updated", 
                       template_id=template_id, 
                       new_score=template.effectiveness_score)
    
    def _get_default_guidelines(self) -> Dict[str, Any]:
        """Default analysis guidelines when no template is found."""
        return {
            "common_clauses": [
                "parties_involved",
                "main_obligations",
                "payment_terms",
                "termination_conditions",
                "dispute_resolution"
            ],
            "risk_factors": [
                {
                    "risk": "unclear_terms",
                    "description": "Ambiguous or unclear language",
                    "severity": "medium"
                },
                {
                    "risk": "one_sided_terms",
                    "description": "Terms heavily favoring one party",
                    "severity": "high"
                }
            ],
            "key_terms": [
                "effective_date",
                "duration",
                "payment_amounts",
                "termination_clause",
                "liability_limits"
            ],
            "red_flags": [
                "No termination clause",
                "Unlimited liability",
                "Unclear payment terms",
                "No dispute resolution process"
            ]
        }
    
    def _get_default_explanations(self) -> Dict[str, str]:
        """Default simplified explanations for legal terms."""
        return {
            "consideration": "Something of value exchanged in a contract (money, services, goods)",
            "liability": "Legal responsibility for damages or losses",
            "indemnification": "One party agrees to cover losses of another party",
            "force_majeure": "Unforeseeable circumstances that prevent contract performance",
            "jurisdiction": "Which court system has authority over disputes",
            "severability": "If one part of contract is invalid, the rest remains valid"
        }