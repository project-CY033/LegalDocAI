from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "postgresql://legaldocai:defaultpassword@localhost:5432/legaldocai"
    
    # Redis settings
    REDIS_URL: str = "redis://localhost:6379"
    
    # Google Cloud settings
    GOOGLE_CLOUD_PROJECT: str = ""
    GOOGLE_APPLICATION_CREDENTIALS: str = ""
    GCS_BUCKET_NAME: str = "legaldocai-documents"
    VERTEX_AI_LOCATION: str = "us-central1"
    VERTEX_AI_MODEL: str = "gemini-pro"
    
    # Firebase settings
    FIREBASE_API_KEY: str = ""
    FIREBASE_AUTH_DOMAIN: str = ""
    FIREBASE_PROJECT_ID: str = ""
    FIREBASE_STORAGE_BUCKET: str = ""
    FIREBASE_MESSAGING_SENDER_ID: str = ""
    FIREBASE_APP_ID: str = ""
    
    # JWT settings
    JWT_SECRET: str = "your-super-secret-jwt-key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS settings
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # File upload settings
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: List[str] = [".pdf", ".docx", ".txt"]
    UPLOAD_DIR: str = "uploads"
    
    # Document processing settings
    MAX_DOCUMENT_PAGES: int = 50
    AI_TIMEOUT_SECONDS: int = 120
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()