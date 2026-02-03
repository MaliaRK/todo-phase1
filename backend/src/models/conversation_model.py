from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class ConversationBase(SQLModel):
    user_id: str = Field(nullable=False)


class Conversation(ConversationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ConversationCreate(ConversationBase):
    pass


class ConversationUpdate(SQLModel):
    pass