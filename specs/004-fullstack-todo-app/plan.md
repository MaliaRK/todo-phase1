# Implementation Plan: Authentication Extension for Todo App

**Branch**: `004-fullstack-todo-app` | **Date**: 2026-01-06 | **Spec**: [spec-auth-extension.md](spec-auth-extension.md)
**Input**: Feature specification from `/specs/004-fullstack-todo-app/spec-auth-extension.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement Better Auth with JWT authentication for the Phase II Todo application. This involves configuring Better Auth in the Next.js frontend for user registration/login, securing API communication with JWT tokens, and implementing JWT verification middleware in the FastAPI backend to enforce user-specific data access. The implementation will maintain existing API routes while adding authentication requirements and user isolation.

## Technical Context

**Language/Version**: Next.js 14+, FastAPI 0.104+, Python 3.11+, SQLModel
**Primary Dependencies**: Better Auth, JWT plugin, python-jose, Neon Serverless PostgreSQL, Claude Code, Spec-Kit Plus
**Storage**: Neon Serverless PostgreSQL database with SQLModel ORM
**Testing**: pytest (backend), Jest/React Testing Library (frontend)
**Target Platform**: Full-stack web application with Next.js frontend and FastAPI backend
**Project Type**: Multi-project structure with frontend/ and backend/ directories
**Performance Goals**: JWT token validation under 100ms for 99% of requests
**Constraints**: Must maintain existing API routes and business logic, no refresh tokens, no OAuth providers
**Scale/Scope**: Multi-user support with secure data isolation per user

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Code generation must be performed by Claude Code (no manual code writing)
- Implementation must follow written specifications from spec.md
- Developer acts as Product Architect (intentional design)
- Technology stack must match current phase requirements (no future-phase tech)
- Clean architecture and separation of concerns must be maintained
- All source code must reside in appropriate directory structure with modular logic
- Implementation must respect current phase's architectural constraints
- No global mutable state leakage allowed
- Follow phase-specific quality and documentation standards

## Project Structure

### Documentation (this feature)
```text
specs/004-fullstack-todo-app/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)
```text
backend/
├── src/
│   ├── models/
│   │   ├── task_model.py
│   │   └── user_model.py
│   ├── services/
│   │   ├── task_service.py
│   │   └── auth_service.py
│   ├── api/
│   │   ├── task_router.py
│   │   └── auth_router.py
│   ├── auth/
│   │   └── jwt_auth.py
│   └── main.py
├── tests/
│   ├── unit/
│   └── integration/
└── requirements.txt

frontend/
├── src/
│   ├── components/
│   │   ├── TaskList.jsx
│   │   ├── TaskForm.jsx
│   │   ├── TaskItem.jsx
│   │   └── Auth/
│   │       ├── Login.jsx
│   │       ├── Register.jsx
│   │       └── ProtectedRoute.jsx
│   ├── pages/
│   │   ├── index.jsx
│   │   ├── login.jsx
│   │   ├── register.jsx
│   │   └── api/
│   ├── services/
│   │   ├── api_client.js
│   │   └── auth_client.js
│   └── auth/
│       └── auth_provider.jsx
├── tests/
│   ├── unit/
│   └── integration/
└── package.json

docker-compose.yml
README.md
```

**Structure Decision**: Web application structure with separate backend and frontend directories to maintain full decoupling as required by specification. Backend uses FastAPI with SQLModel for data modeling and Neon PostgreSQL. Frontend uses Next.js for UI rendering and state management. Authentication components are added to both frontend and backend to support JWT-based user authentication and authorization.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [None] | [No violations identified] | [All constitution requirements met] |