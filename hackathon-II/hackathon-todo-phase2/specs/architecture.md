# Architecture Specification

## System Architecture
The application follows a microservices architecture with clear separation of concerns.

## Components
- **Frontend Service**: Next.js 16 application serving the user interface
- **Backend Service**: FastAPI REST API handling business logic
- **Database Service**: PostgreSQL for data persistence
- **Authentication Service**: JWT-based authentication

## Technology Stack
- Frontend: Next.js 16, React, TypeScript
- Backend: Python 3.9+, FastAPI, SQLAlchemy
- Database: PostgreSQL
- Containerization: Docker, Docker Compose
- Deployment: Vercel/Netlify for frontend, Heroku/Docker for backend

## Communication Patterns
- Frontend communicates with backend via REST API
- Backend communicates with database via ORM
- All services containerized for consistent deployment

## Security Considerations
- JWT authentication for API protection
- Input validation and sanitization
- Secure session management