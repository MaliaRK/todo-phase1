from sqlmodel import select, Session
from typing import Optional, List, Dict, Any
from ..models.task_model import Task, TaskCreate, TaskUpdate
from ..database import get_session
from contextlib import contextmanager
from ..utils.logging import get_logger
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

logger = get_logger("mcp-tools")

async def add_task(user_id: str, title: str, description: Optional[str] = None) -> Dict[str, Any]:
    """
    Add a new task to the user's list.

    Args:
        user_id: ID of the user creating the task
        title: Title of the task
        description: Optional description of the task

    Returns:
        Dictionary with task information
    """
    try:
        # Create a new task instance
        task_create = TaskCreate(
            title=title,
            description=description,
            is_completed=False
        )

        # Create the task in the database
        with contextmanager(get_session)() as session:
            db_task = Task(
                title=task_create.title,
                description=task_create.description,
                is_completed=task_create.is_completed,
                user_id=user_id
            )
            session.add(db_task)
            session.commit()
            session.refresh(db_task)

        logger.info(f"Task added for user {user_id}: {title}")

        return {
            "id": db_task.id,
            "title": db_task.title,
            "description": db_task.description,
            "is_completed": db_task.is_completed,
            "user_id": db_task.user_id,
            "created_at": db_task.created_at.isoformat() if hasattr(db_task, 'created_at') else None
        }
    except SQLAlchemyError as e:
        logger.error(f"Database error in add_task for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while adding task"
        )
    except Exception as e:
        logger.error(f"Unexpected error in add_task for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while adding task"
        )


async def list_tasks(user_id: str, status: Optional[str] = "all") -> List[Dict[str, Any]]:
    """
    List tasks for the user with optional filtering.

    Args:
        user_id: ID of the user whose tasks to list
        status: Filter status ('all', 'pending', 'completed')

    Returns:
        List of task dictionaries
    """
    try:
        with contextmanager(get_session)() as session:
            # Build query based on status filter
            query = select(Task).where(Task.user_id == user_id)

            if status == "pending":
                query = query.where(Task.is_completed == False)
            elif status == "completed":
                query = query.where(Task.is_completed == True)

            db_tasks = session.exec(query).all()

        logger.info(f"Tasks listed for user {user_id}, status: {status}, count: {len(db_tasks)}")

        return [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_completed": task.is_completed,
                "user_id": task.user_id,
                "created_at": task.created_at.isoformat() if hasattr(task, 'created_at') else None,
                "updated_at": task.updated_at.isoformat() if hasattr(task, 'updated_at') else None
            }
            for task in db_tasks
        ]
    except SQLAlchemyError as e:
        logger.error(f"Database error in list_tasks for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while listing tasks"
        )
    except Exception as e:
        logger.error(f"Unexpected error in list_tasks for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while listing tasks"
        )


async def complete_task(user_id: str, task_id: int) -> Dict[str, Any]:
    """
    Mark a task as completed.

    Args:
        user_id: ID of the user owning the task
        task_id: ID of the task to complete

    Returns:
        Dictionary with updated task information
    """
    try:
        with contextmanager(get_session)() as session:
            # First, get the task to verify it belongs to the user
            db_task = session.exec(
                select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
            ).first()

            if not db_task:
                logger.warning(f"Task {task_id} not found for user {user_id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Task not found or does not belong to user"
                )

            # Update the task completion status
            db_task.is_completed = True
            session.add(db_task)
            session.commit()
            session.refresh(db_task)

        logger.info(f"Task {task_id} completed for user {user_id}")

        return {
            "id": db_task.id,
            "title": db_task.title,
            "description": db_task.description,
            "is_completed": db_task.is_completed,
            "user_id": db_task.user_id,
            "updated_at": db_task.updated_at.isoformat() if hasattr(db_task, 'updated_at') else None
        }
    except SQLAlchemyError as e:
        logger.error(f"Database error in complete_task for user {user_id}, task {task_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while completing task"
        )
    except Exception as e:
        logger.error(f"Unexpected error in complete_task for user {user_id}, task {task_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while completing task"
        )


async def delete_task(user_id: str, task_id: int) -> Dict[str, Any]:
    """
    Delete a task from the user's list.

    Args:
        user_id: ID of the user owning the task
        task_id: ID of the task to delete

    Returns:
        Dictionary confirming deletion
    """
    try:
        with contextmanager(get_session)() as session:
            # First, get the task to verify it belongs to the user and get its details
            db_task = session.exec(
                select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
            ).first()

            if not db_task:
                logger.warning(f"Task {task_id} not found for user {user_id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Task not found or does not belong to user"
                )

            # Delete the task
            session.delete(db_task)
            session.commit()

        logger.info(f"Task {task_id} deleted for user {user_id}")

        return {
            "id": db_task.id,
            "title": db_task.title,
            "deleted": True
        }
    except SQLAlchemyError as e:
        logger.error(f"Database error in delete_task for user {user_id}, task {task_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while deleting task"
        )
    except Exception as e:
        logger.error(f"Unexpected error in delete_task for user {user_id}, task {task_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting task"
        )


async def update_task(user_id: str, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
    """
    Update a task's details.

    Args:
        user_id: ID of the user owning the task
        task_id: ID of the task to update
        title: New title (optional)
        description: New description (optional)

    Returns:
        Dictionary with updated task information
    """
    try:
        with contextmanager(get_session)() as session:
            # First, get the task to verify it belongs to the user
            db_task = session.exec(
                select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
            ).first()

            if not db_task:
                logger.warning(f"Task {task_id} not found for user {user_id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Task not found or does not belong to user"
                )

            # Update the task with provided values
            if title is not None:
                db_task.title = title
            if description is not None:
                db_task.description = description

            session.add(db_task)
            session.commit()
            session.refresh(db_task)

        logger.info(f"Task {task_id} updated for user {user_id}")

        return {
            "id": db_task.id,
            "title": db_task.title,
            "description": db_task.description,
            "is_completed": db_task.is_completed,
            "user_id": db_task.user_id,
            "updated_at": db_task.updated_at.isoformat() if hasattr(db_task, 'updated_at') else None
        }
    except SQLAlchemyError as e:
        logger.error(f"Database error in update_task for user {user_id}, task {task_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while updating task"
        )
    except Exception as e:
        logger.error(f"Unexpected error in update_task for user {user_id}, task {task_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating task"
        )