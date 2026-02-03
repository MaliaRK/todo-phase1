from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class MessageBase(SQLModel):
    conversation_id: int = Field(nullable=False)
    user_id: str = Field(nullable=False)
    role: str = Field(max_length=20, nullable=False)  # 'user' or 'assistant'
    content: str = Field(max_length=10000, nullable=False)


class Message(MessageBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", nullable=False)
    user_id: str = Field(foreign_key="user.id", nullable=False)
    role: str = Field(max_length=20, nullable=False)  # 'user' or 'assistant'
    content: str = Field(max_length=10000, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class MessageCreate(MessageBase):
    pass


class MessageUpdate(SQLModel):
    content: Optional[str] = None