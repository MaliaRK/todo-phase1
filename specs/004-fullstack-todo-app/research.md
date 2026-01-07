# Research: Phase II Full-Stack Todo Web Application with Authentication Extension

## Overview
This research document addresses the technical decisions and unknowns identified during the planning phase for the full-stack todo application with authentication extension.

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

## Decision: Better Auth with JWT for Authentication
**Rationale**: Better Auth provides a comprehensive authentication solution that includes JWT support, session management, and user registration/login flows. It integrates well with Next.js and can be configured to work with FastAPI backend. The JWT plugin enables the specific requirements from the specification: including user_id, email, iat, and exp claims in the token.

**Alternatives considered**:
- Custom JWT Implementation: More complex, requires handling token generation, validation, and storage manually
- Auth.js: Would require more configuration for JWT support
- NextAuth.js: More focused on OAuth, JWT support requires additional configuration
- Better Auth: Chosen for its built-in JWT plugin and comprehensive auth features

## Technical Implementation Details for Authentication:

### Frontend (Next.js) Research:
- Better Auth client SDK provides hooks for authentication state management
- JWT plugin enables JWT token generation and management
- Session cookies can be configured with HttpOnly, Secure, and SameSite=Lax flags
- Client-side API calls can access the JWT token for backend communication

### Backend (FastAPI) Research:
- JWT verification can be implemented as a dependency using python-jose or similar libraries
- Better Auth uses HS256 algorithm for JWT signing
- Token validation requires the same secret key used for signing (BETTER_AUTH_SECRET)
- User ID extraction from JWT payload for authorization enforcement

### API Integration Research:
- Existing API routes can remain unchanged, with authentication enforced as a dependency
- Authorization header format: `Authorization: Bearer <JWT_TOKEN>`
- 401 Unauthorized responses for missing/invalid tokens
- User ID validation to ensure JWT user_id matches route parameter

## Architecture Patterns for Authentication:
- Frontend: Next.js App Router with Better Auth integration
- Backend: FastAPI dependency injection for JWT validation
- Security: HttpOnly cookies for session storage, Bearer tokens for API communication
- Data Isolation: Database queries filtered by authenticated user_id

## Dependencies to Install:
- Frontend: `better-auth`, JWT plugin
- Backend: `python-jose`, `cryptography` for JWT verification