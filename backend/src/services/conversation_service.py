from sqlmodel import Session, select
from typing import Optional
from ..models.conversation_model import Conversation, ConversationCreate
from ..models.message_model import Message
from ..utils.logging import get_logger
from sqlalchemy.exc import SQLAlchemyError

logger = get_logger("conversation-service")

async def get_or_create_conversation(
    user_id: int,
    conversation_id: Optional[int],
    session: Session
) -> Conversation:
    """
    Get an existing conversation or create a new one.

    Args:
        user_id: ID of the user requesting the conversation
        conversation_id: Optional existing conversation ID
        session: Database session

    Returns:
        Conversation instance
    """
    try:
        if conversation_id is not None:
            # Try to get existing conversation
            existing_conversation = session.exec(
                select(Conversation)
                .where(Conversation.id == conversation_id)
                .where(Conversation.user_id == user_id)
            ).first()

            if existing_conversation:
                logger.info(f"Retrieved existing conversation {conversation_id} for user {user_id}")
                return existing_conversation

        # Create new conversation
        conversation_create = ConversationCreate(user_id=user_id)
        db_conversation = Conversation(
            user_id=conversation_create.user_id
        )
        session.add(db_conversation)
        session.commit()
        session.refresh(db_conversation)

        logger.info(f"Created new conversation {db_conversation.id} for user {user_id}")
        return db_conversation

    except SQLAlchemyError as e:
        logger.error(f"Database error in get_or_create_conversation for user {user_id}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_or_create_conversation for user {user_id}: {str(e)}")
        raise


async def get_conversation_history(
    conversation_id: int,
    user_id: int,
    session: Session,
    limit: Optional[int] = 50
) -> list:
    """
    Get the message history for a conversation.

    Args:
        conversation_id: ID of the conversation
        user_id: ID of the user requesting the history
        session: Database session
        limit: Maximum number of messages to return (default 50)

    Returns:
        List of message dictionaries
    """
    try:
        # Verify conversation belongs to user
        conversation = session.exec(
            select(Conversation)
            .where(Conversation.id == conversation_id)
            .where(Conversation.user_id == user_id)
        ).first()

        if not conversation:
            logger.warning(f"Conversation {conversation_id} not found for user {user_id}")
            return []

        # Get messages for the conversation
        query = select(Message).where(Message.conversation_id == conversation_id)

        if limit:
            query = query.limit(limit)

        # Order by creation time
        query = query.order_by(Message.created_at)

        messages = session.exec(query).all()

        logger.info(f"Retrieved {len(messages)} messages for conversation {conversation_id}")

        return [
            {
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.created_at.isoformat()
            }
            for msg in messages
        ]

    except SQLAlchemyError as e:
        logger.error(f"Database error in get_conversation_history for conversation {conversation_id}, user {user_id}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_conversation_history for conversation {conversation_id}, user {user_id}: {str(e)}")
        raise


async def update_conversation_timestamp(
    conversation_id: int,
    user_id: int,
    session: Session
) -> bool:
    """
    Update the timestamp of the last activity in a conversation.

    Args:
        conversation_id: ID of the conversation to update
        user_id: ID of the user updating the conversation
        session: Database session

    Returns:
        True if update was successful, False otherwise
    """
    try:
        conversation = session.exec(
            select(Conversation)
            .where(Conversation.id == conversation_id)
            .where(Conversation.user_id == user_id)
        ).first()

        if not conversation:
            logger.warning(f"Conversation {conversation_id} not found for user {user_id}")
            return False

        # Update the updated_at timestamp
        conversation.updated_at = type(conversation).updated_at.default.arg()
        session.add(conversation)
        session.commit()

        logger.info(f"Updated timestamp for conversation {conversation_id}")
        return True

    except SQLAlchemyError as e:
        logger.error(f"Database error in update_conversation_timestamp for conversation {conversation_id}, user {user_id}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in update_conversation_timestamp for conversation {conversation_id}, user {user_id}: {str(e)}")
        raise