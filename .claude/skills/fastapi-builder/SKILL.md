---
name: fastapi-builder
description: |
  This skill should be used when users need to create FastAPI artifacts including applications, endpoints, models, dependencies, and configurations.
  It provides guidance on FastAPI best practices, security patterns, and implementation patterns for production-ready APIs.
---

# FastAPI Builder Skill

Build production-ready FastAPI applications with proper patterns, best practices, and security considerations.

## When to Use This Skill

Use this skill when users need to create:
- FastAPI application instances with proper configuration
- API endpoints with request/response validation
- Pydantic models for data validation and serialization
- Dependency injection systems
- Authentication and authorization systems
- Database integration patterns
- Background tasks and event handlers
- API documentation and testing patterns

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing FastAPI structure, patterns, database models, and configuration files |
| **Conversation** | User's specific requirements, endpoint types, data models, authentication needs |
| **Skill References** | FastAPI patterns from `references/` (routing, validation, security) |
| **User Guidelines** | Project-specific conventions, team standards, and existing patterns |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (FastAPI expertise is in this skill).

## Core FastAPI Concepts

### Type Hints and Validation
- Pydantic models for request/response validation
- Automatic serialization and deserialization
- Type hints for automatic documentation and validation
- Field constraints and validators

### Dependency Injection
- Shared dependencies for authentication, database sessions
- Sub-dependencies for complex logic
- Security dependencies with OAuth2, API keys
- Async dependencies for async operations

### ASGI and Async Support
- Built-in async/await support
- Non-blocking I/O operations
- Background tasks
- WebSocket support

## Implementation Patterns

### Application Creation Pattern
```
1. Create FastAPI instance with proper configuration
2. Configure CORS and other middleware
3. Set up exception handlers
4. Include API routers with proper prefixes
5. Add event handlers for startup/shutdown
6. Configure custom settings and logging
```

### Endpoint Creation Pattern
```
1. Define Pydantic models for request/response
2. Create endpoint function with proper type hints
3. Implement dependency injection
4. Add proper status codes and responses
5. Include validation error handling
6. Document parameters and responses
```

### Model Creation Pattern
```
1. Create Pydantic model with appropriate fields
2. Add field constraints and validation
3. Implement custom validators if needed
4. Define response models for serialization
5. Add proper documentation for fields
6. Consider using ConfigDict for settings
```

## Quality Standards

### Performance
- Use async/await for I/O operations
- Implement proper database connection pooling
- Use background tasks for non-critical operations
- Optimize database queries with proper indexing

### Security
- Validate all inputs through Pydantic models
- Implement proper authentication and authorization
- Use HTTPS in production
- Sanitize sensitive data in logs

### Documentation
- Use descriptive docstrings
- Implement proper OpenAPI schemas
- Include example requests/responses
- Add proper tags for organization

## FastAPI Best Practices

### Application Structure
- Use APIRouter for modular endpoints
- Separate concerns with different files
- Use consistent naming conventions
- Organize dependencies separately

### Error Handling
- Use HTTPException for client errors
- Implement custom exception handlers
- Return appropriate status codes
- Provide meaningful error messages

### Database Integration
- Use dependency injection for database sessions
- Implement proper transaction management
- Follow repository pattern for data access
- Use connection pooling for performance

## Common FastAPI Patterns

### Application Factory Pattern
```python
# main.py
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

def create_app() -> FastAPI:
    app = FastAPI(
        title="My API",
        description="My API description",
        version="1.0.0",
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
```

### Dependency Injection Pattern
```python
# dependencies.py
from fastapi import Depends, HTTPException, status
from typing import Optional

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user
```

### Pydantic Model Pattern
```python
# models.py
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: str = Field(..., example="user@example.com", description="User's email address")
    username: str = Field(..., min_length=3, max_length=50, example="johndoe")
    password: str = Field(..., min_length=8, example="secretpassword")

    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email')
        return v

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime

    class Config:
        from_attributes = True  # For ORM compatibility
```

## Checklist for FastAPI Artifacts

### Endpoints
- [ ] Proper Pydantic request/response models
- [ ] Appropriate status codes
- [ ] Dependency injection implemented
- [ ] Error handling with HTTPException
- [ ] Type hints for all parameters
- [ ] Proper documentation strings

### Models
- [ ] Field constraints and validation
- [ ] Config for ORM compatibility if needed
- [ ] Custom validators if required
- [ ] Proper documentation for fields
- [ ] Example values provided
- [ ] Appropriate field types

### Dependencies
- [ ] Proper error handling in dependencies
- [ ] Async implementation when needed
- [ ] Resource cleanup (e.g., database sessions)
- [ ] Security considerations implemented
- [ ] Sub-dependencies if complex
- [ ] Proper typing for return values

## Troubleshooting Common Issues

### Validation Errors
- Check Pydantic model field types
- Verify field constraints and validators
- Ensure proper serialization settings
- Confirm Config settings for ORM compatibility

### Dependency Issues
- Verify dependency function signatures
- Check for async/await consistency
- Ensure proper error handling in dependencies
- Confirm dependency return types

### Performance Issues
- Check for blocking operations in async functions
- Verify database connection pooling
- Review query optimization
- Confirm background task usage for non-critical operations