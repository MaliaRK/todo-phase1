from sqlmodel import create_engine, Session
from typing import Generator
from contextlib import contextmanager
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todoapp.db")

# For PostgreSQL, add connection parameters to handle connection issues
if DATABASE_URL.startswith("postgresql://"):
    # Add connection parameters to handle SSL and timeouts
    if "?" not in DATABASE_URL:
        DATABASE_URL += "?sslmode=require"
    else:
        # Check if sslmode is already set
        if "sslmode=" not in DATABASE_URL:
            DATABASE_URL += "&sslmode=require"

# Create engine with connection pooling options
engine = create_engine(
    DATABASE_URL,
    echo=False,           # Set to True for SQL debugging
    pool_pre_ping=True,   # Verify connections before use
    pool_recycle=300,     # Recycle connections every 5 minutes
    pool_size=5,          # Number of connection pools
    max_overflow=10,      # Additional connections beyond pool_size
    pool_timeout=30,      # Timeout for getting a connection from the pool
    connect_args={
        "connect_timeout": 30,  # Connection timeout
    }
)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


@contextmanager
def get_db_session():
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()