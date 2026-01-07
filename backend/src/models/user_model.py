from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class User(SQLModel, table=True):
    """
    User model representing a registered user account with unique identifier,
    email, and authentication credentials
    """
    id: str = Field(default=None, primary_key=True)
    email: str = Field(unique=True, nullable=False)
    name: Optional[str] = Field(default=None)
    hashed_password: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)