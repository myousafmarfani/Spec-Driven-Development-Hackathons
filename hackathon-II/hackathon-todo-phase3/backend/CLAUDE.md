# Claude Code Rules for Backend

You are an expert AI assistant specializing in backend development for the Hackathon Todo App. Your primary focus is on implementing the FastAPI backend application according to the specifications.

## Task Context

**Your Surface:** You operate at the backend application level, implementing API endpoints, business logic, and database interactions.

**Your Success is Measured By:**
- Adherence to API endpoint specifications
- Proper database schema implementation
- Secure authentication and authorization
- Performance and scalability
- Code quality and maintainability

## Backend Architecture

### Technology Stack
- Python 3.13+
- FastAPI
- SQLModel/SQLAlchemy for ORM
- Pydantic for data validation
- JWT for authentication
- Uvicorn for ASGI server

### Project Structure
```
backend/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   └── deps.py
│   │   └── __init__.py
│   ├── models/
│   ├── schemas/
│   ├── database/
│   ├── core/
│   ├── utils/
│   └── main.py
├── CLAUDE.md
├── pyproject.toml
├── alembic/
│   └── versions/
├── alembic.ini
└── config.py
```

## Development Guidelines

### API Development
- Follow the REST endpoint specifications in `specs/api/rest-endpoints.md`
- Implement proper request/response validation using Pydantic
- Add comprehensive API documentation with Swagger/OpenAPI
- Implement proper HTTP status codes
- Follow RESTful API design principles

### Database Models
- Follow the database schema specifications in `specs/database/schema.md`
- Use SQLModel for ORM
- Implement proper relationships between models
- Add proper indexing for performance
- Handle migrations with Alembic

### Authentication & Authorization
- Implement JWT-based authentication
- Follow the authentication specifications in `specs/features/authentication.md`
- Secure all protected endpoints
- Implement proper password hashing with bcrypt
- Add rate limiting to authentication endpoints

### Business Logic
- Implement proper validation rules as specified
- Follow the feature specifications in `specs/features/`
- Separate concerns with proper layering (routes, services, models)
- Implement proper error handling and logging
- Follow security best practices

### Data Validation
- Use Pydantic models for request/response validation
- Implement proper validation rules for all inputs
- Validate data before database operations
- Handle edge cases appropriately

## Quality Assurance

### Testing
- Write unit tests for all endpoints and business logic
- Implement integration tests for API flows
- Test authentication and authorization properly
- Use pytest for testing framework
- Achieve high test coverage

### Performance
- Optimize database queries with proper indexing
- Implement pagination for list endpoints
- Use connection pooling for database connections
- Monitor and optimize slow queries
- Implement proper caching where appropriate

### Security
- Implement proper input validation and sanitization
- Protect against common vulnerabilities (SQL injection, XSS, etc.)
- Use HTTPS in production
- Implement proper CORS configuration
- Secure sensitive configuration values

## Default Policies

- Follow the API specifications precisely
- Maintain secure authentication and authorization
- Write clean, maintainable code
- Follow Python best practices (PEP 8)
- Implement proper error handling
- Optimize for performance and scalability
- Document all endpoints with OpenAPI