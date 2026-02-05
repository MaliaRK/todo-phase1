from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from sqlmodel import Session, select
from ..models.message_model import Message, MessageCreate
from ..models.conversation_model import Conversation, ConversationCreate
from ..database import get_session
from ..auth.jwt_auth import get_current_user
from ..models.user_model import User
from ..utils.logging import get_logger
# Remove these imports as they're not used in the current implementation
# from openai.types.beta.threads.runs.run import Run
# from openai.types.beta.threads.thread import Thread
from ..services.conversation_service import get_or_create_conversation
from ..services.message_service import save_user_message, save_assistant_message
from ..services.agent_service import process_user_message
from ..services.response_service import format_response

router = APIRouter(prefix="/api", tags=["chat"])
logger = get_logger("chat-api")

class ChatRequest(BaseModel):
    """
    Request model for chat endpoint.
    """
    conversation_id: Optional[int] = None
    message: str

class ToolCall(BaseModel):
    """
    Model for tool calls in the response.
    """
    id: str
    type: str
    function: Dict[str, Any]

class TaskSummary(BaseModel):
    """
    Model for task summary in the response.
    """
    total_count: int
    pending_count: int
    completed_count: int

class ChatResponse(BaseModel):
    """
    Response model for chat endpoint.
    """
    conversation_id: int
    response: str
    tool_calls: Optional[List[ToolCall]] = []
    task_summary: Optional[TaskSummary] = None

@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> ChatResponse:
    """
    Process a user message in a conversation.

    Args:
        user_id: ID of the user making the request
        request: Chat request containing the message and optional conversation ID
        current_user: Authenticated user making the request
        session: Database session

    Returns:
        ChatResponse with the AI's response and conversation ID

    Raises:
        HTTPException: If authentication fails or user_id doesn't match JWT
    """
    # Verify that the user_id in the path matches the authenticated user
    if current_user.id != user_id:
        logger.warning(f"User ID mismatch: path={user_id}, token={current_user.id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in path does not match authenticated user"
        )

    try:
        # Get or create conversation
        conversation = await get_or_create_conversation(user_id, request.conversation_id, session)

        # Save user message to database
        user_message = await save_user_message(conversation.id, user_id, request.message, session)

        # Process the message with the AI agent
        agent_response = await process_user_message(
            user_id=user_id,
            conversation_id=conversation.id,
            user_message=request.message
        )

        # Save assistant response to database
        assistant_message = await save_assistant_message(
            conversation.id,
            user_id,
            agent_response.get('response', ''),
            session
        )

        # Format the response
        formatted_response = await format_response(agent_response)

        logger.info(f"Chat processed for user {user_id}, conversation {conversation.id}")

        return ChatResponse(
            conversation_id=conversation.id,
            response=formatted_response.get('response', ''),
            tool_calls=formatted_response.get('tool_calls', []),
            task_summary=formatted_response.get('task_summary', None)
        )

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error processing chat for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your message"
        )

# Health check endpoint
@router.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint to verify the service is running.

    Returns:
        Dictionary with status information
    """
    return {"status": "healthy", "service": "ai-todo-chatbot"}