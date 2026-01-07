---
name: sqlmodel-builder
description: |
  This skill should be used when users need to create SQLModel artifacts including models, database operations, relationships, and FastAPI integrations.
  It provides guidance on SQLModel best practices, combining SQLAlchemy and Pydantic features for production-ready applications.
---

# SQLModel Builder Skill

Build production-ready SQLModel applications with proper patterns, best practices, and security considerations.

## When to Use This Skill

Use this skill when users need to create:
- SQLModel models that serve as both database models and Pydantic schemas
- Database relationships and foreign key constraints
- Query operations using SQLModel's select statements
- FastAPI integration with SQLModel models
- Database session management and transactions
- Model validation and serialization patterns

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing SQLModel structure, database schema, and model relationships |
| **Conversation** | User's specific requirements, model fields, relationships, validation needs |
| **Skill References** | SQLModel patterns from `references/` (models, queries, relationships) |
| **User Guidelines** | Project-specific conventions, team standards, and existing patterns |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (SQLModel expertise is in this skill).

## Core SQLModel Concepts

### Model Definition
- Inherit from SQLModel with `table=True` to create database tables
- Use type hints for automatic validation and database column types
- Combine Pydantic validation with SQLAlchemy database features
- Use Optional for nullable fields

### Field Configuration
- Use Field() for database-specific configurations (index, foreign_key, etc.)
- Use Field() for Pydantic validation constraints
- Combine database and validation properties in single Field() calls

### Relationships
- Use Relationship() for defining relationships between models
- Implement proper back_populates for bidirectional relationships
- Handle relationship loading strategies appropriately

## Implementation Patterns

### Model Creation Pattern
```
1. Define class inheriting from SQLModel with table=True
2. Add primary key field (typically Optional[int] with default=None and primary_key=True)
3. Add required fields with appropriate types
4. Add optional fields with Optional[] type hints
5. Configure database properties with Field() when needed
6. Add Pydantic validation with Field() constraints
```

### Relationship Implementation Pattern
```
1. Define foreign key field with Field(foreign_key=...)
2. Create Relationship attribute with back_populates
3. Handle bidirectional relationships properly
4. Consider relationship loading strategies (lazy/eager)
5. Implement proper cascade options if needed
6. Add proper typing with List for one-to-many relationships
```

### Query Implementation Pattern
```
1. Use select() statements from sqlmodel for queries
2. Implement proper session management
3. Use parameterized queries to prevent SQL injection
4. Handle query results appropriately
5. Implement proper error handling
6. Use transactions for complex operations
```

## Quality Standards

### Performance
- Use proper indexing with Field(index=True)
- Implement efficient queries with select statements
- Consider relationship loading strategies
- Use transactions for multiple related operations

### Validation
- Use type hints for automatic validation
- Implement custom validators when needed
- Use Field() constraints for validation
- Validate foreign key relationships

### Security
- Use parameterized queries to prevent SQL injection
- Validate all inputs through model validation
- Implement proper authentication for database access
- Sanitize sensitive data in logs

## SQLModel Best Practices

### Model Design
- Use descriptive field names
- Follow naming conventions for tables and columns
- Use Optional for nullable fields
- Implement proper default values

### Database Operations
- Use dependency injection for database sessions
- Implement proper transaction management
- Handle database errors appropriately
- Use connection pooling for performance

### FastAPI Integration
- Use same models for request/response validation
- Implement proper error handling
- Use dependency injection for database access
- Follow RESTful API design principles

## Common SQLModel Patterns

### Basic Model Pattern
```python
# models/user.py
from sqlmodel import SQLModel, Field
from typing import Optional

class UserBase(SQLModel):
    email: str = Field(index=True, unique=True)
    username: str = Field(index=True, min_length=3, max_length=50)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str = Field(max_length=255)
    is_active: bool = Field(default=True)
```

### Relationship Pattern
```python
# models/team.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=100)
    headquarters: str

    # Relationship to heroes
    heroes: List["Hero"] = Relationship(back_populates="team")

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, ge=0, le=150)

    # Foreign key to team
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    team: Optional[Team] = Relationship(back_populates="heroes")
```

### Query Pattern
```python
# crud/user.py
from sqlmodel import Session, select
from models.user import User

def get_user_by_email(session: Session, email: str) -> User:
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()

def create_user(session: Session, user: User) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_users(session: Session, skip: int = 0, limit: int = 100) -> List[User]:
    statement = select(User).offset(skip).limit(limit)
    return session.exec(statement).all()
```

## Checklist for SQLModel Artifacts

### Models
- [ ] Proper inheritance from SQLModel with table=True if needed
- [ ] Primary key field properly defined
- [ ] Type hints for all fields
- [ ] Optional types for nullable fields
- [ ] Field() configurations for database properties
- [ ] Validation constraints implemented

### Relationships
- [ ] Foreign key fields properly defined
- [ ] Relationship attributes with back_populates
- [ ] Proper typing for relationship fields
- [ ] Bidirectional relationships handled correctly
- [ ] Cascade options configured if needed
- [ ] Loading strategies considered

### Queries
- [ ] Use select statements instead of raw SQL
- [ ] Proper session management
- [ ] Parameterized queries for security
- [ ] Proper error handling
- [ ] Transactions for complex operations
- [ ] Efficient query patterns

## Troubleshooting Common Issues

### Model Creation Issues
- Check proper inheritance from SQLModel
- Verify table=True for database tables
- Confirm field type hints are correct
- Ensure Field() configurations are valid

### Relationship Issues
- Verify foreign key field types match referenced table
- Check back_populates references exist
- Confirm relationship attribute names
- Ensure proper typing for relationship fields

### Query Issues
- Check session management patterns
- Verify select statement syntax
- Confirm transaction handling
- Ensure proper error handling