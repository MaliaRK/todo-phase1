"""
Business logic services for the Todo Application CLI
"""
from typing import Optional
from .models import Task
from .storage import InMemoryStorage
from .utils import validate_task_content, ValidationError, TaskNotFoundError


class TaskService:
    """
    Business logic for task operations
    """
    def __init__(self, storage: InMemoryStorage):
        self.storage = storage

    def add_task(self, title: str, description: str = None) -> Task:
        """
        Implement add_task function with title and description validation
        """
        validate_task_content(title, description)
        task = Task(id=0, title=title.strip(), description=description, completed=False)
        return self.storage.add_task(task)

    def list_tasks(self) -> list:
        """
        Implement list_tasks function to retrieve all tasks
        """
        return self.storage.list_tasks()

    def toggle_task_completion(self, task_id: int) -> Optional[Task]:
        """
        Implement toggle_task_completion function
        """
        task = self.storage.get_task(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")

        task.completed = not task.completed
        return self.storage.update_task(task_id, task)

    def update_task(self, task_id: int, title: str = None, description: str = None) -> Optional[Task]:
        """
        Implement update_task function with validation
        """
        task = self.storage.get_task(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")

        # Use existing values if not provided
        new_title = title if title is not None else task.title
        new_description = description if description is not None else task.description

        # Validate the new content
        validate_task_content(new_title, new_description)

        # Update the task
        updated_task = Task(
            id=task_id,
            title=new_title.strip(),
            description=new_description,
            completed=task.completed
        )

        return self.storage.update_task(task_id, updated_task)

    def delete_task(self, task_id: int) -> bool:
        """
        Implement delete_task function with validation
        """
        task = self.storage.get_task(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")

        return self.storage.delete_task(task_id)

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Get a specific task by ID
        """
        return self.storage.get_task(task_id)