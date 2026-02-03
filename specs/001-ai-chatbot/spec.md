# Feature Specification: AI-Powered Todo Chatbot

**Feature Branch**: `001-ai-chatbot`
**Created**: 2026-01-12
**Status**: Draft
**Input**: User description: "Phase III (Todo AI Chatbot)
# sp.specify — Phase III: Todo AI Chatbot (MCP + Agents)

## Context
We have a single Git repository containing multiple phases of the \"Evolution of Todo\" project, organized using branches:
- Phase I: CLI Todo App
- Phase II: Full-Stack Web App (Next.js + FastAPI + SQLModel + Neon + Better Auth)

This specification applies ONLY to the Phase III branch and must build on top of Phase II without breaking or rewriting it.

## Objective
Define a complete, spec-driven architecture for **Phase III**, introducing an **AI-powered conversational chatbot** that manages todos through natural language using:
- OpenAI Agents SDK
- Official MCP (Model Context Protocol) SDK
- OpenAI ChatKit frontend
- Stateless FastAPI backend
- Persistent conversation state stored in Neon PostgreSQL

No manual coding is allowed. All implementation must be generated via Claude Code using Spec-Kit Plus.

---

## Core Requirements

### Conversational AI Interface
- Users must manage todos using natural language
- The chatbot must support all **Basic Level Todo features**:
  - Add task
  - List tasks
  - Update task
  - Complete task
  - Delete task

### Stateless Architecture
- FastAPI server must remain stateless
- Conversation state must be persisted in the database
- Every request must fully reconstruct context from stored messages

---

## Technology Stack

| Component | Technology |
|---------|------------|
| Frontend | OpenAI ChatKit |
| Backend | Python FastAPI |
| AI Framework | OpenAI Agents SDK |
| MCP Server | Official MCP SDK |
| ORM | SQLModel |
| Database | Neon Serverless PostgreSQL |
| Authentication | Better Auth (JWT-based, from Phase II) |
| LLM Provider | Cohere API (via OpenAI-compatible interface) |

---

## High-Level Architecture

- ChatKit UI sends user messages
- FastAPI exposes a single stateless chat endpoint
- OpenAI Agent processes user intent
- MCP server exposes task operations as tools
- Agent invokes MCP tools
- MCP tools interact with database via SQLModel
- All conversation messages are stored in the database
- Server holds no in-memory state between requests

---

## Database Models

### Task
- user_id
- id
- title
- description
- completed
- created_at
- updated_at

### Conversation
- user_id
- id
- created_at
- updated_at

### Message
- user_id
- id
- conversation_id
- role (user / assistant)
- content
- created_at

---

## Chat API Specification

### Endpoint


POST /api/{user_id}/chat


### Request
| Field | Type | Required | Description |
|-----|-----|---------|-------------|
| conversation_id | integer | No | Existing conversation ID (new if absent) |
| message | string | Yes | User's natural language input |

### Response
| Field | Type | Description |
|-----|-----|-------------|
| conversation_id | integer | Active conversation ID |
| response | string | AI assistant reply |
| tool_calls | array | MCP tools invoked |

---

## MCP Tool Specifications

The MCP server must expose the following **stateless tools**:

### add_task
- Parameters: user_id (required), title (required), description (optional)
- Creates a task in the database

### list_tasks
- Parameters: user_id (required), status (optional: all/pending/completed)
- Returns filtered task list

### complete_task
- Parameters: user_id (required), task_id (required)
- Marks task as completed

### delete_task
- Parameters: user_id (required), task_id (required)
- Deletes a task

### update_task
- Parameters: user_id (required), task_id (required), title/description (optional)
- Updates task fields

All MCP tools:
- Must NOT store state in memory
- Must persist all changes directly to the database
- Must enforce user ownership

---

## Agent Behavior Specification

The AI agent must:
- Interpret natural language intent
- Select appropriate MCP tool(s)
- Chain tools when required (e.g., list → delete)
- Confirm actions with friendly responses
- Handle errors gracefully (task not found, invalid input)

---

## Stateless Conversation Flow

1. Receive user message
2. Fetch conversation history from database
3. Append new message
4. Store user message
5. Run agent with MCP tools
6. Execute tool calls
7. Store assistant response
8. Return response
9. Discard all in-memory state

---

## Authentication & Security
- All requests require valid JWT (Better Auth)
- User identity der"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Natural Language Todo Management (Priority: P1)

A user wants to manage their todos using natural language instead of clicking buttons or filling forms. They can speak or type in everyday language like "Add a task to buy groceries" or "Mark my meeting as completed".

**Why this priority**: This is the core value proposition of the AI chatbot - allowing users to interact with their todo list naturally without learning specific commands.

**Independent Test**: Can be fully tested by sending natural language messages to the chatbot and verifying that appropriate todo actions are performed, delivering the convenience of voice/command-free todo management.

**Acceptance Scenarios**:

1. **Given** a user wants to add a new task, **When** they say "Add a task to buy milk", **Then** a new todo item titled "buy milk" is created in their list
2. **Given** a user wants to view their tasks, **When** they say "Show me my tasks", **Then** they receive a list of their current todo items
3. **Given** a user wants to complete a task, **When** they say "Complete task number 1", **Then** the first task in their list is marked as completed

---

### User Story 2 - Conversation Continuity (Priority: P2)

A user continues a conversation with the chatbot across multiple interactions, expecting the system to remember the context of their previous exchanges within the same conversation.

**Why this priority**: Users expect conversational continuity to have natural-feeling interactions with the AI assistant.

**Independent Test**: Can be fully tested by maintaining a conversation thread and verifying that the AI remembers context from previous messages within the same session.

**Acceptance Scenarios**:

1. **Given** a user has an ongoing conversation, **When** they send a follow-up message, **Then** the AI responds considering the context of previous messages
2. **Given** a user refers to a previously mentioned task, **When** they say "update that task", **Then** the AI correctly identifies which task they're referring to based on conversation history

---

### User Story 3 - Secure Access and User Isolation (Priority: P1)

A user accesses their todo list through the chatbot while being assured that their data remains private and isolated from other users.

**Why this priority**: Security and privacy are fundamental requirements for any system handling personal data.

**Independent Test**: Can be fully tested by verifying that users can only access their own data and authentication is properly enforced.

**Acceptance Scenarios**:

1. **Given** a user is authenticated, **When** they request their tasks, **Then** they only see tasks associated with their account
2. **Given** an unauthenticated user attempts access, **When** they try to interact with the system, **Then** they are denied access

---

### User Story 4 - Task Operations via Natural Language (Priority: P3)

A user performs advanced todo operations like updating task details, deleting specific tasks, or filtering their task list using natural language commands.

**Why this priority**: While basic operations are covered in P1, advanced operations enhance the usability and completeness of the system.

**Independent Test**: Can be fully tested by sending various natural language commands for different operations and verifying correct execution.

**Acceptance Scenarios**:

1. **Given** a user wants to update a task, **When** they say "Change task 1 to 'Buy organic milk'", **Then** the task title is updated appropriately
2. **Given** a user wants to delete a task, **When** they say "Remove my grocery task", **Then** the specified task is deleted from their list

---

### Edge Cases

- What happens when a user's natural language command is ambiguous and could refer to multiple tasks?
- How does the system handle requests for non-existent tasks or conversations?
- What happens when the AI misinterprets user intent and performs an incorrect operation?
- How does the system handle very long conversations that might impact performance?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST follow written specifications as defined in this document
- **FR-002**: System MUST be generated by Claude Code (no manual code writing allowed)
- **FR-003**: Users MUST be able to add, view, update, delete, and mark tasks as complete/incomplete through natural language
- **FR-004**: System MUST maintain clean architecture and separation of concerns
- **FR-005**: System MUST use the technology stack appropriate for the current phase (OpenAI Agents SDK, MCP SDK, FastAPI, SQLModel, Neon PostgreSQL)
- **FR-006**: System MUST not introduce future-phase technologies prematurely
- **FR-007**: System MUST place source code in appropriate directory structure with modular logic
- **FR-008**: System MUST provide appropriate user interface based on phase requirements (using OpenAI ChatKit frontend)
- **FR-009**: System MUST avoid global mutable state leakage
- **FR-010**: System MUST be developed with Product Architect approach using specification-driven methodology
- **FR-011**: System MUST maintain professional quality standards across all phases
- **FR-012**: System MUST maintain statelessness of the FastAPI backend service
- **FR-013**: System MUST persist all conversation data in the database to maintain continuity
- **FR-014**: System MUST authenticate all requests using JWT tokens from Better Auth
- **FR-015**: System MUST ensure users can only access their own data and tasks
- **FR-016**: System MUST interpret natural language input and map to appropriate todo operations
- **FR-017**: System MUST expose MCP tools for all required todo operations (add, list, update, complete, delete)
- **FR-018**: System MUST maintain conversation history for context awareness
- **FR-019**: System MUST handle errors gracefully when tasks or conversations don't exist
- **FR-020**: System MUST return appropriate responses that confirm actions taken or explain errors

### Key Entities *(include if feature involves data)*

- **Task**: Represents a single todo item with properties like title, description, completion status, and timestamps
- **Conversation**: Represents a session of interaction between a user and the AI assistant with metadata
- **Message**: Represents individual exchanges within a conversation with role (user/assistant) and content

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can successfully add, list, update, complete, and delete tasks using natural language with 95% accuracy
- **SC-002**: System maintains conversation context and continuity across multiple exchanges within the same session
- **SC-003**: 90% of user requests result in appropriate task operations without requiring clarification
- **SC-004**: System responds to user queries within 3 seconds for 95% of requests
- **SC-005**: Users report high satisfaction with the natural language interface compared to traditional UI controls
- **SC-006**: System securely isolates user data with 100% success rate - users cannot access others' tasks
- **SC-007**: Authentication is successful for 99.9% of valid requests while blocking unauthorized access
- **SC-008**: Conversation state persists correctly between requests with no data loss