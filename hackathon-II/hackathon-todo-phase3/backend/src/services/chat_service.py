"""
Chat Service
This module handles chat operations including conversation state management.
"""
from typing import Dict, Any, Optional
from sqlmodel import Session, select
from datetime import datetime
import uuid
import asyncio

from ..models.conversation import Conversation
from ..models.message import Message
from ..agents.agent_runner import AgentRunner


class ChatService:
    """
    Service class for handling chat operations and conversation state management.
    """

    def __init__(self, db_session: Session):
        self.db = db_session
        self.agent_runner = AgentRunner()

    async def process_chat_message(
        self,
        user_id: str,
        message: str,
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a chat message and return the AI response.

        Args:
            user_id: ID of the user
            message: User's message
            conversation_id: Optional conversation ID to continue existing conversation

        Returns:
            Dictionary containing the response and conversation ID
        """
        # Attempt to find an existing conversation by its public ID (UUID)
        conversation: Optional[Conversation] = None
        if conversation_id:
            statement = select(Conversation).where(
                Conversation.conversation_id == conversation_id,
                Conversation.user_id == user_id
            )
            conversation = self.db.exec(statement).first()

        # Create a brand-new conversation when none exist or ownership fails
        if not conversation:
            conversation = Conversation(
                user_id=user_id,
                conversation_id=str(uuid.uuid4())
            )
            self.db.add(conversation)
            self.db.commit()
            self.db.refresh(conversation)

        # Separate internal DB id from the public UUID we expose
        conversation_db_id = conversation.id
        conversation_public_id = conversation.conversation_id

        # Run the agent to get the response
        result = await self.agent_runner.run_agent_async(
            user_input=message,
            user_id=user_id,
            conversation_id=conversation_db_id
        )

        # Return the response and conversation ID
        return {
            "response": result.get("response", "I couldn't process your request."),
            "conversation_id": conversation_public_id,
            "tool_calls": result.get("tool_calls", [])
        }

    def get_conversation_history(self, conversation_id: int, user_id: str) -> Optional[list]:
        """
        Retrieve conversation history for a given conversation ID.

        Args:
            conversation_id: ID of the conversation
            user_id: ID of the user (for authorization check)

        Returns:
            List of messages in the conversation or None if not found/authorized
        """
        # Verify that the conversation belongs to the user
        conversation = self.db.get(Conversation, conversation_id)
        if not conversation or conversation.user_id != user_id:
            return None

        # Get all messages in this conversation
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at)

        messages = self.db.exec(statement).all()

        return [
            {
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.created_at.isoformat() if msg.created_at else None
            }
            for msg in messages
        ]

    def create_message(self, conversation_id: int, user_id: str, role: str, content: str) -> Optional[Message]:
        """
        Create a new message in a conversation.

        Args:
            conversation_id: ID of the conversation
            user_id: ID of the user
            role: Role of the message sender ('user' or 'assistant')
            content: Content of the message

        Returns:
            Created Message object or None if conversation doesn't exist/auth fails
        """
        # Verify that the conversation exists and belongs to the user
        conversation = self.db.get(Conversation, conversation_id)
        if not conversation or conversation.user_id != user_id:
            return None

        # Create the message
        message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            content=content
        )

        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)

        return message