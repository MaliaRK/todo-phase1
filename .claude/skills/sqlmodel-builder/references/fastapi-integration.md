# SQLModel FastAPI Integration Guide

## Basic Integration

### Database Setup
```python
# database.py
from sqlmodel import create_engine, Session
from typing import Generator
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

engine = create_engine(DATABASE_URL, echo=True)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
```

### Main Application
```python
# main.py
from fastapi import FastAPI, Depends
from sqlmodel import Session
from database import get_session
from routers import heroes, teams

app = FastAPI(title="SQLModel API")

app.include_router(heroes.router)
app.include_router(teams.router)

@app.get("/")
def read_root():
    return {"message": "SQLModel API"}
```

## CRUD Operations with FastAPI

### Creating Records
```python
# routers/heroes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models.hero import Hero, HeroCreate, HeroUpdate

router = APIRouter(prefix="/heroes", tags=["heroes"])

@router.post("/", response_model=Hero)
def create_hero(hero: HeroCreate, session: Session = Depends(get_session)):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero
```

### Reading Records
```python
@router.get("/", response_model=List[Hero])
def read_heroes(
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = 100
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes

@router.get("/{hero_id}", response_model=Hero)
def read_hero(hero_id: int, session: Session = Depends(get_session)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero
```

### Updating Records
```python
@router.put("/{hero_id}", response_model=Hero)
def update_hero(
    hero_id: int,
    hero_update: HeroUpdate,
    session: Session = Depends(get_session)
):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    update_data = hero_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(hero, key, value)

    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero
```

### Deleting Records
```python
@router.delete("/{hero_id}")
def delete_hero(hero_id: int, session: Session = Depends(get_session)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    session.delete(hero)
    session.commit()
    return {"message": "Hero deleted successfully"}
```

## Advanced Integration Patterns

### Using Different Models for Input/Output

#### Request Models
```python
# models/requests.py
from sqlmodel import SQLModel
from typing import Optional

class HeroCreate(SQLModel):
    name: str
    secret_name: str
    age: Optional[int] = None
    team_id: Optional[int] = None

class HeroUpdate(SQLModel):
    name: Optional[str] = None
    secret_name: Optional[str] = None
    age: Optional[int] = None
    team_id: Optional[int] = None

class HeroUpdatePublic(HeroUpdate):
    # Only allow updating public fields
    name: Optional[str] = None
    age: Optional[int] = None
```

#### Response Models
```python
# models/responses.py
from sqlmodel import SQLModel
from typing import Optional

class HeroPublic(SQLModel):
    id: int
    name: str
    age: Optional[int] = None

class HeroPrivate(HeroPublic):
    secret_name: str
    team_id: Optional[int] = None
```

### Relationship Handling in APIs

#### Including Related Data
```python
from typing import Optional
from models.team import Team

class HeroWithTeam(Hero):
    team: Optional[Team] = None

@router.get("/{hero_id}/with-team", response_model=HeroWithTeam)
def read_hero_with_team(
    hero_id: int,
    session: Session = Depends(get_session)
):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero
```

#### Creating with Relationships
```python
@router.post("/", response_model=Hero)
def create_hero_with_team(
    hero_data: HeroCreate,
    session: Session = Depends(get_session)
):
    # Validate that team exists
    if hero_data.team_id is not None:
        team = session.get(Team, hero_data.team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")

    db_hero = Hero.model_validate(hero_data)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero
```

## FastAPI Dependencies for SQLModel

### Session Dependency with Error Handling
```python
from contextlib import contextmanager

@contextmanager
def get_session_context() -> Generator[Session, None, None]:
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def get_session_dependency() -> Session:
    with get_session_context() as session:
        yield session

# Alternative: Simple dependency with try/finally
def get_session_simple() -> Generator[Session, None, None]:
    with Session(engine) as session:
        try:
            yield session
        except Exception:
            session.rollback()
            raise
```

### Current User Dependency with SQLModel
```python
from fastapi import HTTPException, status
from models.user import User

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = session.get(User, int(user_id))
    if user is None:
        raise credentials_exception
    return user
```

## Validation and Error Handling

### Custom Exception Handlers
```python
from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=400,
        content={"message": "Integrity constraint violation", "detail": str(exc)}
    )

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": "Validation error", "detail": str(exc)}
    )
```

### Validation in Models
```python
from pydantic import field_validator

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, min_length=2, max_length=100)
    secret_name: str = Field(max_length=100)
    age: Optional[int] = Field(default=None, ge=0, le=150)

    @field_validator('name')
    def validate_name(cls, v):
        if len(v) < 2:
            raise ValueError('Name must be at least 2 characters long')
        return v.title()

    @field_validator('age')
    def validate_age(cls, v):
        if v is not None and (v < 0 or v > 150):
            raise ValueError('Age must be between 0 and 150')
        return v
```

## Background Tasks with SQLModel

### Database Operations in Background
```python
from fastapi import BackgroundTasks

def send_hero_created_notification(hero_id: int, session: Session):
    hero = session.get(Hero, hero_id)
    if hero:
        # Send notification logic here
        print(f"Notification: Hero {hero.name} was created")

@router.post("/", response_model=Hero)
def create_hero_with_notification(
    hero: HeroCreate,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session)
):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)

    # Add background task with a new session
    background_tasks.add_task(send_hero_created_notification, db_hero.id, session)

    return db_hero
```

## Testing SQLModel with FastAPI

### Test Dependencies
```python
# conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool
from main import app
from database import get_session

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(bind=engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
```

### Test Examples
```python
# test_heroes.py
def test_create_hero(client: TestClient, session: Session):
    response = client.post(
        "/heroes/",
        json={"name": "Deadpool", "secret_name": "Wade Wilson", "age": 35}
    )
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "Deadpool"
    assert data["secret_name"] == "Wade Wilson"
    assert data["age"] == 35

def test_read_hero(client: TestClient, session: Session):
    # First create a hero
    hero = Hero(name="Spider-Boy", secret_name="Pedro Parqueador", age=16)
    session.add(hero)
    session.commit()

    response = client.get(f"/heroes/{hero.id}")
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "Spider-Boy"
```

## Performance Considerations

### Eager Loading in API Endpoints
```python
from sqlalchemy.orm import selectinload

@router.get("/with-teams", response_model=List[Hero])
def read_heroes_with_teams(session: Session = Depends(get_session)):
    statement = select(Hero).options(selectinload(Hero.team))
    heroes = session.exec(statement).all()
    return heroes
```

### Pagination in APIs
```python
from typing import List

class PaginatedHeroes(BaseModel):
    heroes: List[Hero]
    total: int
    offset: int
    limit: int

@router.get("/paginated", response_model=PaginatedHeroes)
def read_heroes_paginated(
    session: Session = Depends(get_session),
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    total_statement = select(Hero).with_only_columns(func.count(Hero.id))
    total = session.exec(total_statement).one()

    heroes = session.exec(
        select(Hero).offset(offset).limit(limit)
    ).all()

    return PaginatedHeroes(
        heroes=heroes,
        total=total,
        offset=offset,
        limit=limit
    )
```