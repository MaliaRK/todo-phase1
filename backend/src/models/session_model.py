from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Session(SQLModel, table=True):
    """
    Session model representing an authenticated user's active session with JWT token
    containing user identity claims
    """
    id: str = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", nullable=False)
    expires_at: datetime = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)