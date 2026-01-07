import os
from sqlmodel import create_engine, SQLModel
from src.models.task_model import Task
from src.models.user_model import User
from src.models.session_model import Session as SessionModel
from dotenv import load_dotenv
from sqlalchemy import text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todoapp.db")

# For PostgreSQL, add only valid connection parameters to handle connection issues
if DATABASE_URL.startswith("postgresql://"):
    # Add connection parameters to handle SSL and timeouts
    if "?" not in DATABASE_URL:
        DATABASE_URL += "?sslmode=require"
    else:
        # Check if sslmode is already set
        if "sslmode=" not in DATABASE_URL:
            DATABASE_URL += "&sslmode=require"

    # Add connection timeout parameter only
    if "connect_timeout=" not in DATABASE_URL:
        DATABASE_URL += "&connect_timeout=30"

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

def check_and_update_schema():
    print("Recreating database schema to match current models...")

    # This will recreate all tables to match the current models
    # NOTE: This will lose all existing data - only use in development!
    SQLModel.metadata.create_all(engine)

    print("Database schema updated to match current models.")

if __name__ == "__main__":
    check_and_update_schema()