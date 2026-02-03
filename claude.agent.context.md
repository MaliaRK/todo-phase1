# Evolution of Todo - Phase III Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-01-12

## Active Technologies

- Python 3.13+ (Backend development)
- FastAPI (Web framework)
- SQLModel (ORM and database modeling)
- Neon PostgreSQL (Database)
- OpenAI Agents SDK (AI agent framework)
- Official MCP SDK (Model Context Protocol)
- Cohere API (Language model via OpenAI-compatible interface)
- OpenAI ChatKit (Frontend chat interface)
- Better Auth (JWT-based authentication)
- uv (Python package manager)

## Project Structure

```text
backend/
├── main.py                 # FastAPI application entry point
├── models/                 # SQLModel database models
│   ├── __init__.py
│   ├── task.py             # Task entity model
│   ├── conversation.py     # Conversation entity model
│   └── message.py          # Message entity model
├── api/                    # API endpoints
│   ├── __init__.py
│   └── chat.py             # Chat endpoint implementation
├── mcp/                    # MCP server implementation
│   ├── __init__.py
│   └── server.py           # MCP tools and server
├── agents/                 # AI agent configuration
│   ├── __init__.py
│   └── config.py           # Agent setup and tools
├── auth/                   # Authentication utilities
│   ├── __init__.py
│   └── middleware.py       # JWT validation
└── database/               # Database utilities
    ├── __init__.py
    └── session.py          # Session management

frontend/
├── package.json            # Frontend dependencies
├── chatkit-config.js       # ChatKit configuration
└── public/                 # Static assets

specs/001-ai-chatbot/       # Phase III specifications
├── spec.md                 # Feature specification
├── plan.md                 # Implementation plan
├── research.md             # Research findings
├── data-model.md           # Data model documentation
├── quickstart.md           # Quickstart guide
├── contracts/              # API contracts
│   └── chat-api.yaml       # OpenAPI specification
└── checklists/             # Quality checklists
    └── requirements.md
```

## Commands

### Backend Development
```bash
# Activate environment
uv venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows

# Install dependencies
uv pip install -r requirements.txt

# Run development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Run tests
python -m pytest tests/
```

### Database Management
```bash
# Create database tables (if not using Alembic)
python create_tables.py

# With Alembic migrations
alembic revision --autogenerate -m "Create conversation and message tables"
alembic upgrade head
```

### Environment Setup
```bash
# Set required environment variables
export DATABASE_URL="postgresql://..."
export COHERE_API_KEY="..."
export BETTER_AUTH_SECRET="..."
```

## Code Style

### Python
- Follow PEP 8 style guide
- Use type hints for all function signatures
- Import order: standard library, third-party, local
- Maximum line length: 88 characters
- Use f-strings for string formatting
- Prefer early returns to deep nesting

### FastAPI
- Use Pydantic models for request/response validation
- Implement proper error handling with HTTPException
- Use dependency injection for shared functionality
- Document API endpoints with proper descriptions

### SQLModel
- Define models with proper relationships
- Use TypedDict for complex return types
- Implement proper foreign key constraints
- Use async session for database operations

## Recent Changes

### Phase III: AI-Powered Todo Chatbot
- Added MCP server with tools for task operations
- Implemented stateless AI agent with conversation persistence
- Integrated Cohere API via OpenAI-compatible interface
- Created conversation and message data models

### Phase II: Full-Stack Web App
- Implemented Next.js frontend with FastAPI backend
- Added SQLModel for database operations
- Integrated Better Auth for authentication
- Connected to Neon PostgreSQL database

### Phase I: CLI Todo App
- Created basic in-memory todo application
- Implemented core CRUD operations
- Added JSON persistence
- Built with Python 3.13+ and uv package manager

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->