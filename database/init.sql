-- Legal Document AI Database Schema
-- PostgreSQL initialization script

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    firebase_uid VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    company VARCHAR(255),
    role VARCHAR(255),
    preferred_language VARCHAR(10) DEFAULT 'en',
    documents_processed INTEGER DEFAULT 0,
    api_calls_count INTEGER DEFAULT 0
);

-- Documents table
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    mime_type VARCHAR(100) NOT NULL,
    extracted_text TEXT,
    page_count INTEGER,
    word_count INTEGER,
    status VARCHAR(50) DEFAULT 'uploaded',
    processing_started_at TIMESTAMP,
    processing_completed_at TIMESTAMP,
    error_message TEXT,
    document_type VARCHAR(100),
    confidence_score DECIMAL(5,4),
    language VARCHAR(10) DEFAULT 'en',
    is_sensitive BOOLEAN DEFAULT TRUE,
    retention_days INTEGER DEFAULT 30,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);

-- Analyses table
CREATE TABLE IF NOT EXISTS analyses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    analysis_type VARCHAR(100) NOT NULL,
    request_data JSONB,
    model_used VARCHAR(100) NOT NULL,
    model_version VARCHAR(50),
    prompt_template TEXT,
    summary TEXT,
    simplified_explanation TEXT,
    key_points JSONB,
    risk_assessment JSONB,
    legal_implications JSONB,
    clauses_analyzed JSONB,
    problematic_clauses JSONB,
    question TEXT,
    answer TEXT,
    confidence_score DECIMAL(5,4),
    source_language VARCHAR(10) DEFAULT 'en',
    target_language VARCHAR(10) DEFAULT 'en',
    processing_time_seconds DECIMAL(8,3),
    token_count_input INTEGER,
    token_count_output INTEGER,
    status VARCHAR(50) DEFAULT 'pending',
    quality_score DECIMAL(5,4),
    human_reviewed BOOLEAN DEFAULT FALSE,
    user_rating INTEGER CHECK (user_rating >= 1 AND user_rating <= 5),
    user_feedback TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- Legal Templates table
CREATE TABLE IF NOT EXISTS legal_templates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    subcategory VARCHAR(100),
    description TEXT NOT NULL,
    common_clauses JSONB NOT NULL,
    risk_factors JSONB NOT NULL,
    key_terms_to_check JSONB NOT NULL,
    red_flags JSONB NOT NULL,
    standard_protections JSONB,
    simplified_language JSONB,
    question_templates JSONB,
    jurisdiction VARCHAR(100) DEFAULT 'US',
    applicable_laws JSONB,
    version VARCHAR(50) DEFAULT '1.0',
    is_active BOOLEAN DEFAULT TRUE,
    usage_count INTEGER DEFAULT 0,
    effectiveness_score DECIMAL(5,4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_used TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_firebase_uid ON users(firebase_uid);
CREATE INDEX IF NOT EXISTS idx_documents_user_id ON documents(user_id);
CREATE INDEX IF NOT EXISTS idx_documents_status ON documents(status);
CREATE INDEX IF NOT EXISTS idx_documents_document_type ON documents(document_type);
CREATE INDEX IF NOT EXISTS idx_analyses_user_id ON analyses(user_id);
CREATE INDEX IF NOT EXISTS idx_analyses_document_id ON analyses(document_id);
CREATE INDEX IF NOT EXISTS idx_analyses_analysis_type ON analyses(analysis_type);
CREATE INDEX IF NOT EXISTS idx_legal_templates_category ON legal_templates(category);
CREATE INDEX IF NOT EXISTS idx_legal_templates_active ON legal_templates(is_active);

-- Update timestamp trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply update timestamp triggers
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_documents_updated_at BEFORE UPDATE ON documents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_analyses_updated_at BEFORE UPDATE ON analyses
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_legal_templates_updated_at BEFORE UPDATE ON legal_templates
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();