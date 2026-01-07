import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from sqlmodel import SQLModel
from src.database import engine


def create_db_and_tables():
    """Create database tables based on SQLModel models"""
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()
    print("Database tables created successfully!")