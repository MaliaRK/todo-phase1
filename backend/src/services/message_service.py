from sqlmodel import Session, select
from typing import Optional
from ..models.message_model import Message, MessageCreate
from ..utils.logging import get_logger
from sqlalchemy.exc import SQLAlchemyError

logger = get_logger("message-service")

async def save_user_message(
    conversation_id: int,
    user_id: int,
    content: str,
    session: Session
) -> Message:
    """
    Save a user message to the database.

    Args:
        conversation_id: ID of the conversation
        user_id: ID of the user sending the message
        content: Content of the message
        session: Database session

    Returns:
        Saved Message instance
    """
    try:
        message_create = MessageCreate(
            conversation_id=conversation_id,
            user_id=user_id,
            role="user",
            content=content
        )

        db_message = Message(
            conversation_id=message_create.conversation_id,
            user_id=message_create.user_id,
            role=message_create.role,
            content=message_create.content
        )

        session.add(db_message)
        session.commit()
        session.refresh(db_message)

        logger.info(f"Saved user message for conversation {conversation_id}, user {user_id}")
        return db_message

    except SQLAlchemyError as e:
        logger.error(f"Database error in save_user_message for conversation {conversation_id}, user {user_id}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in save_user_message for conversation {conversation_id}, user {user_id}: {str(e)}")
        raise


async def save_assistant_message(
    conversation_id: int,
    user_id: int,
    content: str,
    session: Session
) -> Message:
    """
    Save an assistant message to the database.

    Args:
        conversation_id: ID of the conversation
        user_id: ID of the user (for reference)
        content: Content of the assistant's response
        session: Database session

    Returns:
        Saved Message instance
    """
    try:
        message_create = MessageCreate(
            conversation_id=conversation_id,
            user_id=user_id,
            role="assistant",
            content=content
        )

        db_message = Message(
            conversation_id=message_create.conversation_id,
            user_id=message_create.user_id,
            role=message_create.role,
            content=message_create.content
        )

        session.add(db_message)
        session.commit()
        session.refresh(db_message)

        logger.info(f"Saved assistant message for conversation {conversation_id}, user {user_id}")
        return db_message

    except SQLAlchemyError as e:
        logger.error(f"Database error in save_assistant_message for conversation {conversation_id}, user {user_id}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in save_assistant_message for conversation {conversation_id}, user {user_id}: {str(e)}")
        raise


async def get_latest_messages(
    conversation_id: int,
    user_id: int,
    session: Session,
    limit: int = 10
) -> list:
    """
    Get the latest messages from a conversation.

    Args:
        conversation_id: ID of the conversation
        user_id: ID of the user requesting messages
        session: Database session
        limit: Number of messages to retrieve (default 10)

    Returns:
        List of message dictionaries
    """
    try:
        # Verify the conversation belongs to the user
        from ..models.conversation_model import Conversation
        conversation = session.exec(
            select(Conversation)
            .where(Conversation.id == conversation_id)
            .where(Conversation.user_id == user_id)
        ).first()

        if not conversation:
            logger.warning(f"Conversation {conversation_id} not found for user {user_id}")
            return []

        # Get the latest messages
        messages = session.exec(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        ).all()

        # Reverse to get chronological order (oldest first)
        messages.reverse()

        logger.info(f"Retrieved {len(messages)} latest messages for conversation {conversation_id}")
        return [
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.created_at.isoformat()
            }
            for msg in messages
        ]

    except SQLAlchemyError as e:
        logger.error(f"Database error in get_latest_messages for conversation {conversation_id}, user {user_id}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_latest_messages for conversation {conversation_id}, user {user_id}: {str(e)}")
        raise


async def count_messages_in_conversation(
    conversation_id: int,
    user_id: int,
    session: Session
) -> int:
    """
    Count the number of messages in a conversation.

    Args:
        conversation_id: ID of the conversation
        user_id: ID of the user requesting the count
        session: Database session

    Returns:
        Number of messages in the conversation
    """
    try:
        # Verify the conversation belongs to the user
        from ..models.conversation_model import Conversation
        conversation = session.exec(
            select(Conversation)
            .where(Conversation.id == conversation_id)
            .where(Conversation.user_id == user_id)
        ).first()

        if not conversation:
            logger.warning(f"Conversation {conversation_id} not found for user {user_id}")
            return 0

        # Count messages
        from sqlalchemy import func
        count = session.exec(
            select(func.count(Message.id))
            .where(Message.conversation_id == conversation_id)
        ).one()

        logger.info(f"Counted {count} messages in conversation {conversation_id}")
        return count

    except SQLAlchemyError as e:
        logger.error(f"Database error in count_messages_in_conversation for conversation {conversation_id}, user {user_id}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in count_messages_in_conversation for conversation {conversation_id}, user {user_id}: {str(e)}")
        raise