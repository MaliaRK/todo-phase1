# FastAPI Database Integration Guide

## SQLAlchemy Integration

### Database Setup

```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

engine = create_engine(
    DATABASE_URL,
    # For SQLite only
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Database Models

```python
# models.py
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    items = relationship("Item", back_populates="owner")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Relationship
    owner = relationship("User", back_populates="items")
```

### Pydantic Schemas

```python
# schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Shared properties
class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None

# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str

# Properties to receive on item update
class ItemUpdate(ItemBase):
    pass

# Properties shared by models stored in DB
class ItemInDBBase(ItemBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

# Properties to return to client
class Item(ItemInDBBase):
    pass

# Properties properties stored in DB
class ItemInDB(ItemInDBBase):
    hashed_password: str
```

## Dependency Injection for Database Sessions

```python
# main.py
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import User, Item
from schemas import UserCreate, User, ItemCreate, Item

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    from models import User
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = User(email=user.email, username=user.username, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/users/{user_id}/items/", response_model=Item)
def create_item_for_user(
    user_id: int, item: ItemCreate, db: Session = Depends(get_db)
):
    from models import Item
    db_item = Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/users/{user_id}/items/", response_model=List[Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(Item).offset(skip).limit(limit).all()
    return items
```

## Async Database with Databases and SQLAlchemy Core

For fully async operations, use `databases` with SQLAlchemy Core:

```python
# async_database.py
import databases
import sqlalchemy
from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean, create_engine
from sqlalchemy.dialects.postgresql import UUID
import os

DATABASE_URL = os.getenv("DATABASE_URL")

database = databases.Database(DATABASE_URL)

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, unique=True, nullable=False),
    Column("username", String, unique=True, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("is_active", Boolean, default=True),
)

engine = create_engine(DATABASE_URL)

# Create tables
metadata.create_all(engine)
```

```python
# async_main.py
from fastapi import FastAPI, Depends
import async_database as db
from async_database import database
from pydantic import BaseModel
from typing import List

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class User(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool = True

@app.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(user.password)

    query = db.users.insert().values(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    user_id = await database.execute(query)

    return {**user.dict(), "id": user_id, "is_active": True}

@app.get("/users/", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 20):
    query = db.users.select().offset(skip).limit(limit)
    users = await database.fetch_all(query)
    return users
```

## Connection Pooling

Configure connection pooling for better performance:

```python
# database.py (with connection pooling)
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,  # Number of connections to maintain
    max_overflow=30,  # Additional connections beyond pool_size
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=3600,  # Recycle connections after 1 hour
)
```

## Repository Pattern

Implement the repository pattern for better separation of concerns:

```python
# repositories/user_repository.py
from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, user_id: int) -> User:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()

    def get_users(self, skip: int = 0, limit: int = 100):
        return self.db.query(User).offset(skip).limit(limit).all()

    def create_user(self, user: UserCreate):
        hashed_password = pwd_context.hash(user.password)
        db_user = User(
            email=user.email,
            username=user.username,
            hashed_password=hashed_password
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
```

```python
# dependencies.py
from sqlalchemy.orm import Session
from database import SessionLocal
from repositories.user_repository import UserRepository

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_repository(db: Session = Depends(get_db)):
    return UserRepository(db)
```

```python
# routers/users.py
from fastapi import APIRouter, Depends
from repositories.user_repository import UserRepository
from schemas import UserCreate, User

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=User)
async def create_user(
    user: UserCreate,
    user_repo: UserRepository = Depends(get_user_repository)
):
    db_user = user_repo.create_user(user)
    return db_user
```

## Background Tasks with Database

Handle database operations in background tasks:

```python
from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
from database import SessionLocal

def send_notification_email(user_email: str, message: str):
    # Simulate sending an email
    print(f"Sending email to {user_email}: {message}")

@app.post("/users/")
async def create_user_and_notify(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Create user
    user_repo = UserRepository(db)
    db_user = user_repo.create_user(user)

    # Send notification in background
    background_tasks.add_task(
        send_notification_email,
        db_user.email,
        "Welcome to our service!"
    )

    return db_user
```

## Error Handling for Database Operations

Implement proper error handling for database operations:

```python
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        user_repo = UserRepository(db)
        db_user = user_repo.create_user(user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="A user with this email or username already exists"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An error occurred while creating the user"
        )
```