# Implementation Plan: Phase III AI-Powered Todo Chatbot

**Feature**: AI-Powered Todo Chatbot
**Branch**: 001-ai-chatbot
**Created**: 2026-01-12
**Status**: Draft

## Technical Context

### Known Elements
- **Frontend**: OpenAI ChatKit
- **Backend**: Python FastAPI
- **AI Framework**: OpenAI Agents SDK
- **MCP Server**: Official MCP SDK
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth (JWT-based, from Phase II)
- **LLM Provider**: Cohere API (via OpenAI-compatible interface)
- **Architecture**: Stateless with persistent conversation state
- **Core Functionality**: Natural language todo management (add, list, update, complete, delete)

### Unknown Elements
- Specific Cohere API endpoint configuration for OpenAI-compatible interface
- Exact structure of MCP tool definitions using the Official MCP SDK
- Detailed authentication integration between Better Auth and FastAPI endpoint
- OpenAI ChatKit integration specifics with our backend endpoint
- Database connection pooling and optimization settings for Neon
- Rate limiting and security considerations for AI endpoints

## Constitution Check

### Direct Violations (ERROR if present)
- [x] Manual code writing: No manual coding allowed - Claude Code only ✅
- [x] Future-phase technology: No Docker/Kubernetes/Kafka tech in Phase III ✅
- [x] Phase-specific stack: Using Phase III tech (ChatKit, Agents SDK, MCP) ✅
- [x] Multi-phase repo structure: Maintaining separate branch for Phase III ✅

### Indirect Violations (Review required)
- [x] Specification compliance: Following written spec from feature document ✅
- [x] Clean architecture: Ensuring separation of concerns between components ✅
- [x] Production standards: Maintaining professional quality throughout ✅

### Gate Status: **APPROVED** - All constitutional requirements satisfied

---

## Phase 0: Research & Resolution

### Research Task 1: Cohere API Configuration
**Objective**: Determine how to configure Cohere API as an OpenAI-compatible interface for the Agents SDK
- Research Cohere's OpenAI compatibility layer setup
- Identify required headers, endpoints, and authentication methods
- Document configuration parameters for FastAPI integration

### Research Task 2: MCP SDK Implementation Patterns
**Objective**: Understand the Official MCP SDK patterns for creating stateless tools
- Research official MCP SDK documentation and examples
- Identify patterns for exposing database operations as MCP tools
- Determine best practices for tool registration and error handling

### Research Task 3: Better Auth Integration with FastAPI
**Objective**: Integrate Better Auth JWT verification with FastAPI endpoint
- Research Better Auth's JWT token structure and verification methods
- Determine how to extract user_id from JWT for authorization
- Document security best practices for token validation

### Research Task 4: OpenAI ChatKit Integration
**Objective**: Connect OpenAI ChatKit frontend with our backend
- Research ChatKit configuration and domain allowlisting
- Determine how to pass user authentication to ChatKit
- Document conversation_id persistence mechanisms

---

## Phase 1: Design & Architecture

### Design Task 1: Enhanced Data Model
**Objective**: Extend the existing data model with conversation entities

#### Conversation Entity
- `id`: Primary key (UUID or auto-increment)
- `user_id`: Foreign key linking to user account
- `created_at`: Timestamp of conversation start
- `updated_at`: Timestamp of last activity

#### Message Entity
- `id`: Primary key
- `conversation_id`: Foreign key linking to conversation
- `user_id`: Foreign key for ownership verification
- `role`: Enum (user/assistant/system)
- `content`: Text content of the message
- `created_at`: Timestamp of message creation

#### Relationship Constraints
- Messages belong to one Conversation (many-to-one)
- Both entities enforce user_id for proper ownership
- Indexes on user_id for efficient querying

### Design Task 2: API Contract Definition
**Objective**: Define the API contract for the chat endpoint

#### POST /api/{user_id}/chat
**Headers**:
- `Authorization: Bearer <jwt_token>` - Required for authentication

**Path Parameters**:
- `user_id`: User identifier extracted from JWT (validation required)

**Request Body**:
```json
{
  "conversation_id": "integer (optional)",
  "message": "string (required)"
}
```

**Response Body**:
```json
{
  "conversation_id": "integer",
  "response": "string",
  "tool_calls": "array"
}
```

**Error Responses**:
- 401: Unauthorized (invalid JWT)
- 403: Forbidden (user_id mismatch)
- 404: Conversation not found
- 500: Internal server error

### Design Task 3: MCP Tool Specifications
**Objective**: Define the MCP tools that will be exposed to the AI agent

#### add_task Tool
- **Parameters**: `{user_id: int, title: string, description?: string}`
- **Function**: Creates a new task in the database
- **Returns**: Task object with ID and confirmation

#### list_tasks Tool
- **Parameters**: `{user_id: int, status?: string (all/pending/completed)}`
- **Function**: Retrieves tasks for the user with optional filtering
- **Returns**: Array of task objects

#### complete_task Tool
- **Parameters**: `{user_id: int, task_id: int}`
- **Function**: Updates task completion status
- **Returns**: Updated task object

#### delete_task Tool
- **Parameters**: `{user_id: int, task_id: int}`
- **Function**: Removes task from database
- **Returns**: Confirmation of deletion

#### update_task Tool
- **Parameters**: `{user_id: int, task_id: int, title?: string, description?: string}`
- **Function**: Updates task fields
- **Returns**: Updated task object

### Design Task 4: Stateless Processing Flow
**Objective**: Document the complete request processing flow

1. **Authentication**: Verify JWT token and extract user_id
2. **Validation**: Ensure path user_id matches JWT user_id
3. **Conversation Load**: Fetch conversation history from DB (or create new)
4. **Message Store**: Save incoming user message to DB
5. **Agent Execution**: Run OpenAI Agent with MCP tools and conversation context
6. **Tool Execution**: Execute any MCP tools called by the agent
7. **Response Store**: Save assistant response to DB
8. **Response**: Return formatted response to client

### Design Task 5: Quickstart Documentation
**Objective**: Create setup and run instructions

#### Prerequisites
- Python 3.13+
- PostgreSQL-compatible database (Neon recommended)
- Better Auth configured
- Cohere API key

#### Setup Steps
1. Clone the Phase III branch
2. Install dependencies with `uv pip install`
3. Set environment variables (database URL, API keys, JWT secret)
4. Run database migrations
5. Start the FastAPI server
6. Configure ChatKit frontend with backend endpoint

---

## Phase 2: Implementation Plan

### Implementation Task 1: Project Structure Setup
- Create `/backend` directory with FastAPI application structure
- Create `/frontend` directory with ChatKit configuration
- Set up environment configuration files
- Establish proper directory structure for maintainability

### Implementation Task 2: Database Layer
- Implement SQLModel models for Conversation and Message
- Create database connection utilities
- Implement repository/DAO patterns for data access
- Set up Alembic for database migrations

### Implementation Task 3: MCP Server Implementation
- Create MCP server using the Official MCP SDK
- Implement stateless MCP tools for task operations
- Connect tools to database operations with proper error handling
- Ensure user isolation and authorization in all tools

### Implementation Task 4: Authentication Middleware
- Implement JWT verification using Better Auth
- Create middleware to validate user identity
- Ensure user_id consistency between JWT and request parameters
- Handle authentication errors gracefully

### Implementation Task 5: AI Agent Configuration
- Configure OpenAI Agents SDK with Cohere backend
- Register MCP tools with the agent
- Set up agent instructions for task management
- Implement tool chaining capabilities

### Implementation Task 6: Chat Endpoint Implementation
- Create the main chat endpoint with stateless processing
- Implement conversation history loading and storage
- Integrate agent execution with tool calling
- Format responses appropriately

### Implementation Task 7: Frontend Integration
- Configure OpenAI ChatKit with backend endpoint
- Set up authentication flow with Better Auth
- Handle conversation persistence on frontend
- Ensure responsive and user-friendly interface

### Implementation Task 8: Testing and Validation
- Unit tests for MCP tools
- Integration tests for chat endpoint
- End-to-end tests for complete flow
- Performance and security validation

---

## Architecture Decisions

### Decision: Stateless Server with Persistent State
**Rationale**: Maintains scalability while providing conversation continuity
**Alternative Considered**: Client-side state storage (rejected - poor UX)
**Impact**: Requires database calls on each request but ensures reliability

### Decision: MCP Tools for Database Operations
**Rationale**: Enables AI agents to perform actions safely through defined interfaces
**Alternative Considered**: Direct database access from agent (rejected - security risk)
**Impact**: Adds abstraction layer but improves security and maintainability

### Decision: JWT-Based Authentication
**Rationale**: Leverages existing Better Auth infrastructure from Phase II
**Alternative Considered**: Session cookies (rejected - ChatKit integration complexity)
**Impact**: Maintains consistency with existing auth system

---

## Risk Assessment

### High Risk Items
- **AI Response Quality**: Natural language understanding may not be perfect
  - *Mitigation*: Implement robust error handling and user feedback mechanisms
- **Security**: Potential for unauthorized data access through AI agent
  - *Mitigation*: Strict user isolation in all MCP tools and authentication checks

### Medium Risk Items
- **Performance**: Database operations on each request may impact response time
  - *Mitigation*: Optimize queries and consider caching for frequently accessed data
- **API Compatibility**: Cohere's OpenAI compatibility may have limitations
  - *Mitigation*: Thorough testing and fallback mechanisms if needed

---

## Success Criteria Alignment

This plan addresses all success criteria from the specification:
- Natural language processing for todo operations (✓)
- Conversation continuity across sessions (✓)
- Secure user isolation (✓)
- Performance targets through efficient implementation (✓)
- Accurate task operations through MCP tools (✓)