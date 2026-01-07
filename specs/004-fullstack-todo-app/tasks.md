---
description: "Task list for Better Auth integration in Todo application"
---

# Tasks: Authentication Extension for Todo App

**Input**: Design documents from `/specs/004-fullstack-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are OPTIONAL - only include them if explicitly requested in the feature specification. Based on the specification, we will include basic tests for authentication functionality.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`, `backend/tests/`
- **Frontend**: `frontend/src/`, `frontend/tests/`
- **Shared**: `docker-compose.yml`, `README.md`, environment files

<!--
  ============================================================================
  IMPORTANT: The tasks below are GENERATED based on design documents.

  The /sp.tasks command generated these tasks based on:
  - User stories from spec.md (with their priorities P1, P2, P3...)
  - Feature requirements from plan.md
  - Entities from data-model.md
  - Endpoints from contracts/

  Tasks MUST be organized by user story so each story can be:
  - Implemented independently
  - Tested independently
  - Delivered as an MVP increment

  DO NOT modify these sample tasks - they represent the actual implementation plan.
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure with backend and frontend directories per implementation plan
- [X] T002 [P] Initialize backend with FastAPI, SQLModel, and required dependencies in backend/requirements.txt
- [X] T003 [P] Initialize frontend with Next.js in frontend/ directory
- [ ] T004 [P] Configure linting and formatting tools for both backend (flake8, black) and frontend (eslint, prettier)
- [X] T005 Set up database connection with Neon PostgreSQL configuration in backend/.env
- [X] T006 Create backend/src directory structure: models/, services/, api/, main.py
- [X] T007 Create frontend/src directory structure: components/, pages/, services/
- [ ] T008 [P] Configure development environment with proper Python virtual environment
- [X] T009 [P] Configure Next.js project with proper package.json dependencies
- [X] T010 Set up docker-compose.yml for local development environment

---
## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T011 Set up SQLModel database models infrastructure in backend/src/models/
- [X] T012 [P] Implement database session management and connection pooling in backend/src/database/
- [X] T013 [P] Setup FastAPI application structure with CORS and middleware in backend/src/main.py
- [X] T014 Create base API router configuration in backend/src/api/
- [ ] T015 [P] Implement error handling and validation middleware for backend
- [ ] T016 [P] Setup frontend API client service to communicate with backend in frontend/src/services/
- [X] T017 Configure environment variables for backend and frontend
- [ ] T018 Set up basic authentication framework if needed (session/JWT)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 2.5: Authentication Foundation (Blocking Prerequisites)

**Purpose**: Core authentication infrastructure that MUST be complete before authentication user stories can be implemented

**⚠️ CRITICAL**: No authentication user story work can begin until this phase is complete

- [X] T076 Create User model in backend/src/models/user_model.py
- [X] T077 Create Session model in backend/src/models/session_model.py
- [X] T078 [P] Create JWT authentication dependency in backend/src/auth/jwt_auth.py
- [X] T079 [P] Create authentication service in backend/src/services/auth_service.py
- [X] T080 Update Task model to include user_id foreign key in backend/src/models/task_model.py
- [X] T081 Create auth router in backend/src/api/auth_router.py
- [X] T082 Create auth provider in frontend/src/auth/auth_provider.jsx
- [X] T083 [P] Create auth client service in frontend/src/services/auth_client.js
- [ ] T084 Install Better Auth dependencies in frontend package.json
- [ ] T085 Install JWT and authentication dependencies in backend requirements.txt
- [ ] T086 [P] Update backend requirements.txt with python-jose and cryptography
- [ ] T087 [P] Update frontend package.json with better-auth and related packages
- [ ] T088 Configure environment variables for BETTER_AUTH_SECRET in both frontend and backend

**Checkpoint**: Authentication foundation ready - authentication user stories can now begin

---

## Phase 3: User Story 1 - New User Registration (Priority: P1) 🎯 MVP

**Goal**: Enable new users to register for accounts with email and password

**Independent Test**: A new user can visit the registration page, provide their email and password, and successfully create a new account that is securely stored in the system.

### Tests for User Story 1 (OPTIONAL - included for auth functionality) ⚠️

- [ ] T089 [P] [US1] Contract test for registration endpoint in backend/tests/contract/test_auth_contract.py
- [ ] T090 [P] [US1] Integration test for registration flow in backend/tests/integration/test_auth_integration.py

### Implementation for User Story 1

- [ ] T091 [P] [US1] Create registration endpoint in backend/src/api/auth_router.py
- [ ] T092 [US1] Create registration form component in frontend/src/components/Auth/Register.jsx
- [ ] T093 [US1] Create registration page in frontend/src/pages/register.jsx
- [ ] T094 [US1] Implement registration form submission logic in frontend/src/components/Auth/Register.jsx
- [ ] T095 [US1] Update auth service to handle registration in backend/src/services/auth_service.py
- [ ] T096 [US1] Add email validation and duplicate check in registration endpoint

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - User Login and Session Management (Priority: P1)

**Goal**: Enable existing users to log in to the Todo application and maintain secure session management

**Independent Test**: A registered user can log in with their credentials, maintain a secure session while using the application, and log out to end their session.

### Tests for User Story 2 (OPTIONAL - included for auth functionality) ⚠️

- [ ] T097 [P] [US2] Contract test for login endpoint in backend/tests/contract/test_auth_contract.py
- [ ] T098 [P] [US2] Contract test for logout endpoint in backend/tests/contract/test_auth_contract.py

### Implementation for User Story 2

- [ ] T099 [P] [US2] Create login endpoint in backend/src/api/auth_router.py
- [ ] T100 [P] [US2] Create logout endpoint in backend/src/api/auth_router.py
- [ ] T101 [US2] Create login form component in frontend/src/components/Auth/Login.jsx
- [ ] T102 [US2] Create login page in frontend/src/pages/login.jsx
- [ ] T103 [US2] Create protected route component in frontend/src/components/Auth/ProtectedRoute.jsx
- [ ] T104 [US2] Implement login form submission logic in frontend/src/components/Auth/Login.jsx
- [ ] T105 [US2] Update auth service to handle login/logout in backend/src/services/auth_service.py
- [ ] T106 [US2] Implement session management in frontend/src/auth/auth_provider.jsx

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Secure Task Access (Priority: P1)

**Goal**: Ensure authenticated users can only access their own tasks, maintaining data privacy and security

**Independent Test**: When a user accesses their tasks via API, they only see tasks that belong to their account, regardless of what other users' data exists in the system.

### Tests for User Story 3 (OPTIONAL - included for auth functionality) ⚠️

- [ ] T107 [P] [US3] Contract test for user-specific task endpoints in backend/tests/contract/test_task_auth_contract.py
- [ ] T108 [P] [US3] Integration test for user isolation in backend/tests/integration/test_task_isolation.py

### Implementation for User Story 3

- [ ] T109 [P] [US3] Update task endpoints to require user_id in path in backend/src/api/task_router.py
- [ ] T110 [US3] Add JWT authentication dependency to task endpoints in backend/src/api/task_router.py
- [ ] T111 [US3] Update task service to filter by authenticated user_id in backend/src/services/task_service.py
- [ ] T112 [US3] Update task creation to automatically assign user_id from JWT in backend/src/services/task_service.py
- [ ] T113 [US3] Update frontend API client to include JWT in authorization header in frontend/src/services/api_client.js
- [ ] T114 [US3] Update frontend task components to use user-specific endpoints

**Checkpoint**: All user stories should now be independently functional

---
## Phase 6: User Story 4 - JWT Token Management (Priority: P2)

**Goal**: Securely manage JWT tokens for API authentication, ensuring secure communication between frontend and backend

**Independent Test**: API requests between frontend and backend include valid JWT tokens in headers, and tokens are properly validated on the backend.

### Tests for User Story 4 (OPTIONAL - included for auth functionality) ⚠️

- [ ] T061 [P] [US4] Unit test for JWT validation in backend/tests/unit/test_jwt_auth.py
- [ ] T062 [P] [US4] Integration test for token validation in backend/tests/integration/test_jwt_validation.py

### Implementation for User Story 4

- [ ] T063 [P] [US4] Configure Better Auth with JWT plugin in frontend/src/auth/auth_provider.jsx
- [ ] T064 [US4] Ensure JWT includes required claims (sub, email, iat, exp) in auth configuration
- [ ] T065 [US4] Configure secure session cookies (HttpOnly, Secure, SameSite=Lax) in auth configuration
- [ ] T066 [US4] Update JWT validation middleware to extract user_id and validate against path parameter
- [ ] T067 [US4] Add error handling for missing/invalid/expired tokens in backend/src/auth/jwt_auth.py
- [ ] T068 [US4] Update frontend to handle 401 responses and redirect to login

**Checkpoint**: All user stories should now be fully integrated and functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T069 [P] Update README.md with authentication setup instructions
- [ ] T070 Update quickstart.md with authentication workflow
- [ ] T071 [P] Add proper error handling and user feedback for auth failures
- [ ] T072 Add validation for JWT user_id matching path parameter
- [ ] T073 [P] Add additional unit tests for auth components
- [ ] T074 Security hardening and validation
- [ ] T075 Run quickstart.md validation to ensure complete workflow
- [ ] T052 [P] Add comprehensive error handling and validation in backend
- [ ] T053 [P] Add input validation to frontend forms
- [ ] T054 Add proper loading states and user feedback throughout application
- [X] T055 [P] Add documentation updates in README.md
- [ ] T056 Add environment configuration for different deployment stages
- [ ] T057 [P] Add comprehensive tests (unit, integration) for all components
- [ ] T058 Add logging configuration for backend
- [ ] T059 Add frontend build optimization and performance improvements
- [ ] T060 Run quickstart.md validation and update if needed

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
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P1)**: Can start after Foundational (Phase 2) - Depends on authentication being in place (US1/US2)
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - May integrate with other stories but should be independently testable

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
Task: "Contract test for GET /api/v1/tasks in backend/tests/contract/test_tasks.py"
Task: "Contract test for POST /api/v1/tasks in backend/tests/contract/test_tasks.py"

# Launch all models for User Story 1 together:
Task: "Create Task model in backend/src/models/task_model.py"
Task: "Implement Task service with create and list methods in backend/src/services/task_service.py"
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

1. Team completes Setup + Foundational + Authentication Foundation together
2. Once Authentication Foundation is done:
   - Developer A: User Story 1 (Registration)
   - Developer B: User Story 2 (Login/Session)
   - Developer C: User Story 3 (Secure Task Access)
   - Developer D: User Story 4 (JWT Management)
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