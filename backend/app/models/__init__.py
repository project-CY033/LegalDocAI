# Import all models to ensure they're registered with SQLAlchemy
from app.core.database import Base
from .user import User
from .document import Document
from .analysis import Analysis
from .legal_template import LegalTemplate

__all__ = ["Base", "User", "Document", "Analysis", "LegalTemplate"]