from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .conversation import Conversation  # noqa: F401


class MessageBase(SQLModel):
    conversation_id: int = Field(foreign_key="conversations.id", description="ID of the conversation this message belongs to")
    user_id: str = Field(index=True, description="ID of the user who sent this message")
    role: str = Field(description="Message sender role (user/assistant/system)")
    content: str = Field(description="Message content")


class Message(MessageBase, table=True):
    """
    Message model representing a single message in a chat conversation.
    """
    __tablename__ = "messages"
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    # Relationship to the conversation this message belongs to
    conversation: "Conversation" = Relationship(back_populates="messages")


class MessagePublic(MessageBase):
    """
    Public representation of a Message without internal fields.
    """
    id: int
    created_at: datetime
    updated_at: datetime