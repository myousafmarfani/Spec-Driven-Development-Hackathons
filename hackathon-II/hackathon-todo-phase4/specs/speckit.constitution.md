<!-- SYNC IMPACT REPORT
Version change: 1.0.0 → 1.1.0
Added sections: Principle 3 - Statelessness Guarantee
Modified principles: Principle 3-8 renumbered to 4-9
Removed sections: N/A
Templates requiring updates:
  - .specify/templates/plan-template.md
  - .specify/templates/spec-template.md
  - .specify/templates/tasks-template.md
  - .specify/templates/commands/sp.constitution.md
Runtime docs requiring updates:
  - README.md
Follow-up TODOs:
  - Communicate statelessness requirement to all developers
-->

# Project Constitution

**Document Version:** 1.1.0
**Ratification Date:** 2026-02-08
**Last Amended:** 2026-02-11
**Status:** Active

## Governance

This constitution establishes the binding principles and practices that govern all development activities for the project. All contributors agree to abide by these principles, which serve as the authoritative source for technical and process decisions.

### Amendment Procedure
Changes to this constitution require:
1. Public proposal with rationale
2. Discussion period of minimum 48 hours
3. Approval by project lead
4. Documentation of version change impact

### Versioning Policy
- MAJOR: Breaking changes to established practices
- MINOR: Addition of new principles or expansion of scope
- PATCH: Clarifications, corrections, or non-substantive changes

### Compliance Review
Quarterly reviews ensure ongoing adherence to constitutional principles and identify areas needing updates.

## Principle 1: Architecture Values

**Statement:** Applications must follow monorepo organization with clear separation of concerns between frontend and backend components, utilizing RESTful API design principles, stateless backend services, and JWT-based authentication.

**Rules:**
- All frontend and backend code must be organized in a single repository with clear service boundaries
- Frontend and backend must communicate solely through well-defined RESTful API endpoints
- Backend services must be stateless and horizontally scalable
- Authentication must be implemented using JWT tokens
- Clear separation of concerns between presentation, business logic, and data layers

**Rationale:** This ensures maintainable, scalable, and secure applications with clear service boundaries that facilitate team collaboration and system evolution.

## Principle 2: Technology Stack (Non-Negotiable)

**Statement:** Projects must utilize the specified technology stack with no deviations allowed for core components.

**Rules:**
- **Frontend:** Next.js 16+ with App Router, TypeScript (strict mode), Tailwind CSS, Better Auth
- **Backend:** Python 3.13+, FastAPI, SQLModel ORM, Pydantic, JWT token verification
- **Database:** Neon Serverless PostgreSQL with schema migration tracking
- **Development:** UV for Python package management, npm/pnpm for Node.js packages
- All versions specified must be adhered to without deviation
- Dependency updates must follow semver and maintain compatibility

**Rationale:** Standardized technology stack ensures consistent development experience, reduces onboarding time, enables knowledge sharing, and maintains compatibility across team members.

## Principle 3: Statelessness Guarantee

**Statement:** Backend services must operate without in-memory state, ensuring complete recovery from any failure and enabling unlimited horizontal scalability.

**Rules:**
- Servers must hold ZERO conversation/application state in memory
- ALL state must persist in the database before responding to requests
- Each request must be completely independent and self-contained
- Conversation history and user context must be fetched from database on EVERY request
- Server must be able to restart mid-conversation without data loss
- Multiple server instances must be able to handle requests for any user without coordination
- No session-based state storage (memory, files, or distributed caches)
- Cache invalidation complexity must be avoided entirely

**Forbidden Practices:**
- In-memory conversation caching or session storage
- Redis/Memcached for storing user conversations or task state
- Global variables storing user-specific data
- Process-local state that doesn't survive restarts
- Any optimization that sacrifices statelessness

**Rationale:** Statelessness guarantees reliability, simplifies scaling, eliminates single points of failure, and reduces operational complexity. It is a foundational requirement for cloud-native applications and enables DevOps practices like rolling deployments and auto-scaling.

## Principle 4: Code Quality Standards

**Statement:** All code must meet stringent quality standards including type safety, proper error handling, and security considerations.

**Rules:**
- Python code must include type hints for all function signatures
- TypeScript frontend code must use strict mode compilation
- Async/await patterns must be preferred over callbacks
- All endpoints must include comprehensive error handling
- Input validation required on all API entry points
- ORM must be used exclusively to prevent SQL injection
- Code must pass all linting and formatting checks before merging
- Unit tests must cover at least 80% of business logic

**Rationale:** High code quality standards ensure maintainability, security, and reduce long-term maintenance costs while improving developer productivity.

## Principle 5: Security Requirements

**Statement:** Applications must implement comprehensive security measures to protect user data and system integrity.

**Rules:**
- All API endpoints must require JWT authentication except explicitly public routes
- Users can only access their own data through proper authorization checks
- Passwords must never be stored in plain text (handled by Better Auth)
- Secrets must be managed through environment variables or secure vault
- CORS must be configured to allow only authorized frontend origins
- Production deployments must use HTTPS encryption
- Security headers must be properly configured
- Regular security audits must be conducted

**Rationale:** Robust security measures protect user privacy, prevent data breaches, and maintain trust in the application.

## Principle 6: API Design Principles

**Statement:** APIs must follow consistent RESTful design patterns with standardized request/response formats.

**Rules:**
- APIs must follow RESTful conventions and HTTP method semantics
- All requests/responses must use JSON format
- Proper HTTP status codes must be returned for all responses
- User-specific data must include user ID in URL path for isolation
- Error responses must follow consistent format across all endpoints
- API versioning must be implemented using path prefixes
- Rate limiting must be applied to prevent abuse
- API documentation must be maintained and kept current

**Rationale:** Consistent API design improves usability, simplifies client development, and ensures predictable behavior across the application ecosystem.

## Principle 7: Database Principles

**Statement:** Database design and operations must follow best practices for data integrity, performance, and maintainability.

**Rules:**
- Proper foreign key relationships must be defined and enforced
- Frequently queried fields must have appropriate indexes
- All records must include timestamps (created_at, updated_at)
- Soft deletes must be considered for audit trail requirements
- Schema changes must be tracked through migration files
- Database queries must be optimized to prevent performance issues
- Backup strategies must be implemented and tested
- Data validation must occur at both application and database levels

**Rationale:** Well-designed databases ensure data integrity, optimal performance, and support for business requirements while enabling safe evolution of the data model.

## Principle 8: Performance Expectations

**Statement:** Applications must meet specific performance benchmarks to ensure responsive user experience.

**Rules:**
- API response times must be under 200ms for standard CRUD operations
- Database connection pooling must be implemented
- Server-side rendering must be utilized where beneficial for performance
- Heavy components must implement lazy loading strategies
- Resource bundling and optimization must be configured
- Performance monitoring must be implemented and maintained
- Load testing must be performed before production releases
- Performance regression tests must be included in CI pipeline

**Rationale:** Meeting performance expectations ensures positive user experience and system scalability under varying load conditions.

## Principle 9: Development Workflow

**Statement:** Development activities must follow standardized workflows that ensure code quality and maintainability.

**Rules:**
- All code changes must go through pull request review process
- Automated tests must pass before merging
- Code reviews must be conducted by at least one other team member
- Branch naming conventions must be followed (feature/, bugfix/, etc.)
- Commit messages must follow conventional commit format
- Continuous integration must validate all changes
- Documentation must be updated for new features or breaking changes
- Dependent artifacts must be updated when constitution changes

**Rationale:** Standardized development workflows ensure consistent quality, knowledge sharing, and maintainable codebase evolution.