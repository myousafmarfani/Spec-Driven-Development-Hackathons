# Implementation Plan: AI Chatbot for Todo Management

**Branch**: `002-chatbot-todo` | **Date**: 2026-02-12 | **Spec**: [specs/002-chatbot-todo/spec.md](../spec.md)
**Input**: Feature specification from `/specs/002-chatbot-todo/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement an AI-powered chatbot for todo management that provides natural language interface for task operations. The system will extend Phase 2 functionality with conversation persistence, OpenAI Agents SDK integration, and MCP (Model Context Protocol) tools for stateless task operations. The chatbot will understand at least 8 natural language patterns for add, list, complete, delete, update, and query operations while maintaining conversation history in Neon PostgreSQL database.

## Technical Context

**Language/Version**: Python 3.13+ (FastAPI backend), TypeScript/JavaScript (Next.js frontend)
**Primary Dependencies**: FastAPI, SQLModel, Pydantic, OpenAI Agents SDK, Official MCP SDK, Better Auth, Neon PostgreSQL
**Storage**: Neon Serverless PostgreSQL with schema migration tracking
**Testing**: pytest for backend, Jest for frontend, contract tests for API endpoints
**Target Platform**: Web application (Linux server deployment)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: API response times under 200ms, database operations under 100ms, AI processing under 5 seconds
**Constraints**: Stateless architecture, no in-memory state, JWT authentication, conversation persistence, 95% intent accuracy
**Scale/Scope**: Single user per session, conversation history persistence, 8+ natural language patterns, 50 message history display

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Architecture Values (Principle 1)
- ✅ **PASS**: Web application with frontend/backend separation using RESTful APIs
- ✅ **PASS**: Stateless backend services with JWT authentication
- ✅ **PASS**: Clear separation of concerns between presentation, business logic, and data layers

### Technology Stack (Principle 2)
- ✅ **PASS**: Uses specified stack - Python 3.13+, FastAPI, SQLModel, Pydantic, JWT, Next.js, TypeScript, Tailwind CSS
- ✅ **PASS**: Neon PostgreSQL for database, UV for Python package management

### Statelessness Guarantee (Principle 3)
- ✅ **PASS**: Backend services must operate without in-memory state
- ✅ **PASS**: All state persists in database before responding to requests
- ✅ **PASS**: Each request completely independent and self-contained
- ✅ **PASS**: No server-side session state or in-memory caching

### Code Quality Standards (Principle 4)
- ✅ **PASS**: Python code includes type hints, TypeScript uses strict mode
- ✅ **PASS**: Async/await patterns preferred, comprehensive error handling required
- ✅ **PASS**: Input validation on all API entry points, ORM usage for security

### Security Requirements (Principle 5)
- ✅ **PASS**: All API endpoints require JWT authentication
- ✅ **PASS**: Users only access their own data through authorization checks
- ✅ **PASS**: Passwords never stored in plain text, secrets managed through environment variables

### API Design Principles (Principle 6)
- ✅ **PASS**: RESTful conventions with JSON format, proper HTTP status codes
- ✅ **PASS**: User-specific data includes user ID in URL path for isolation
- ✅ **PASS**: Error responses follow consistent format, API versioning implemented

### Database Principles (Principle 7)
- ✅ **PASS**: Foreign key relationships enforced, frequently queried fields indexed
- ✅ **PASS**: All records include timestamps, schema changes tracked through migrations
- ✅ **PASS**: Database queries optimized, backup strategies implemented

### Performance Expectations (Principle 8)
- ✅ **PASS**: API response times under 200ms for CRUD operations
- ✅ **PASS**: Database connection pooling implemented, server-side rendering utilized
- ✅ **PASS**: Performance monitoring and regression tests included

### Development Workflow (Principle 9)
- ✅ **PASS**: Pull request review process, automated tests, code reviews required
- ✅ **PASS**: Branch naming conventions followed, commit messages conventional format
- ✅ **PASS**: Continuous integration validates all changes

### AI & MCP Architecture (Principle 10)
- ✅ **PASS**: MCP tools stateless and database-backed, conversation state persists to Neon DB
- ✅ **PASS**: Agent responses confirm actions explicitly, MCP tools validate user_id
- ✅ **PASS**: Chat endpoint stateless, no server-side conversation caching

### OpenAI Integration (Principle 11)
- ✅ **PASS**: Official OpenAI Agents SDK and MCP SDK usage, domain allowlist configuration
- ✅ **PASS**: JWT tokens from Better Auth required, API keys through environment variables
- ✅ **PASS**: AI-generated content logged with user context, rate limiting applied

### Error Handling & Resilience (Principle 12)
- ✅ **PASS**: MCP tools handle task not found errors gracefully, friendly user messages
- ✅ **PASS**: Failed tool calls logged but don't crash conversation, timeouts configured
- ✅ **PASS**: Retry logic for transient failures, user informed without technical details

## Project Structure

### Documentation (this feature)

```text
specs/002-chatbot-todo/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Web application structure (frontend + backend)
backend/
├── src/
│   ├── models/           # SQLModel database models (Task, Conversation, Message)
│   ├── services/         # Business logic services (task operations, chat logic)
│   ├── api/              # FastAPI endpoints (including /api/{user_id}/chat)
│   └── mcp/              # MCP server implementation with 5 task operation tools
├── tests/                # Backend test suite
└── migrations/           # Database migration scripts (Alembic or similar)

frontend/
├── src/
│   ├── components/       # React components (UI elements)
│   ├── pages/            # Next.js pages (/chat page with ChatKit)
│   ├── services/         # API client services (chat client, auth)
│   └── chat/             # ChatKit integration and chat UI components
└── public/               # Static assets
```

**Structure Decision**: Web application structure selected based on detected "frontend" + "backend" requirements. This provides clear separation between client-side React/Next.js components and server-side FastAPI services with proper API boundaries. All existing Phase 2 code resides under backend/ and frontend/ directories.

# Implementation Plan: AI Chatbot for Todo Management

**Branch**: `002-chatbot-todo` | **Date**: 2026-02-12 | **Spec**: [specs/002-chatbot-todo/spec.md](../spec.md)
**Input**: Feature specification from `/specs/002-chatbot-todo/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement an AI-powered chatbot for todo management that provides natural language interface for task operations. The system will extend Phase 2 functionality with conversation persistence, OpenAI Agents SDK integration, and MCP (Model Context Protocol) tools for stateless task operations. The chatbot will understand at least 8 natural language patterns for add, list, complete, delete, update, and query operations while maintaining conversation history in Neon PostgreSQL database.

## Technical Context

**Language/Version**: Python 3.13+ (FastAPI backend), TypeScript/JavaScript (Next.js frontend)
**Primary Dependencies**: FastAPI, SQLModel, Pydantic, OpenAI Agents SDK, Official MCP SDK, Better Auth, Neon PostgreSQL
**Storage**: Neon Serverless PostgreSQL with schema migration tracking
**Testing**: pytest for backend, Jest for frontend, contract tests for API endpoints
**Target Platform**: Web application (Linux server deployment)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: API response times under 200ms, database operations under 100ms, AI processing under 5 seconds
**Constraints**: Stateless architecture, no in-memory state, JWT authentication, conversation persistence, 95% intent accuracy
**Scale/Scope**: Single user per session, conversation history persistence, 8+ natural language patterns, 50 message history display

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Architecture Values (Principle 1)
- ✅ **PASS**: Web application with frontend/backend separation using RESTful APIs
- ✅ **PASS**: Stateless backend services with JWT authentication
- ✅ **PASS**: Clear separation of concerns between presentation, business logic, and data layers

### Technology Stack (Principle 2)
- ✅ **PASS**: Uses specified stack - Python 3.13+, FastAPI, SQLModel, Pydantic, JWT, Next.js, TypeScript, Tailwind CSS
- ✅ **PASS**: Neon PostgreSQL for database, UV for Python package management

### Statelessness Guarantee (Principle 3)
- ✅ **PASS**: Backend services must operate without in-memory state
- ✅ **PASS**: All state persists in database before responding to requests
- ✅ **PASS**: Each request completely independent and self-contained
- ✅ **PASS**: No server-side session state or in-memory caching

### Code Quality Standards (Principle 4)
- ✅ **PASS**: Python code includes type hints, TypeScript uses strict mode
- ✅ **PASS**: Async/await patterns preferred, comprehensive error handling required
- ✅ **PASS**: Input validation on all API entry points, ORM usage for security

### Security Requirements (Principle 5)
- ✅ **PASS**: All API endpoints require JWT authentication
- ✅ **PASS**: Users only access their own data through authorization checks
- ✅ **PASS**: Passwords never stored in plain text, secrets managed through environment variables

### API Design Principles (Principle 6)
- ✅ **PASS**: RESTful conventions with JSON format, proper HTTP status codes
- ✅ **PASS**: User-specific data includes user ID in URL path for isolation
- ✅ **PASS**: Error responses follow consistent format, API versioning implemented

### Database Principles (Principle 7)
- ✅ **PASS**: Foreign key relationships enforced, frequently queried fields indexed
- ✅ **PASS**: All records include timestamps, schema changes tracked through migrations
- ✅ **PASS**: Database queries optimized, backup strategies implemented

### Performance Expectations (Principle 8)
- ✅ **PASS**: API response times under 200ms for CRUD operations
- ✅ **PASS**: Database connection pooling implemented, server-side rendering utilized
- ✅ **PASS**: Performance monitoring and regression tests included

### Development Workflow (Principle 9)
- ✅ **PASS**: Pull request review process, automated tests, code reviews required
- ✅ **PASS**: Branch naming conventions followed, commit messages conventional format
- ✅ **PASS**: Continuous integration validates all changes

### AI & MCP Architecture (Principle 10)
- ✅ **PASS**: MCP tools stateless and database-backed, conversation state persists to Neon DB
- ✅ **PASS**: Agent responses confirm actions explicitly, MCP tools validate user_id
- ✅ **PASS**: Chat endpoint stateless, no server-side conversation caching

### OpenAI Integration (Principle 11)
- ✅ **PASS**: Official OpenAI Agents SDK and MCP SDK usage, domain allowlist configuration
- ✅ **PASS**: JWT tokens from Better Auth required, API keys through environment variables
- ✅ **PASS**: AI-generated content logged with user context, rate limiting applied

### Error Handling & Resilience (Principle 12)
- ✅ **PASS**: MCP tools handle task not found errors gracefully, friendly user messages
- ✅ **PASS**: Failed tool calls logged but don't crash conversation, timeouts configured
- ✅ **PASS**: Retry logic for transient failures, user informed without technical details

## Project Structure

### Documentation (this feature)

```text
specs/002-chatbot-todo/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Web application structure (frontend + backend)
backend/
├── src/
│   ├── models/           # SQLModel database models (Task, Conversation, Message)
│   ├── services/         # Business logic services (task operations, chat logic)
│   ├── api/              # FastAPI endpoints (including /api/{user_id}/chat)
│   └── mcp/              # MCP server implementation with 5 task operation tools
├── tests/                # Backend test suite
└── migrations/           # Database migration scripts (Alembic or similar)

frontend/
├── src/
│   ├── components/       # React components (UI elements)
│   ├── pages/            # Next.js pages (/chat page with ChatKit)
│   ├── services/         # API client services (chat client, auth)
│   └── chat/             # ChatKit integration and chat UI components
└── public/               # Static assets
```

**Structure Decision**: Web application structure selected based on detected "frontend" + "backend" requirements. This provides clear separation between client-side React/Next.js components and server-side FastAPI services with proper API boundaries. All existing Phase 2 code resides under backend/ and frontend/ directories.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| MCP server integration | Required for AI tool exposure via Model Context Protocol | Direct API calls would bypass MCP ecosystem and tool standardization |
| Conversation persistence | Required for maintaining chat history across sessions | In-memory caching would violate statelessness guarantee |
| OpenAI Agents SDK | Required for natural language processing and intent extraction | Custom NLP would lack maturity and ecosystem support |
| Dual frontend/backend | Required for proper separation of concerns and scalability | Single-page application without backend would violate architecture principles |

## ChatKit Frontend Details

### /chat Route Implementation

**ChatKit Component Requirements**:
- Full-screen chat interface with conversation history display
- Message input with natural language processing capabilities
- Real-time message rendering with user/assistant attribution
- Conversation history scrolling with timestamp display
- Error handling for API failures and network issues
- Loading states for AI processing and message sending
- Responsive design for mobile and desktop

**Domain Allowlist Configuration**:
- OpenAI platform domain allowlist must be configured before deployment
- ChatKit requires proper CORS configuration for OpenAI API calls
- Frontend domain must be added to OpenAI allowlist for chat functionality
- Development and production domains require separate configurations

**Message Display Features**:
- Chronological message ordering with timestamps
- User messages displayed on right side, assistant on left
- Message status indicators (sending, sent, error)
- Markdown rendering for rich text content
- Link detection and clickable URL formatting
- Code block formatting for technical responses
- System message display for information and errors

**Conversation History Rendering**:
- Last 50 messages displayed by default
- Infinite scroll for older conversation history
- Search functionality for past messages
- Message filtering by user/assistant type
- Conversation context preservation across sessions
- Message deletion support (with proper authorization)

## Integration Flow

```
User → ChatKit Component → /api/{user_id}/chat Endpoint →
OpenAI Agents SDK → MCP Tools → Phase 2 Endpoints → Neon DB
```

### Detailed Flow Description:

1. **User Interaction**: User types natural language message in ChatKit interface
2. **Frontend Processing**: ChatKit captures message, validates input, shows sending state
3. **API Call**: POST /api/{user_id}/chat with conversation_id (optional) and message
4. **Authentication**: JWT token validation via Better Auth middleware
5. **Agent Processing**: OpenAI Agents SDK receives message and conversation context
6. **Tool Selection**: Agent identifies intent and selects appropriate MCP tool
7. **MCP Tool Execution**: MCP tool calls Phase 2 FastAPI endpoints internally
8. **Database Operations**: Phase 2 endpoints perform CRUD operations on Neon DB
9. **Response Generation**: Results returned to MCP tool, then to Agent, then to ChatKit
10. **UI Update**: ChatKit displays assistant response with proper formatting and attribution

### Data Flow Details:

- **Request Format**: `{ "conversation_id": "uuid", "message": "natural language text" }`
- **Response Format**: `{ "conversation_id": "uuid", "response": "assistant message", "tool_calls": [tool_call_objects] }`
- **State Management**: All conversation state stored in Neon DB, no in-memory caching
- **Error Handling**: Each layer provides user-friendly error messages without technical details
- **Security**: JWT validation at each API call, user data isolation enforced
- **Performance**: <5 second total response time including AI processing
- **Scalability**: Stateless design enables horizontal scaling of all components

### Component Responsibilities:

- **ChatKit**: UI rendering, user input capture, API integration, state management
- **FastAPI Endpoint**: Request validation, authentication, conversation context assembly, response formatting
- **OpenAI Agents SDK**: Intent recognition, tool selection, response generation
- **MCP Tools**: Stateless task operations, Phase 2 endpoint integration, error handling
- **Phase 2 Endpoints**: Database operations, business logic, data validation
- **Neon DB**: Persistent storage for conversations, messages, and tasks
