# LegalDocAI - Legal Document Demystification Platform

## Overview
LegalDocAI is an intelligent platform that uses Google Cloud's generative AI to simplify complex legal documents into clear, accessible guidance. The platform empowers users to make informed decisions by providing plain-language explanations of legal jargon, contract terms, and potential risks.

## 🚀 Vercel Deployment

For production deployment on Vercel, see our comprehensive guide:

**👉 [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)**

## 🌐 Netlify Deployment

For deployment on Netlify with serverless functions, see our detailed guide:

**👉 [NETLIFY_DEPLOYMENT.md](NETLIFY_DEPLOYMENT.md)**

Both guides include:
- Step-by-step deployment instructions
- Environment variable configuration
- Database setup (Supabase/PlanetScale/MongoDB)
- Google Cloud integration
- Troubleshooting tips

## Key Features
- **Document Upload & Analysis**: Support for PDF, DOCX, and text files
- **AI-Powered Simplification**: Uses Google Cloud Vertex AI to break down complex legal language
- **Risk Assessment**: Identifies potentially unfavorable terms and clauses
- **Interactive Q&A**: Ask specific questions about your documents
- **Document History**: Keep track of analyzed documents and explanations
- **Templates Library**: Pre-analyzed common document types
- **Multi-language Support**: Translate explanations to various languages

## Technology Stack
- **Backend**: Python (FastAPI)
- **Frontend**: React with TypeScript
- **AI/ML**: Google Cloud Vertex AI (Gemini Pro)
- **Database**: PostgreSQL
- **File Storage**: Google Cloud Storage
- **Authentication**: Firebase Auth
- **Deployment**: Docker, Google Cloud Run

## Project Structure
```
Gen Ai/
├── backend/                 # Python FastAPI backend
├── frontend/               # React TypeScript frontend
├── database/              # Database schemas and migrations
├── docs/                  # Documentation
├── deployment/            # Docker and deployment configs
└── tests/                # Test suites
```

## Getting Started
1. Clone the repository
2. Set up Google Cloud credentials
3. Install dependencies for both backend and frontend
4. Run the development servers
5. Upload a legal document to see the magic happen!

## Use Cases
- **Rental Agreements**: Understand lease terms, tenant rights, and obligations
- **Loan Contracts**: Identify interest rates, penalties, and repayment terms
- **Terms of Service**: Decode privacy policies and user agreements
- **Employment Contracts**: Clarify compensation, benefits, and termination clauses
- **Business Contracts**: Analyze partnerships, vendor agreements, and service contracts

## Security & Privacy
- End-to-end encryption for document transmission
- No permanent storage of sensitive document content
- GDPR and privacy law compliant
- Secure authentication and authorization

## Contributing
We welcome contributions! Please read our contributing guidelines and code of conduct.

## License
This project is licensed under the MIT License - see the LICENSE file for details.