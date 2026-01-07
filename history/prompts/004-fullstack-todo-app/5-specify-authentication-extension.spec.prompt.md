---
id: 5
title: specify-authentication-extension
stage: spec
date: 2026-01-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: 004-fullstack-todo-app
branch: 004-fullstack-todo-app
user: user
command: /sp.specify
labels: ["auth", "authentication", "jwt", "specification"]
links:
  spec: specs/004-fullstack-todo-app/spec-auth-extension.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/004-fullstack-todo-app/spec-auth-extension.md
 - specs/004-fullstack-todo-app/checklists/auth-extension-requirements.md
tests:
 - null
---

## Prompt

# sp.specify — Phase II Authentication Extension

## Context
We have an existing Phase II Todo Full-Stack Web Application already implemented using:
- Next.js (App Router)
- FastAPI
- SQLModel
- Neon Serverless PostgreSQL
- Spec-Kit Plus + Claude Code
- REST APIs for Todo CRUD

All basic-level Todo functionality is complete.

## Objective
Extend the existing Phase II specification to add **authentication and authorization** using **Better Auth with JWT**, without changing existing API routes or business logic.

## Authentication Requirements

### Frontend (Next.js)
- Integrate **Better Auth** for:
  - User signup
  - User signin
  - Session management
- Enable **JWT plugin** in Better Auth configuration
- JWT must include:
  - `sub` (user_id)
  - `email`
  - `iat`, `exp`
- Store session securely using:
  - HttpOnly cookies
  - Secure flag (in production)
  - SameSite=Lax

### Token Handling
- JWT token must be accessible to the frontend API client
- Every API request to FastAPI must include:
  - `Authorization: Bearer <JWT_TOKEN>` header

## Backend (FastAPI)
- Add JWT verification middleware or dependency
- Verify JWT using:
  - Shared secret from environment variable `BETTER_AUTH_SECRET`
  - HS256 algorithm
- Reject requests with:
  - Missing token → 401 Unauthorized
  - Invalid token → 401 Unauthorized
  - Expired token → 401 Unauthorized

### User Identity Enforcement
- Decode JWT to extract:
  - `user_id`
- Ensure:
  - `user_id` in JWT MUST match `user_id` in route path
- All database queries must be filtered by authenticated `user_id`
- Users must only access their own tasks

## API Behavior Changes
- All `/api/{user_id}/tasks` endpoints now require authentication
- No unauthenticated access allowed
- Task ownership is enforced at every CRUD operation

## Non-Goals
- Do NOT implement refresh tokens
- Do NOT change existing API routes
- Do NOT add OAuth providers

## Constraints
- No manual code writing
- Use Spec-Kit Plus structure
- Use Claude Code for all implementations
- Existing repo structure and branches must be preserved
- This update applies ONLY to Phase II branch

## Deliverables
- Updated spec documents
- JWT-secured FastAPI backend
- Better Auth–enabled Next.js frontend
- Fully authenticated multi-user Todo app

## Response snapshot

# Feature Specification: Authentication Extension for Todo App

**Feature Branch**: `004-fullstack-todo-app`
**Created**: 2026-01-06
**Status**: Draft
**Input**: User description: "# sp.specify — Phase II Authentication Extension

## Context
We have an existing Phase II Todo Full-Stack Web Application already implemented using:
- Next.js (App Router)
- FastAPI
- SQLModel
- Neon Serverless PostgreSQL
- Spec-Kit Plus + Claude Code
- REST APIs for Todo CRUD

All basic-level Todo functionality is complete.

## Objective
Extend the existing Phase II specification to add **authentication and authorization** using **Better Auth with JWT**, without changing existing API routes or business logic.

## Authentication Requirements

### Frontend (Next.js)
- Integrate **Better Auth** for:
  - User signup
  - User signin
  - Session management
- Enable **JWT plugin** in Better Auth configuration
- JWT must include:
  - `sub` (user_id)
  - `email`
  - `iat`, `exp`
- Store session securely using:
  - HttpOnly cookies
  - Secure flag (in production)
  - SameSite=Lax

### Token Handling
- JWT token must be accessible to the frontend API client
- Every API request to FastAPI must include:
  - `Authorization: Bearer <JWT_TOKEN>` header

## Backend (FastAPI)
- Add JWT verification middleware or dependency
- Verify JWT using:
  - Shared secret from environment variable `BETTER_AUTH_SECRET`
  - HS256 algorithm
- Reject requests with:
  - Missing token → 401 Unauthorized
  - Invalid token → 401 Unauthorized
  - Expired token → 401 Unauthorized

### User Identity Enforcement
- Decode JWT to extract:
  - `user_id`
- Ensure:
  - `user_id` in JWT MUST match `user_id` in route path
- All database queries must be filtered by authenticated `user_id`
- Users must only access their own tasks

## API Behavior Changes
- All `/api/{user_id}/tasks` endpoints now require authentication
- No unauthenticated access allowed
- Task ownership is enforced at every CRUD operation

## Non-Goals
- Do NOT implement refresh tokens
- Do NOT change existing API routes
- Do NOT add OAuth providers

## Constraints
- No manual code writing
- Use Spec-Kit Plus structure
- Use Claude Code for all implementations
- Existing repo structure and branches must be preserved
- This update applies ONLY to Phase II branch

## Deliverables
- Updated spec documents
- JWT-secured FastAPI backend
- Better Auth–enabled Next.js frontend
- Fully authenticated multi-user Todo app"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - New User Registration (Priority: P1)

A new user wants to create an account in the Todo application so they can securely store and manage their personal tasks without other users accessing them.

**Why this priority**: This is the foundational requirement for multi-user functionality - without user registration, no other authentication features are possible.

**Independent Test**: A new user can visit the registration page, provide their email and password, and successfully create a new account that is securely stored in the system.

**Acceptance Scenarios**:

1. **Given** a user is on the registration page, **When** they enter valid email and password and submit the form, **Then** a new account is created and they are redirected to the login page
2. **Given** a user enters an already registered email, **When** they submit the registration form, **Then** they receive an error message indicating the email is already in use
3. **Given** a user enters invalid email format or weak password, **When** they submit the registration form, **Then** they receive appropriate validation error messages

---

### User Story 2 - User Login and Session Management (Priority: P1)

An existing user wants to log in to the Todo application so they can access their personal tasks with secure session management.

**Why this priority**: Essential for users to access their existing data and maintain a secure session across their usage.

**Independent Test**: A registered user can log in with their credentials, maintain a secure session while using the application, and log out to end their session.

**Acceptance Scenarios**:

1. **Given** a user is on the login page, **When** they enter valid credentials and submit, **Then** they are logged in and redirected to their task dashboard
2. **Given** a user enters invalid credentials, **When** they submit the login form, **Then** they receive an appropriate error message
3. **Given** a user is logged in and active, **When** they navigate between different parts of the application, **Then** their authentication state is maintained
4. **Given** a user is logged in, **When** they click logout, **Then** their session is securely ended and they are redirected to the login page

---

### User Story 3 - Secure Task Access (Priority: P1)

An authenticated user wants to access only their own tasks, ensuring data privacy and security in the multi-user environment.

**Why this priority**: Critical for data security and privacy - users must only access their own data, not others'.

**Independent Test**: When a user accesses their tasks via API, they only see tasks that belong to their account, regardless of what other users' data exists in the system.

**Acceptance Scenarios**:

1. **Given** a user is authenticated, **When** they request their task list, **Then** they only see tasks associated with their user ID
2. **Given** a user is authenticated, **When** they try to access another user's tasks, **Then** they receive a 401 Unauthorized error
3. **Given** a user is not authenticated, **When** they try to access any task data, **Then** they receive a 401 Unauthorized error

---

### User Story 4 - JWT Token Management (Priority: P2)

The system needs to securely manage JWT tokens for API authentication, ensuring secure communication between frontend and backend.

**Why this priority**: Essential for secure API communication while maintaining good user experience without constant re-authentication.

**Independent Test**: API requests between frontend and backend include valid JWT tokens in headers, and tokens are properly validated on the backend.

**Acceptance Scenarios**:

1. **Given** a user is logged in, **When** they make API requests to the backend, **Then** each request includes a valid JWT token in the Authorization header
2. **Given** an API request has a valid JWT token, **When** it reaches the backend, **Then** the request is processed normally
3. **Given** an API request has an invalid or expired JWT token, **When** it reaches the backend, **Then** the request is rejected with 401 Unauthorized

---

### Edge Cases

- What happens when a JWT token expires during an active session?
- How does the system handle concurrent sessions from the same user account?
- What happens when a user account is deleted while they have active sessions?
- How does the system handle malformed JWT tokens?
- What happens when the authentication server is temporarily unavailable?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST follow written specifications as defined in this document
- **FR-002**: System MUST be generated by Claude Code (no manual code writing allowed)
- **FR-003**: Users MUST be able to register new accounts with email and password
- **FR-004**: Users MUST be able to securely log in to their accounts
- **FR-005**: Users MUST be able to securely log out of their accounts
- **FR-006**: System MUST use Better Auth with JWT for authentication
- **FR-007**: JWT tokens MUST include sub (user_id), email, iat, and exp claims
- **FR-008**: JWT tokens MUST be stored securely using HttpOnly cookies
- **FR-009**: JWT tokens MUST use HS256 algorithm for verification
- **FR-010**: System MUST verify JWT tokens using BETTER_AUTH_SECRET environment variable
- **FR-011**: System MUST reject requests with missing, invalid, or expired tokens with 401 status
- **FR-012**: System MUST ensure JWT user_id matches the user_id in route path
- **FR-013**: System MUST filter all database queries by authenticated user_id
- **FR-014**: Users MUST only access their own tasks through CRUD operations
- **FR-015**: All existing /api/{user_id}/tasks endpoints MUST require authentication
- **FR-016**: System MUST NOT allow unauthenticated access to task endpoints
- **FR-017**: Frontend API client MUST include Authorization: Bearer <JWT_TOKEN> header for all requests
- **FR-018**: System MUST maintain existing API routes without changes
- **FR-019**: System MUST maintain existing business logic without changes
- **FR-020**: Session cookies MUST use Secure flag in production
- **FR-021**: Session cookies MUST use SameSite=Lax attribute
- **FR-022**: System MUST NOT implement refresh tokens
- **FR-023**: System MUST NOT add OAuth providers

### Key Entities

- **User**: Represents a registered user account with unique identifier (user_id), email, and authentication credentials
- **Session**: Represents an authenticated user's active session with JWT token containing user identity claims
- **Task**: Represents a todo item that is associated with a specific user_id and accessible only by that user

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete account registration in under 1 minute with 95% success rate
- **SC-002**: Users can log in to their accounts in under 30 seconds with 98% success rate
- **SC-003**: 100% of API requests from authenticated users include valid JWT tokens
- **SC-004**: 100% of unauthorized access attempts to task data return 401 Unauthorized error
- **SC-005**: Users can only access tasks that belong to their own account (0% cross-user data access)
- **SC-006**: JWT token validation completes in under 100ms for 99% of requests
- **SC-007**: Session management provides secure authentication without impacting user experience
- **SC-008**: System maintains backward compatibility with existing API routes and business logic

## Outcome

- ✅ Impact: Created comprehensive authentication extension specification for the Todo app, enabling multi-user functionality with JWT-based authentication
- 🧪 Tests: No tests created yet, specification phase
- 📁 Files: Created spec-auth-extension.md and auth-extension-requirements.md checklist
- 🔁 Next prompts: Ready for /sp.clarify or /sp.plan to continue development
- 🧠 Reflection: Specification addresses all requirements from user input with clear user scenarios, functional requirements, and success criteria

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Specification validation passed all quality checklist items
- Prompt variant (if applicable): Standard spec creation
- Next experiment (smallest change to try): Proceed with planning phase to implement the authentication features