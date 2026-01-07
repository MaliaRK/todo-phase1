from sqlmodel import Session, select
from typing import List, Optional
from ..models.task_model import Task, TaskCreate, TaskUpdate
from datetime import datetime


class TaskService:
    @staticmethod
    def create_task_for_user(task_data: TaskCreate, user_id: str, session: Session) -> Task:
        # Create task instance manually to handle datetime fields properly
        task = Task(
            title=task_data.title,
            description=task_data.description,
            is_completed=task_data.is_completed,
            user_id=user_id  # Assign the task to the current user
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def get_task_by_id_for_user(task_id: int, user_id: str, session: Session) -> Optional[Task]:
        # Get task by ID and ensure it belongs to the user
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()
        return task

    @staticmethod
    def get_user_tasks(user_id: str, session: Session) -> List[Task]:
        # Get all tasks for a specific user
        statement = select(Task).where(Task.user_id == user_id)
        tasks = session.exec(statement).all()
        return tasks

    @staticmethod
    def update_task_for_user(task_id: int, task_data: TaskUpdate, user_id: str, session: Session) -> Optional[Task]:
        # Get task and ensure it belongs to the user
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()

        if not task:
            return None

        # Update only provided fields
        for field, value in task_data.model_dump(exclude_unset=True).items():
            setattr(task, field, value)

        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def delete_task_for_user(task_id: int, user_id: str, session: Session) -> bool:
        # Get task and ensure it belongs to the user
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()

        if not task:
            return False

        session.delete(task)
        session.commit()
        return True

    @staticmethod
    def toggle_task_completion_for_user(task_id: int, user_id: str, session: Session) -> Optional[Task]:
        # Get task and ensure it belongs to the user
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()

        if not task:
            return None

        task.is_completed = not task.is_completed
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    # Keep the original methods for backward compatibility if needed
    @staticmethod
    def create_task(task_data: TaskCreate, session: Session) -> Task:
        # Create task instance manually to handle datetime fields properly
        task = Task(
            title=task_data.title,
            description=task_data.description,
            is_completed=task_data.is_completed,
            # The created_at and updated_at fields will be set by their default_factory
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def get_task_by_id(task_id: int, session: Session) -> Optional[Task]:
        return session.get(Task, task_id)

    @staticmethod
    def get_all_tasks(session: Session) -> List[Task]:
        tasks = session.exec(select(Task)).all()
        return tasks

    @staticmethod
    def update_task(task_id: int, task_data: TaskUpdate, session: Session) -> Optional[Task]:
        task = session.get(Task, task_id)
        if not task:
            return None

        # Update only provided fields
        for field, value in task_data.model_dump(exclude_unset=True).items():
            setattr(task, field, value)

        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def delete_task(task_id: int, session: Session) -> bool:
        task = session.get(Task, task_id)
        if not task:
            return False

        session.delete(task)
        session.commit()
        return True

    @staticmethod
    def toggle_task_completion(task_id: int, session: Session) -> Optional[Task]:
        task = session.get(Task, task_id)
        if not task:
            return None

        task.is_completed = not task.is_completed
        session.add(task)
        session.commit()
        session.refresh(task)
        return task