from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .message import Message  # noqa: F401


class ConversationBase(SQLModel):
    user_id: str = Field(index=True, description="ID of the user who owns this conversation")
    conversation_id: str = Field(default=None, unique=True, description="Unique identifier for the conversation")


class Conversation(ConversationBase, table=True):
    """
    Conversation model representing a chat conversation between user and AI assistant.
    """
    __tablename__ = "conversations"
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    # Relationship to messages in this conversation
    messages: List["Message"] = Relationship(back_populates="conversation")


class ConversationPublic(ConversationBase):
    """
    Public representation of a Conversation without internal fields.
    """
    id: int
    created_at: datetime
    updated_at: datetime