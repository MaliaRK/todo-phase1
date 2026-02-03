from sqlmodel import create_engine, Session
from sqlalchemy.orm import sessionmaker
from typing import Generator, AsyncGenerator
from contextlib import contextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.pool import QueuePool
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

# For PostgreSQL, add connection parameters to handle connection issues
if DATABASE_URL.startswith("postgresql://"):
    # Add connection parameters to handle SSL and timeouts
    if "?" not in DATABASE_URL:
        DATABASE_URL += "?sslmode=require"
    else:
        # Check if sslmode is already set
        if "sslmode=" not in DATABASE_URL:
            DATABASE_URL += "&sslmode=require"

# For async operations - use async driver
async_db_url = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
async_engine = create_async_engine(
    async_db_url,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={
        "connect_timeout": 30,
    }
)

# For sync operations (if needed) - use sync driver
sync_engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={
        "connect_timeout": 30,
    }
)

AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

def get_session() -> Generator[Session, None, None]:
    """Dependency to get sync database session."""
    with Session(sync_engine) as session:
        yield session


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get async database session."""
    async with AsyncSessionLocal() as session:
        yield session


@contextmanager
def get_db_session():
    with Session(sync_engine) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

# Import all models here to ensure they're registered with SQLModel
from .models.task_model import Task
from .models.user_model import User
from .models.conversation_model import Conversation
from .models.message_model import Message

def create_db_and_tables():
    """Create database tables (synchronous - for initialization)."""
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(sync_engine)