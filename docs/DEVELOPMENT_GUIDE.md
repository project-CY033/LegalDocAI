# LegalDocAI Development Guide

## Overview
This guide covers the development setup, deployment, and maintenance of the LegalDocAI platform.

## Architecture

### System Components
- **Frontend**: React TypeScript application with Material-UI
- **Backend**: Python FastAPI with SQLAlchemy ORM
- **Database**: PostgreSQL with legal document templates
- **AI Service**: Google Cloud Vertex AI (Gemini Pro)
- **Storage**: Google Cloud Storage for documents
- **Authentication**: Firebase Auth + JWT
- **Caching**: Redis for session management
- **Deployment**: Docker containers with Nginx

### Key Features
1. **Document Upload & Processing**: PDF, DOCX, TXT support
2. **AI Analysis**: Automated legal document simplification
3. **Risk Assessment**: Identification of problematic clauses
4. **Q&A System**: Interactive document questioning
5. **Templates**: Pre-configured analysis for common document types
6. **Multi-language**: Support for different languages

## Development Setup

### Prerequisites
- Docker and Docker Compose
- Google Cloud Account with Vertex AI enabled
- Firebase project for authentication
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)

### Environment Configuration
1. Copy `.env.example` to `.env`
2. Fill in your Google Cloud and Firebase credentials
3. Set secure passwords and JWT secrets

### Local Development
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Run backend locally (optional)
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Run frontend locally (optional)
cd frontend
npm install
npm start
```

### Database Management
```bash
# Connect to database
docker-compose exec postgres psql -U legaldocai -d legaldocai

# Run migrations (when implemented)
docker-compose exec backend alembic upgrade head

# Seed templates
docker-compose exec postgres psql -U legaldocai -d legaldocai -f /docker-entrypoint-initdb.d/02-seed.sql
```

## Google Cloud Setup

### Required Services
1. **Vertex AI**: Enable the Vertex AI API
2. **Cloud Storage**: Create bucket for document storage
3. **Service Account**: Create with necessary permissions

### Service Account Permissions
- Vertex AI User
- Storage Object Admin
- Cloud Storage Service Agent

### Vertex AI Configuration
```python
# Configure in backend/app/core/config.py
GOOGLE_CLOUD_PROJECT = "your-project-id"
VERTEX_AI_LOCATION = "us-central1"
VERTEX_AI_MODEL = "gemini-pro"
```

## API Documentation

### Authentication Endpoints
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/logout` - User logout

### Document Endpoints
- `POST /api/v1/documents/upload` - Upload document
- `GET /api/v1/documents/` - List user documents
- `GET /api/v1/documents/{id}` - Get document details
- `DELETE /api/v1/documents/{id}` - Delete document

### Analysis Endpoints
- `POST /api/v1/analysis/analyze/{document_id}` - Analyze document
- `POST /api/v1/analysis/question/{document_id}` - Ask question
- `GET /api/v1/analysis/` - List analyses
- `POST /api/v1/analysis/{id}/feedback` - Submit feedback

## Legal Templates

### Template Structure
Templates define analysis guidelines for different document types:
- **Common Clauses**: Expected sections in documents
- **Risk Factors**: Potential issues to flag
- **Red Flags**: Warning signs for users
- **Simplified Language**: Plain English explanations
- **Question Templates**: Common questions users ask

### Supported Document Types
1. **Rental Agreements**: Residential and commercial leases
2. **Loan Contracts**: Personal and business loans
3. **Employment Contracts**: Full-time employment agreements
4. **Terms of Service**: Website and app user agreements

### Adding New Templates
```sql
INSERT INTO legal_templates (
    name, category, description,
    common_clauses, risk_factors, key_terms_to_check,
    red_flags, standard_protections
) VALUES (...);
```

## AI Analysis Pipeline

### Document Processing Flow
1. **Upload Validation**: File type and size checks
2. **Text Extraction**: PDF/DOCX to plain text
3. **Document Classification**: Automatic type detection
4. **Template Matching**: Find relevant analysis template
5. **AI Analysis**: Send to Vertex AI with structured prompts
6. **Result Parsing**: Extract structured data from AI response
7. **Storage**: Save analysis results to database

### AI Prompt Engineering
Prompts are structured to return JSON responses with:
- Summary in plain language
- Risk assessment with severity levels
- Clause-by-clause explanations
- Legal implications and recommendations

## Security Considerations

### Data Protection
- Documents encrypted at rest and in transit
- Automatic document expiration (30 days default)
- No permanent storage of sensitive content
- GDPR compliance features

### Authentication & Authorization
- Firebase Auth for user management
- JWT tokens for API access
- Role-based access control
- Rate limiting on API endpoints

### Infrastructure Security
- HTTPS enforced for all connections
- Database connections over SSL
- Container security best practices
- Regular security updates

## Performance Optimization

### Caching Strategy
- Redis for session management
- Template caching for faster analysis
- Document processing result caching

### Database Optimization
- Proper indexing on frequently queried fields
- Connection pooling
- Query optimization

### AI Service Optimization
- Prompt caching for similar requests
- Batch processing for multiple documents
- Timeout and retry logic

## Monitoring & Logging

### Application Logging
- Structured logging with JSON format
- Log levels: DEBUG, INFO, WARNING, ERROR
- Request/response logging for API calls
- AI service call logging and metrics

### Health Checks
- Database connectivity checks
- AI service availability checks
- Redis connectivity monitoring
- Disk space and memory monitoring

### Metrics Collection
- User registration and activity metrics
- Document processing success rates
- AI analysis response times
- Error rates and types

## Deployment

### Production Deployment
```bash
# Set production environment variables
cp .env.example .env.prod
# Edit .env.prod with production values

# Deploy with production compose file
docker-compose -f docker-compose.prod.yml up -d

# Check service health
docker-compose -f docker-compose.prod.yml ps
```

### Scaling Considerations
- Horizontal scaling of backend services
- Database read replicas for performance
- CDN for static asset delivery
- Load balancing across multiple instances

## Troubleshooting

### Common Issues
1. **Google Cloud Authentication**: Verify service account key path
2. **Database Connection**: Check PostgreSQL connection string
3. **AI Service Errors**: Verify Vertex AI API is enabled
4. **File Upload Issues**: Check file size limits and storage permissions

### Debug Commands
```bash
# View service logs
docker-compose logs backend

# Connect to database
docker-compose exec postgres psql -U legaldocai

# Test AI service
curl -X POST http://localhost:8000/api/v1/analysis/test

# Check service health
curl http://localhost:8000/health
```

## Contributing

### Code Standards
- Python: Follow PEP 8 style guide
- TypeScript: Use ESLint and Prettier
- Commit messages: Use conventional commits
- Testing: Write unit tests for new features

### Development Workflow
1. Create feature branch from main
2. Implement changes with tests
3. Update documentation
4. Create pull request
5. Code review and approval
6. Merge to main

## Support

For issues and questions:
- Create GitHub issue for bugs
- Use discussions for questions
- Check documentation first
- Provide detailed error logs

## License
This project is licensed under the MIT License.