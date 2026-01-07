# SQLModel Models Guide

## Basic Model Definition

SQLModel combines SQLAlchemy and Pydantic in a single class:

```python
from sqlmodel import SQLModel, Field
from typing import Optional

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, ge=0, le=150)
```

## Field Configuration

### Primary Keys
```python
class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # Alternative for auto-incrementing primary keys
    # id: int = Field(primary_key=True, default=None)
```

### Indexes and Constraints
```python
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True, max_length=255)
    username: str = Field(index=True, min_length=3, max_length=50)
    age: Optional[int] = Field(default=None, ge=0, le=150)
    rating: float = Field(gt=0, le=10)
```

### Default Values
```python
from datetime import datetime
from sqlalchemy import text

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_published: bool = Field(default=False)
    views: int = Field(default=0)
```

## Model Inheritance

### Shared Base Models
```python
from sqlmodel import SQLModel, Field
from typing import Optional

class TimestampMixin(SQLModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None)

class Hero(HeroBase, TimestampMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    power: int = Field(default=0, ge=0, le=100)
```

### Abstract Base Models
```python
class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str

class Hero(HeroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    age: Optional[int] = Field(default=None)

class Enemy(HeroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    threat_level: int = Field(default=1, ge=1, le=10)
```

## Validation with Field Constraints

### String Constraints
```python
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    username: str = Field(min_length=3, max_length=50, regex=r'^[a-zA-Z0-9_]+$')
    bio: Optional[str] = Field(default=None, max_length=500)
```

### Numeric Constraints
```python
class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float = Field(gt=0)  # Greater than 0
    discount: float = Field(ge=0, le=1)  # Between 0 and 1
    quantity: int = Field(ge=0)  # Greater than or equal to 0
    rating: float = Field(ge=0, le=5)  # Between 0 and 5
```

## Using Pydantic Validators

### Custom Validators
```python
from pydantic import field_validator

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None)

    @field_validator('name')
    def validate_name(cls, v):
        if len(v) < 2:
            raise ValueError('Name must be at least 2 characters long')
        if not v.replace(' ', '').isalpha():
            raise ValueError('Name must contain only letters and spaces')
        return v.title()  # Capitalize first letter of each word

    @field_validator('secret_name')
    def validate_secret_name(cls, v):
        if len(v) < 3:
            raise ValueError('Secret name must be at least 3 characters long')
        return v
```

## Model Configuration

### Custom Table Names
```python
class Hero(SQLModel, table=True):
    __tablename__ = "heroes"  # Custom table name

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
```

### Model Config
```python
class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str

    class Config:
        # Pydantic configuration options
        extra = "forbid"  # Forbid extra fields
        # Other options: "ignore", "allow"
```

## Model Usage Patterns

### Creating Instances
```python
# Valid instance creation
hero = Hero(name="Spider-Boy", secret_name="Pedro Parqueador", age=16)

# From dictionary
hero_dict = {
    "name": "Spider-Boy",
    "secret_name": "Pedro Parqueador",
    "age": 16
}
hero = Hero.model_validate(hero_dict)

# From JSON
json_str = '{"name": "Spider-Boy", "secret_name": "Pedro Parqueador", "age": 16}'
hero = Hero.model_validate_json(json_str)
```

### Serialization
```python
hero = Hero(name="Spider-Boy", secret_name="Pedro Parqueador", age=16)

# To dictionary
hero_dict = hero.model_dump()

# To JSON
json_str = hero.model_dump_json()

# Exclude fields
hero_dict = hero.model_dump(exclude={'id'})
```

## Model Relationships (Preview)

While relationships are covered in detail in the relationships guide, here's a simple example:

```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    # Relationship to heroes
    heroes: List["Hero"] = Relationship(back_populates="team")

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None)

    # Foreign key to team
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    team: Optional[Team] = Relationship(back_populates="heroes")
```