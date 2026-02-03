# Research Document: Phase III AI Chatbot Implementation

**Feature**: AI-Powered Todo Chatbot
**Branch**: 001-ai-chatbot
**Created**: 2026-01-12

## Research Task 1: Cohere API Configuration

### Decision: Configure Cohere with OpenAI-Compatible Interface
**Rationale**: Cohere offers an OpenAI-compatible API endpoint that allows us to use the OpenAI Agents SDK with Cohere's models.

**Implementation Approach**:
- Use Cohere's `/v1/chat/completions` endpoint which mimics OpenAI's format
- Set base URL to `https://api.cohere.ai/v1` instead of OpenAI's default
- Use Cohere API key instead of OpenAI API key
- Specify Cohere model (e.g., `command-r-plus`) in the model parameter

**Configuration Parameters**:
```python
import openai

openai.base_url = "https://api.cohere.ai/v1/"
openai.api_key = os.getenv("COHERE_API_KEY")
```

**Alternatives Considered**:
- Direct Cohere SDK: Would require different implementation than OpenAI Agents SDK
- Custom proxy: Would add complexity and maintenance overhead

### Decision: Agent Configuration for Cohere
**Rationale**: Need to properly configure the OpenAI Agent to work with Cohere's API.

**Implementation Approach**:
- Use `openai.beta.threads.runs.create` with Cohere-compatible parameters
- Map Cohere's response format to expected OpenAI format
- Handle any differences in response structure between providers

## Research Task 2: MCP SDK Implementation Patterns

### Decision: Implement MCP Tools Using Official SDK
**Rationale**: The Official MCP SDK provides the correct patterns for creating tools that can be consumed by AI agents.

**Implementation Approach**:
- Create an MCP server that exposes tool definitions
- Use JSON-RPC protocol as specified by MCP specification
- Define tools with proper typing and documentation
- Implement stateless operations that connect to database

**Structure Example**:
```python
from mcp.server import Server
from mcp.types import Tool, ToolCall, TextContent

# Define MCP tools that map to database operations
def create_mcp_tools():
    # add_task, list_tasks, etc. as MCP tools
    pass
```

**Alternatives Considered**:
- Custom RPC mechanism: Would not be compatible with standard tools
- Direct function calling: Would not follow MCP specification

## Research Task 3: Better Auth Integration with FastAPI

### Decision: JWT Token Verification Middleware
**Rationale**: Need to validate JWT tokens from Better Auth and extract user identity.

**Implementation Approach**:
- Use Python-JOSE or similar library to decode JWT tokens
- Extract user_id from the token payload
- Compare the extracted user_id with the route parameter
- Return 403 if they don't match

**Implementation Pattern**:
```python
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status

def verify_token(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

**Alternatives Considered**:
- Session-based authentication: Would complicate ChatKit integration
- API keys per request: Would require additional key management

## Research Task 4: OpenAI ChatKit Integration

### Decision: Backend Endpoint with CORS Configuration
**Rationale**: ChatKit needs to communicate with our backend securely.

**Implementation Approach**:
- Configure CORS middleware to allow ChatKit domains
- Implement proper authentication flow
- Handle conversation_id persistence through frontend state management
- Use WebSocket or Server-Sent Events for real-time updates if needed

**Configuration**:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chat.openai.com"],  # Or configured domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Alternatives Considered**:
- Direct database access from frontend: Would compromise security
- Separate auth service: Would add unnecessary complexity

## Additional Technical Considerations

### Database Connection Optimization
- Use connection pooling with SQLModel/SQLAlchemy
- Implement proper indexing on user_id and foreign keys
- Consider read replicas for heavy read operations

### Error Handling Strategy
- Implement graceful degradation when AI services are unavailable
- Provide helpful error messages to users
- Log errors appropriately for debugging

### Security Measures
- Input validation for all user-provided content
- Rate limiting to prevent abuse
- Sanitize all data before storing or displaying