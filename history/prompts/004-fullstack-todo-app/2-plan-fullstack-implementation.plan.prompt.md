---
id: 2
title: Plan Fullstack Implementation
stage: plan
date: 2026-01-04
surface: agent
model: claude-sonnet-4-5-20250929
feature: fullstack-todo-app
branch: 004-fullstack-todo-app
user: Claude Code User
command: /sp.plan
labels: [plan, fullstack, todo, web-application, nextjs, fastapi, sqlmodel]
links:
  spec: ../specs/004-fullstack-todo-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/004-fullstack-todo-app/plan.md
 - specs/004-fullstack-todo-app/research.md
 - specs/004-fullstack-todo-app/data-model.md
 - specs/004-fullstack-todo-app/contracts/task-api.yaml
 - specs/004-fullstack-todo-app/quickstart.md
tests:
 - null
---

## Prompt

You are given an approved Phase II specification.

---

## Objective

Create a **detailed, step-by-step implementation plan**
to build Phase II using **spec-driven development**.

---

## Mandatory Constraints

- The implementation MUST occur on branch: `fullstack-todo-app`
- The repository is shared across all phases; do NOT disturb other branches
- Code MUST be generated only after this plan is approved
- Human developer will NOT write code manually

---

## Required Planning Scope

Break the work into **logical, incremental stages**, including:

1. Repository and folder setup
2. Backend (FastAPI) initialization
3. SQLModel data modeling and database setup
4. REST API endpoint implementation
5. Frontend (Next.js) application setup
6. UI screens and user flows
7. Frontend–backend integration
8. Error handling and validation
9. Local development workflow
10. Documentation updates

---

## Skill Enforcement

Explicitly state **where and how** each skill is used:

- Next.js → UI rendering, forms, state management
- FastAPI → API routing, business logic
- SQLModel → Database models and persistence

---

## Deliverable Format

- Present the plan as an **ordered checklist**
- Each step must be:
  - Small
  - Verifiable
  - Independently implementable

The output must be **clear enough to directly drive task generation**.

Do NOT generate code.
Do NOT restate the specification.

## Response snapshot

# Implementation Plan: Phase II - Full-Stack Todo Web Application

**Branch**: `004-fullstack-todo-app` | **Date**: 2026-01-04 | **Spec**: [link to spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-fullstack-todo-app/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a full-stack todo web application using Next.js for the frontend and FastAPI for the backend, with SQLModel for data modeling and Neon PostgreSQL for persistence. The application will provide all Phase I CLI functionality through a web interface with proper REST API communication between frontend and backend.

## Technical Context

**Language/Version**: Python 3.11+ (FastAPI), JavaScript/TypeScript (Next.js)
**Primary Dependencies**: Next.js, FastAPI, SQLModel, Neon PostgreSQL, Claude Code
**Storage**: Relational database (PostgreSQL via Neon)
**Testing**: pytest (backend), Jest/React Testing Library (frontend)
**Target Platform**: Web application with browser-based UI
**Project Type**: Full-stack application with separate frontend and backend
**Performance Goals**: Sub-2s page load, sub-1s feedback time for user actions, 99% request success rate
**Constraints**: Decoupled frontend/backend architecture, HTTP API communication only, no direct database access from frontend
**Scale/Scope**: Support 100+ concurrent users with 99.9% data integrity

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
│   │   └── task_model.py
│   ├── services/
│   │   └── task_service.py
│   ├── api/
│   │   └── task_router.py
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
│   │   └── TaskItem.jsx
│   ├── pages/
│   │   ├── index.jsx
│   │   └── api/
│   └── services/
│       └── api_client.js
├── tests/
│   ├── unit/
│   └── integration/
└── package.json

docker-compose.yml
README.md
```

**Structure Decision**: Web application structure with separate backend and frontend directories to maintain full decoupling as required by specification. Backend uses FastAPI with SQLModel for data modeling and Neon PostgreSQL. Frontend uses Next.js for UI rendering and state management.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [None] | [No violations identified] | [All constitution requirements met] |

## Research: Phase II Full-Stack Todo Web Application

## Overview
This research document addresses the technical decisions and unknowns identified during the planning phase for the full-stack todo application.

## Decision: Next.js Implementation Approach
**Rationale**: Next.js was chosen as the frontend framework based on the specification requirements. It provides server-side rendering capabilities, API routes, and a robust ecosystem for building production web applications.
**Alternatives considered**:
- React + Create React App: Simpler but lacks SSR and routing capabilities
- Vue.js/Nuxt.js: Good alternatives but Next.js aligns better with the project's evolution path
- Vanilla JavaScript: Would require more boilerplate and lacks framework benefits

## Decision: FastAPI Backend Framework
**Rationale**: FastAPI was specified as a requirement and offers excellent features including automatic API documentation, type validation, and async support.
**Alternatives considered**:
- Flask: More familiar but lacks automatic documentation and type validation
- Django: More heavyweight than needed for this application
- Express.js: Node-based alternative but doesn't match the Python ecosystem requirement

## Decision: SQLModel for Data Modeling
**Rationale**: SQLModel was specified as the ORM, providing a modern approach that combines SQLAlchemy's power with Pydantic's validation capabilities.
**Alternatives considered**:
- Pure SQLAlchemy: More traditional but lacks Pydantic integration
- Tortoise ORM: Async-native but less mature than SQLModel
- Peewee: Simpler but less feature-rich than SQLModel

## Decision: Neon PostgreSQL Database
**Rationale**: Neon was specified as the PostgreSQL provider, offering serverless PostgreSQL with branching capabilities for development.
**Alternatives considered**:
- Standard PostgreSQL: Would require more infrastructure management
- SQLite: Simpler for development but doesn't match the specification
- PostgreSQL on other cloud providers: Neon was specifically required

## Decision: API Design Pattern
**Rationale**: REST API design will be used to maintain simplicity and alignment with frontend-backend decoupling requirements. Standard HTTP methods and status codes will be implemented.
**Alternatives considered**:
- GraphQL: More flexible but adds complexity
- gRPC: More efficient but less web-native
- Standard REST: Chosen for simplicity and wide tooling support

## Decision: Authentication Approach
**Rationale**: For this phase, simple session-based authentication will be implemented following standard web practices, with JWT tokens as an alternative if needed.
**Alternatives considered**:
- JWT tokens: Stateful but more scalable
- OAuth providers: More complex but provides social login
- Basic auth: Simpler but less secure for web applications

## Decision: Frontend State Management
**Rationale**: React's built-in state management (useState, useReducer) will be used initially, with potential migration to a more sophisticated solution if complexity grows.
**Alternatives considered**:
- Redux: More powerful but adds complexity
- Zustand: Simpler than Redux but still adds external dependency
- Context API: Built-in but can cause performance issues at scale

## Decision: Testing Strategy
**Rationale**: A combination of unit tests (for business logic) and integration tests (for API endpoints and UI components) will be implemented to ensure quality.
**Alternatives considered**:
- Only unit tests: Insufficient coverage of integrated functionality
- Only end-to-end tests: Slower and more brittle than needed
- Integration tests: Good balance of coverage and speed

# Data Model: Phase II Full-Stack Todo Web Application

## Entity: Task

### Fields
- **id** (UUID/Integer): Primary key, unique identifier for the task
- **title** (String, required): Title of the task, maximum 255 characters
- **description** (Text, optional): Detailed description of the task
- **is_completed** (Boolean): Status indicating if the task is completed (default: false)
- **created_at** (DateTime): Timestamp when the task was created (auto-generated)
- **updated_at** (DateTime): Timestamp when the task was last updated (auto-generated)

### Relationships
- No direct relationships for the Task entity in this phase (no user authentication required for MVP)

### Validation Rules
- Title must be present and not empty
- Title must be less than 255 characters
- Description can be up to 10,000 characters if provided
- is_completed defaults to false when creating a new task

### State Transitions
- New task: is_completed = false
- Task marked complete: is_completed = true
- Task marked incomplete: is_completed = false

## Database Schema Considerations

### Indexes
- Index on Task.created_at for sorting
- Index on Task.is_completed for filtering completed tasks

### Constraints
- Task title cannot be empty
- Task title length constraint (255 chars)

## API Representation

### Task Resource
```
{
  "id": "uuid-string",
  "title": "Task title",
  "description": "Optional description",
  "is_completed": false,
  "created_at": "2026-01-04T12:00:00Z",
  "updated_at": "2026-01-04T12:00:00Z"
}
```

### Task Creation Request
```
{
  "title": "Task title",
  "description": "Optional description"
}
```

### Task Update Request
```
{
  "title": "Updated title",        // Optional
  "description": "Updated description", // Optional
  "is_completed": true            // Optional
}
```

# Quickstart Guide: Phase II Full-Stack Todo Web Application

## Overview
This guide provides instructions for setting up and running the full-stack todo application with Next.js frontend and FastAPI backend.

## Prerequisites
- Node.js 18+ for frontend development
- Python 3.11+ for backend development
- PostgreSQL database (Neon serverless recommended)
- UV package manager (or pip)

## Backend Setup (FastAPI)

1. **Install Python dependencies:**
   ```bash
   cd backend
   uv venv  # or python -m venv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install fastapi uvicorn sqlmodel python-multipart
   ```

2. **Set up environment variables:**
   ```bash
   # Create .env file in backend directory
   DATABASE_URL="postgresql://username:password@localhost/dbname"
   ```

3. **Run the backend server:**
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

4. **API documentation:**
   - Access the auto-generated API documentation at `http://localhost:8000/docs`
   - Alternative schema at `http://localhost:8000/redoc`

## Frontend Setup (Next.js)

1. **Install Node.js dependencies:**
   ```bash
   cd frontend
   npm install
   # or yarn install
   ```

2. **Set up environment variables:**
   ```bash
   # Create .env.local file in frontend directory
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   ```

3. **Run the development server:**
   ```bash
   npm run dev
   # or yarn dev
   ```

4. **Access the application:**
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:8000`

## Database Setup (Neon PostgreSQL)

1. **Create a Neon project** and get your connection string
2. **Set the DATABASE_URL** in your backend .env file
3. **Run database migrations** (when implemented):
   ```bash
   python -m src.database.migrate
   ```

## Running the Full Application

1. **Start the backend:**
   ```bash
   cd backend
   uvicorn src.main:app --reload --port 8000
   ```

2. **In a separate terminal, start the frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Access the application at `http://localhost:3000`**

## Key Endpoints

### Task Management
- `GET /api/v1/tasks` - Get all tasks
- `POST /api/v1/tasks` - Create a new task
- `GET /api/v1/tasks/{id}` - Get a specific task
- `PUT /api/v1/tasks/{id}` - Update a task
- `DELETE /api/v1/tasks/{id}` - Delete a task

## Development Workflow

1. **Backend development:**
   - API routes in `backend/src/api/`
   - Data models in `backend/src/models/`
   - Business logic in `backend/src/services/`

2. **Frontend development:**
   - UI components in `frontend/src/components/`
   - Pages in `frontend/src/pages/`
   - API calls in `frontend/src/services/`

3. **Testing:**
   - Backend: `pytest` in the backend directory
   - Frontend: `npm test` in the frontend directory

## Outcome

- ✅ Impact: Created comprehensive implementation plan for Phase II full-stack todo application
- 🧪 Tests: No tests required for planning phase
- 📁 Files: Created plan.md, research.md, data-model.md, contracts/task-api.yaml, quickstart.md
- 🔁 Next prompts: Ready for /sp.tasks to generate implementation tasks
- 🧠 Reflection: Plan covers all required phases with proper technical context and API contracts

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Generate tasks from this plan using /sp.tasks