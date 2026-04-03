# Tasks: AI Chatbot for Todo Management

**Input**: Design documents from `/specs/002-chatbot-todo/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan
- [ ] T002 Initialize FastAPI project with required dependencies (uv, fastapi, sqlmodel, pydantic, better-auth, openai, mcp)
- [ ] T003 [P] Configure linting and formatting tools (black, isort, ruff, mypy)
- [ ] T004 [P] Setup Next.js frontend project with required dependencies (react, typescript, tailwind, better-auth, openai)
- [ ] T005 [P] Initialize Neon PostgreSQL database and configure connection
- [ ] T006 [P] Setup environment configuration management (.env, .env.example)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T007 Setup database schema and migrations framework (Alembic or similar)
- [ ] T008 [P] Implement authentication/authorization framework with Better Auth
- [ ] T009 [P] Setup API routing and middleware structure in FastAPI
- [ ] T010 Create base models/entities that all stories depend on (User, Task from Phase 2)
- [ ] T011 Configure error handling and logging infrastructure
- [ ] T012 Setup environment configuration management

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create and Manage Tasks via Chat (Priority: P1) 🎯 MVP

**Goal**: Enable users to create, view, complete, and delete tasks using natural language commands through chat interface

**Independent Test**: User can send authenticated chat messages like "add task buy groceries" and receive appropriate responses while task list changes accordingly

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T013 [P] [US1] Contract test for POST /api/{user_id}/chat endpoint in tests/contract/test_chat.py
- [ ] T014 [P] [US1] Integration test for chat user journey in tests/integration/test_chat_journey.py

### Implementation for User Story 1

- [ ] T015 [P] [US1] Create Conversation model with SQLModel in backend/src/models/conversation.py
- [ ] T016 [P] [US1] Create Message model with SQLModel in backend/src/models/message.py
- [ ] T017 [US1] Implement database migrations for Conversation and Message models (T-303)
- [ ] T018 [P] [US1] Create Chat service in backend/src/services/chat_service.py
- [ ] T019 [P] [US1] Create Conversation service in backend/src/services/conversation_service.py
- [ ] T020 [P] [US1] Create Message service in backend/src/services/message_service.py
- [ ] T021 [P] [US1] Create POST /api/{user_id}/chat route in backend/src/api/chat.py (T-314)
- [ ] T022 [US1] Implement conversation state fetch and save logic in chat service (T-315)
- [ ] T023 [US1] Integrate OpenAI agent runner with MCP tools in chat endpoint (T-316)
- [ ] T024 [US1] Add JWT authentication and user_id validation to chat endpoint (T-317)
- [ ] T025 [US1] Add validation and error handling for chat operations
- [ ] T026 [US1] Add logging for chat operations

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Persistent Conversation History (Priority: P2)

**Goal**: Enable users to view their conversation history with the chatbot across sessions

**Independent Test**: User can return to chat interface and see previous conversation messages displayed in chronological order

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T026 [P] [US2] Contract test for conversation history endpoint in tests/contract/test_conversation_history.py
- [ ] T027 [P] [US2] Integration test for conversation history user journey in tests/integration/test_conversation_history.py

### Implementation for User Story 2

- [ ] T028 [P] [US2] Install OpenAI ChatKit in Next.js frontend (T-318)
- [ ] T029 [P] [US2] Create ChatKit frontend component in frontend/src/chat/ChatKit.tsx
- [ ] T030 [P] [US2] Configure OpenAI domain allowlist and get domain key (T-320)
- [ ] T031 [P] [US2] Create /chat page route with ChatKit component in frontend/src/pages/chat.tsx (T-319)
- [ ] T032 [P] [US2] Implement chat API client with JWT headers in frontend/src/services/chat_client.ts (T-321)
- [ ] T033 [P] [US2] Implement message display and input components in frontend/src/chat/MessageDisplay.tsx and frontend/src/chat/MessageInput.tsx
- [ ] T034 [P] [US2] Add conversation history display with last 50 messages (T-322)
- [ ] T035 [US2] Implement conversation history rendering and message formatting
- [ ] T036 [US2] Integrate ChatKit with backend /api/{user_id}/chat endpoint (T-033)
- [ ] T037 [US2] Add responsive design for mobile and desktop
- [ ] T038 [US2] Add loading states for AI processing and message sending

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Natural Language Variations (Priority: P3)

**Goal**: Enable chatbot to understand at least 8 distinct natural language patterns for task operations

**Independent Test**: User can issue same command in different phrasings and chatbot correctly extracts intent and executes appropriate operation

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T036 [P] [US3] Contract test for natural language variations in tests/contract/test_natural_language.py
- [ ] T037 [P] [US3] Integration test for natural language patterns in tests/integration/test_natural_language_patterns.py

### Implementation for User Story 3

- [ ] T038 [P] [US3] Install and configure OpenAI Agents SDK (T-311)
- [ ] T039 [P] [US3] Create todo agent with MCP tools configuration (T-312)
- [ ] T040 [P] [US3] Implement agent runner with conversation history support (T-313)
- [ ] T041 [P] [US3] Implement at least 8 distinct natural language patterns for task operations
- [ ] T042 [P] [US3] Add intent recognition and entity extraction logic
- [ ] T043 [P] [US3] Integrate with existing MCP tools for task operations
- [ ] T044 [P] [US3] Add natural language variation testing and validation

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: MCP Server (T-304 to T-310)

**Purpose**: Implement MCP server with task operation tools

- [ ] T045 [P] Set up Official MCP SDK project structure (T-304)
- [ ] T046 [P] Implement add_task MCP tool (calls POST /api/{user_id}/tasks) (T-305)
- [ ] T047 [P] Implement list_tasks MCP tool (calls GET /api/{user_id}/tasks) (T-306)
- [ ] T048 [P] Implement complete_task MCP tool (calls PATCH complete endpoint) (T-307)
- [ ] T049 [P] Implement delete_task MCP tool (calls DELETE endpoint) (T-308)
- [ ] T050 [P] Implement update_task MCP tool (calls PUT endpoint) (T-309)
- [ ] T051 [P] Add MCP server startup script (T-310)

---

## Phase 7: Database (T-301 to T-303)

**Purpose**: Create and setup database models and migrations

- [ ] T052 Create Conversation model with SQLModel (T-301)
- [ ] T053 Create Message model with SQLModel (T-302)
- [ ] T054 Generate and run database migrations (T-303)

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T055 [P] Documentation updates in docs/
- [ ] T056 Code cleanup and refactoring
- [ ] T057 Performance optimization across all stories
- [ ] T058 [P] Additional unit tests (if requested) in tests/unit/
- [ ] T059 Security hardening
- [ ] T060 Run quickstart.md validation
- [ ] T061 Integration testing of complete system
- [ ] T062 Performance testing and optimization

---

## Phase 9: Testing & Validation (T-323 to T-325)

**Purpose**: Comprehensive testing of all specified acceptance criteria

- [ ] T063 [P] Test 8 natural language commands from spec (T-323)
- [ ] T064 [P] Test error handling for invalid task IDs and deleted tasks (T-324)
- [ ] T065 [P] Test conversation persistence across server restarts (T-325)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **MCP Server (Phase 6)**: Depends on Foundational; can parallel with User Stories after Phase 2
- **Database (Phase 7)**: Depends on Foundational and should be complete before User Stories need it
- **Testing & Validation (Phase 9)**: Depends on all desired user stories and MCP/Database phases being complete
- **Polish (Phase 8)**: Depends on all desired user stories being complete; can overlap with Testing

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on Phase 4 tasks; integrates with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Depends on Phase 5 tasks (MCP, Agents SDK); may integrate with US1/US2 but should be independently testable

### Cross-Phase Dependencies

- **Phase 3 (US1)**: Needs Phase 7 (Database models) complete or in parallel
- **Phase 4 (US2)**: Needs Phase 3 (US1) for full integration; frontend can start after Phase 2
- **Phase 5 (US3)**: Needs Phase 6 (MCP Server) and T038-T040 (Agents SDK) complete
- **Phase 9 (Testing)**: Needs all functional phases (3-6) complete to validate complete system

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for POST /api/{user_id}/chat endpoint in tests/contract/test_chat.py"
Task: "Integration test for chat user journey in tests/integration/test_chat_journey.py"

# Launch all models for User Story 1 together:
Task: "Create Conversation model with SQLModel in backend/src/models/conversation.py"
Task: "Create Message model with SQLModel in backend/src/models/message.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence