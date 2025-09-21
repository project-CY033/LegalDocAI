import time
import json
from typing import Dict, List, Optional, Any
from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel, Part
import structlog

from app.core.config import settings
from app.models.document import Document

logger = structlog.get_logger()

class AIAnalyzer:
    """Service for AI-powered legal document analysis using Google Cloud Vertex AI."""
    
    def __init__(self):
        # Initialize Vertex AI
        aiplatform.init(
            project=settings.GOOGLE_CLOUD_PROJECT,
            location=settings.VERTEX_AI_LOCATION
        )
        
        self.model = GenerativeModel(settings.VERTEX_AI_MODEL)
        self.timeout = settings.AI_TIMEOUT_SECONDS
    
    async def analyze_document(
        self, 
        document: Document, 
        analysis_type: str,
        language: str = "en",
        focus_areas: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Perform comprehensive AI analysis of a legal document."""
        
        start_time = time.time()
        
        try:
            # Get the appropriate prompt based on analysis type
            prompt = self._get_analysis_prompt(
                document_text=document.extracted_text,
                document_type=document.document_type,
                analysis_type=analysis_type,
                language=language,
                focus_areas=focus_areas or []
            )
            
            # Generate response from AI
            response = self.model.generate_content(prompt)
            
            # Parse the AI response
            result = self._parse_analysis_response(response.text, analysis_type)
            
            processing_time = time.time() - start_time
            result["processing_time"] = processing_time
            
            logger.info("AI analysis completed", 
                       document_id=document.id,
                       analysis_type=analysis_type,
                       processing_time=processing_time)
            
            return result
            
        except Exception as e:
            logger.error("AI analysis failed", 
                        document_id=document.id,
                        analysis_type=analysis_type,
                        error=str(e))
            raise
    
    async def answer_question(
        self,
        document: Document,
        question: str,
        language: str = "en"
    ) -> Dict[str, Any]:
        """Answer a specific question about the document."""
        
        start_time = time.time()
        
        try:
            prompt = self._get_qa_prompt(
                document_text=document.extracted_text,
                document_type=document.document_type,
                question=question,
                language=language
            )
            
            response = self.model.generate_content(prompt)
            
            result = {
                "answer": response.text.strip(),
                "confidence_score": self._calculate_confidence(response.text),
                "processing_time": time.time() - start_time
            }
            
            logger.info("Question answered", 
                       document_id=document.id,
                       question_length=len(question))
            
            return result
            
        except Exception as e:
            logger.error("Question answering failed", 
                        document_id=document.id,
                        error=str(e))
            raise
    
    def _get_analysis_prompt(
        self,
        document_text: str,
        document_type: str,
        analysis_type: str,
        language: str,
        focus_areas: List[str]
    ) -> str:
        """Generate analysis prompt based on the analysis type."""
        
        base_context = f"""
You are a legal expert AI assistant specialized in analyzing legal documents and explaining them in simple, accessible language. 
The user has uploaded a {document_type} document and needs help understanding it.

Document Type: {document_type}
Analysis Type: {analysis_type}
Language for Response: {language}
Focus Areas: {', '.join(focus_areas) if focus_areas else 'General analysis'}

Document Content:
{document_text[:8000]}  # Limit text to prevent token overflow

Please analyze this document and provide your response in JSON format with the following structure:
"""
        
        if analysis_type == "full_summary":
            return base_context + """
{
    "summary": "A clear, concise summary of the document in plain language",
    "simplified_explanation": "Detailed explanation breaking down complex legal terms",
    "key_points": [
        "List of the most important points",
        "Each point should be in simple language"
    ],
    "risk_assessment": {
        "high_risk_items": ["List of concerning clauses or terms"],
        "medium_risk_items": ["Moderately concerning items"],
        "protective_clauses": ["Clauses that protect the user"]
    },
    "legal_implications": {
        "rights": ["User's rights under this document"],
        "obligations": ["User's obligations and responsibilities"],
        "consequences": ["Potential consequences of signing"]
    },
    "confidence_score": 0.95
}
"""
        
        elif analysis_type == "risk_assessment":
            return base_context + """
{
    "risk_assessment": {
        "overall_risk_level": "low|medium|high",
        "high_risk_items": [
            {
                "clause": "Exact text of concerning clause",
                "risk_level": "high",
                "explanation": "Why this is risky in simple terms",
                "recommendation": "What the user should do about it"
            }
        ],
        "medium_risk_items": [...],
        "red_flags": ["List of major warning signs"],
        "protective_elements": ["Things that work in user's favor"]
    },
    "recommendations": [
        "Specific actions the user should consider",
        "Questions to ask before signing"
    ],
    "confidence_score": 0.90
}
"""
        
        elif analysis_type == "clause_explanation":
            return base_context + """
{
    "clauses_analyzed": [
        {
            "clause_title": "Name of the clause",
            "original_text": "Original legal language",
            "simplified_explanation": "What this means in plain English",
            "importance_level": "high|medium|low",
            "user_impact": "How this affects the user specifically"
        }
    ],
    "problematic_clauses": [
        {
            "clause": "Concerning clause text",
            "problem": "What makes this problematic",
            "alternative_language": "Better language to suggest"
        }
    ],
    "confidence_score": 0.88
}
"""
        
        else:  # general analysis
            return base_context + """
{
    "summary": "Brief overview of the document",
    "key_takeaways": ["Most important things to know"],
    "questions_to_ask": ["Important questions before proceeding"],
    "confidence_score": 0.85
}
"""
    
    def _get_qa_prompt(
        self,
        document_text: str,
        document_type: str,
        question: str,
        language: str
    ) -> str:
        """Generate Q&A prompt."""
        
        return f"""
You are a legal expert helping someone understand their {document_type}. 

Document Content:
{document_text[:8000]}

User Question: {question}

Please provide a clear, accurate answer in {language}. Be specific and refer to relevant parts of the document. 
If the question cannot be answered from the document content, say so clearly.

Format your response as a direct answer to the question, avoiding legal jargon and explaining concepts in simple terms.
If there are important caveats or recommendations, include them.
"""
    
    def _parse_analysis_response(self, response_text: str, analysis_type: str) -> Dict[str, Any]:
        """Parse AI response and extract structured data."""
        
        try:
            # Try to extract JSON from the response
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                json_text = response_text[json_start:json_end].strip()
            elif "{" in response_text and "}" in response_text:
                json_start = response_text.find("{")
                json_end = response_text.rfind("}") + 1
                json_text = response_text[json_start:json_end]
            else:
                # Fallback: create basic structure
                return {
                    "summary": response_text,
                    "confidence_score": 0.7
                }
            
            parsed_result = json.loads(json_text)
            
            # Ensure required fields exist
            if "confidence_score" not in parsed_result:
                parsed_result["confidence_score"] = self._calculate_confidence(response_text)
            
            return parsed_result
            
        except json.JSONDecodeError as e:
            logger.warning("Failed to parse JSON response", error=str(e))
            # Return a basic structure
            return {
                "summary": response_text,
                "simplified_explanation": "Please review the raw analysis above.",
                "confidence_score": 0.6
            }
    
    def _calculate_confidence(self, response_text: str) -> float:
        """Calculate confidence score based on response characteristics."""
        
        # Simple heuristic based on response length and content
        text_length = len(response_text)
        
        if text_length < 100:
            return 0.3  # Very short responses are likely incomplete
        elif text_length < 500:
            return 0.6  # Short but might be adequate
        elif text_length < 2000:
            return 0.8  # Good length
        else:
            return 0.9  # Comprehensive response
    
    def get_legal_templates(self, document_type: str) -> Dict[str, Any]:
        """Get legal analysis templates for specific document types."""
        
        templates = {
            "rental_agreement": {
                "key_clauses": [
                    "rent_amount", "lease_term", "security_deposit", "maintenance_responsibilities",
                    "pet_policy", "subletting_rules", "termination_conditions"
                ],
                "red_flags": [
                    "excessive_fees", "unreasonable_restrictions", "unclear_termination",
                    "maintenance_burden_on_tenant", "automatic_renewal_clauses"
                ],
                "protective_elements": [
                    "reasonable_notice_periods", "deposit_return_procedures",
                    "habitability_guarantees", "privacy_protections"
                ]
            },
            "loan_contract": {
                "key_clauses": [
                    "principal_amount", "interest_rate", "repayment_schedule", "default_conditions",
                    "collateral_requirements", "prepayment_penalties"
                ],
                "red_flags": [
                    "variable_interest_rates", "balloon_payments", "cross_default_clauses",
                    "excessive_fees", "personal_guarantees"
                ],
                "protective_elements": [
                    "fixed_interest_rates", "clear_payment_schedule", "grace_periods",
                    "reasonable_default_cure_periods"
                ]
            }
        }
        
        return templates.get(document_type, {})