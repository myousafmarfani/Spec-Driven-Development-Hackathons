"""
Chat API Endpoint
This module implements the chat endpoint with JWT authentication.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List
import uuid
from sqlmodel import Session, select
from datetime import datetime

from src.services.chat_service import ChatService
from src.models.conversation import Conversation
from src.models.message import Message
from db import get_session
from auth import get_current_user, verify_user_owns_token


router = APIRouter(prefix="/api/{user_id}", tags=["chat"])


class ChatRequest(BaseModel):
    """
    Request model for chat endpoint.
    """
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    """
    Response model for chat endpoint.
    """
    conversation_id: str
    response: str
    timestamp: datetime


class MessageResponse(BaseModel):
    """
    Response model for a single message.
    """
    id: int
    role: str
    content: str
    created_at: datetime


class ConversationMessagesResponse(BaseModel):
    """
    Response model for conversation messages endpoint.
    """
    conversation_id: str
    messages: List[MessageResponse]


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Chat endpoint that handles user messages and returns AI responses.

    Args:
        user_id: The ID of the user (from path parameter)
        request: Chat request containing the message and optional conversation ID
        current_user_id: Current authenticated user ID (validated via JWT)
        db: Database session

    Returns:
        ChatResponse containing the AI response and conversation ID
    """
    # Verify that the user_id in the path matches the authenticated user
    verify_user_owns_token(user_id, current_user_id)

    # Initialize chat service
    chat_service = ChatService(db)

    try:
        # Process the chat request and get response
        result = await chat_service.process_chat_message(
            user_id=user_id,
            message=request.message,
            conversation_id=request.conversation_id
        )

        return ChatResponse(
            conversation_id=result["conversation_id"],
            response=result["response"],
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        # Log the full error for debugging
        import traceback
        print(f"\n=== CHAT ERROR ===")
        print(f"Error: {str(e)}")
        print(f"Traceback:")
        traceback.print_exc()
        print(f"==================\n")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat message: {str(e)}"
        )


# Health check endpoint
@router.get("/chat/health")
async def chat_health():
    """
    Health check for the chat endpoint.
    """
    return {"status": "healthy", "service": "chat"}


@router.get("/conversations/{conversation_id}/messages", response_model=ConversationMessagesResponse)
async def get_conversation_messages(
    user_id: str,
    conversation_id: str,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Get all messages for a specific conversation.

    Args:
        user_id: The ID of the user (from path parameter)
        conversation_id: The public UUID of the conversation
        current_user_id: Current authenticated user ID (validated via JWT)
        db: Database session

    Returns:
        ConversationMessagesResponse containing all messages ordered by created_at
    """
    # Verify that the user_id in the path matches the authenticated user
    verify_user_owns_token(user_id, current_user_id)

    # Find the conversation by public UUID and verify ownership
    statement = select(Conversation).where(
        Conversation.conversation_id == conversation_id,
        Conversation.user_id == user_id
    )
    conversation = db.exec(statement).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or access denied"
        )

    # Get all messages for this conversation ordered by created_at
    messages_statement = select(Message).where(
        Message.conversation_id == conversation.id
    ).order_by(Message.created_at)
    
    messages = db.exec(messages_statement).all()

    return ConversationMessagesResponse(
        conversation_id=conversation_id,
        messages=[
            MessageResponse(
                id=msg.id,
                role=msg.role,
                content=msg.content,
                created_at=msg.created_at
            )
            for msg in messages
        ]
    )