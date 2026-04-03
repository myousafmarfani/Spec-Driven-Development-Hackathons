---
description: "Task list template for feature implementation"
---

# Tasks: Full-Stack Todo Web Application

**Input**: Design documents from `/specs/1-fullstack-todo-app/`
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

<!--
  ============================================================================
  IMPORTANT: The tasks below are SAMPLE TASKS for illustration purposes only.

  The /sp.tasks command MUST replace these with actual tasks based on:
  - User stories from spec.md (with their priorities P1, P2, P3...)
  - Feature requirements from plan.md
  - Entities from data-model.md
  - Endpoints from contracts/

  Tasks MUST be organized by user story so each story can be:
  - Implemented independently
  - Tested independently
  - Delivered as an MVP increment

  DO NOT keep these sample tasks in the generated tasks.md file.
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create backend directory structure and pyproject.toml
- [x] T002 Create frontend directory structure with Next.js app router
- [x] T003 [P] Configure CLAUDE.md files for backend and frontend with development guidelines
- [x] T004 [P] Install backend dependencies (FastAPI, SQLModel, Pydantic, etc.)
- [x] T005 [P] Install frontend dependencies (Next.js 16, TypeScript, Tailwind CSS, Better Auth)

---
## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [x] T006 Create Neon PostgreSQL database and copy connection string
- [x] T007 Create backend models.py with User and Task SQLModel classes
- [x] T008 [P] Create database connection module (db.py) with engine and session
- [x] T009 [P] Create authentication module (auth.py) with JWT verification
- [x] T010 Create Pydantic schemas (schemas.py) for Task entities
- [x] T011 Create backend routes directory with tasks.py for API endpoints
- [x] T012 Configure FastAPI application (main.py) with CORS and route inclusion
- [x] T013 [P] Initialize database tables and indexes via init_db.py script

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration & Login (Priority: P1) 🎯 MVP

**Goal**: Enable user registration and authentication to access the application

**Independent Test**: Can be fully tested by registering with an email/password, receiving a successful response, and verifying the account exists in the system.

### Implementation for User Story 1

- [x] T014 [P] [US1] Configure Better Auth in frontend/lib/auth.ts
- [x] T015 [P] [US1] Create signup page in frontend/app/auth/signup/page.tsx
- [x] T016 [P] [US1] Create signin page in frontend/app/auth/signin/page.tsx
- [x] T017 [US1] Implement authentication middleware in frontend/middleware.ts
- [x] T018 [US1] Test authentication flow with manual API calls

**Checkpoint**: At this point, users can register and authenticate with the system

---
## Phase 4: User Story 2 - Task Management (Priority: P2)

**Goal**: Enable authenticated users to create, view, update, delete, and mark tasks as complete/incomplete

**Independent Test**: Can be tested by creating a task, viewing it in the list, updating its details, marking it as complete, and finally deleting it - all operations should work independently for the authenticated user.

### Implementation for User Story 2

- [x] T019 [P] [US2] Create backend GET /api/{user_id}/tasks endpoint in routes/tasks.py
- [x] T020 [P] [US2] Create backend POST /api/{user_id}/tasks endpoint in routes/tasks.py
- [x] T021 [P] [US2] Create backend PUT /api/{user_id}/tasks/{task_id} endpoint in routes/tasks.py
- [x] T022 [US2] Create backend DELETE /api/{user_id}/tasks/{task_id} endpoint in routes/tasks.py
- [x] T023 [US2] Create backend PATCH /api/{user_id}/tasks/{task_id}/complete endpoint in routes/tasks.py
- [x] T024 [P] [US2] Create API client wrapper in frontend/lib/api.ts
- [x] T025 [P] [US2] Create TypeScript types in frontend/lib/types.ts
- [x] T026 [P] [US2] Create TaskList component in frontend/components/tasks/TaskList.tsx
- [x] T027 [P] [US2] Create TaskItem component in frontend/components/tasks/TaskItem.tsx
- [x] T028 [P] [US2] Create TaskForm component in frontend/components/tasks/TaskForm.tsx
- [x] T029 [US2] Create Delete confirmation dialog in frontend/components/tasks/DeleteDialog.tsx
- [x] T030 [US2] Create tasks page in frontend/app/tasks/page.tsx
- [x] T031 [US2] Test end-to-end task management flows

**Checkpoint**: At this point, User Story 2 should be fully functional and testable independently

---
## Phase 5: User Story 3 - Secure Access Control (Priority: P3)

**Goal**: Ensure users can only see and modify their own tasks, enforcing data isolation

**Independent Test**: Can be tested by verifying that a user cannot access, modify, or delete another user's tasks through various API endpoints - this ensures proper data isolation.

### Implementation for User Story 3

- [x] T032 [P] [US3] Enhance JWT verification middleware to validate user_id matches token
- [x] T033 [P] [US3] Add user_id validation to all task endpoints to enforce data isolation
- [x] T034 [US3] Test that users cannot access other users' tasks via API
- [x] T035 [US3] Test that users cannot modify other users' tasks
- [x] T036 [US3] Test that users cannot delete other users' tasks

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently with proper security

---

[Add more user story phases as needed, following the same pattern]

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T037 [P] Configure environment variables for frontend and backend
- [x] T038 Update README.md with setup and deployment instructions
- [x] T039 [P] Add loading states and error handling to UI components
- [x] T040 Add success/toast notifications for user actions
- [x] T041 Improve responsive design for mobile devices
- [x] T042 Deploy backend to hosting platform (Railway/Vercel)
- [x] T043 Deploy frontend to Vercel
- [x] T044 Test production deployment with all features

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 2

```bash
# Launch all models for User Story 2 together:
Task: "Create Pydantic schemas in backend/schemas.py"
Task: "Create TypeScript types in frontend/lib/types.ts"

# Launch all components for User Story 2 together:
Task: "Create TaskList component in frontend/components/tasks/TaskList.tsx"
Task: "Create TaskItem component in frontend/components/tasks/TaskItem.tsx"
Task: "Create TaskForm component in frontend/components/tasks/TaskForm.tsx"
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
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence