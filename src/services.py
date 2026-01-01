"""
Business logic services for the Todo Application CLI
"""
from typing import Optional, List
from .models import Task
from .storage import InMemoryStorage
from .utils import validate_task_content, ValidationError, TaskNotFoundError


class TaskService:
    """
    Business logic for task operations
    """
    def __init__(self, storage: InMemoryStorage):
        self.storage = storage

    def add_task(self, title: str, description: str = None, priority: str = "Medium", tags: List[str] = None) -> Task:
        """
        Implement add_task function with title and description validation
        """
        validate_task_content(title, description)

        # Validate priority
        if priority not in ["High", "Medium", "Low"]:
            raise ValueError("Priority must be one of: High, Medium, Low")

        task = Task(
            id=0,
            title=title.strip(),
            description=description,
            completed=False,
            priority=priority,
            tags=tags if tags is not None else []
        )
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

    def update_task(self, task_id: int, title: str = None, description: str = None, priority: str = None, tags: List[str] = None) -> Optional[Task]:
        """
        Implement update_task function with validation
        """
        task = self.storage.get_task(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")

        # Use existing values if not provided
        new_title = title if title is not None else task.title
        new_description = description if description is not None else task.description
        new_priority = priority if priority is not None else task.priority
        new_tags = tags if tags is not None else task.tags

        # Validate the new content
        validate_task_content(new_title, new_description)

        # Validate priority if provided
        if priority is not None:
            if priority not in ["High", "Medium", "Low"]:
                raise ValueError("Priority must be one of: High, Medium, Low")

        # Update the task
        updated_task = Task(
            id=task_id,
            title=new_title.strip(),
            description=new_description,
            completed=task.completed,
            priority=new_priority,
            tags=new_tags
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

    def search_tasks(self, keyword: str) -> list:
        """
        Search tasks by keyword across title, description, and tags
        """
        if not keyword:
            return self.storage.list_tasks()

        keyword_lower = keyword.lower()
        matching_tasks = []

        for task in self.storage.list_tasks():
            # Check title
            if keyword_lower in task.title.lower():
                matching_tasks.append(task)
                continue

            # Check description
            if task.description and keyword_lower in task.description.lower():
                matching_tasks.append(task)
                continue

            # Check tags
            if task.tags:
                for tag in task.tags:
                    if keyword_lower in tag.lower():
                        matching_tasks.append(task)
                        break

        return matching_tasks

    def filter_by_status(self, completed: bool) -> list:
        """
        Filter tasks by completion status
        """
        all_tasks = self.storage.list_tasks()
        return [task for task in all_tasks if task.completed == completed]

    def filter_by_priority(self, priority: str) -> list:
        """
        Filter tasks by priority level
        """
        if priority not in ["High", "Medium", "Low"]:
            raise ValueError("Priority must be one of: High, Medium, Low")

        all_tasks = self.storage.list_tasks()
        return [task for task in all_tasks if task.priority == priority]

    def filter_by_tag(self, tag: str) -> list:
        """
        Filter tasks by specific tag
        """
        all_tasks = self.storage.list_tasks()
        return [task for task in all_tasks if tag in task.tags]

    def sort_by_priority(self, tasks: list) -> list:
        """
        Sort tasks by priority (High first, then Medium, then Low)
        """
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        return sorted(tasks, key=lambda task: priority_order[task.priority])

    def sort_alphabetically(self, tasks: list) -> list:
        """
        Sort tasks alphabetically by title
        """
        return sorted(tasks, key=lambda task: task.title.lower())

    def sort_by_creation(self, tasks: list) -> list:
        """
        Sort tasks by creation order (ID)
        """
        return sorted(tasks, key=lambda task: task.id)

    def format_task_display(self, task: Task) -> str:
        """
        Format a task for display including priority and tags
        """
        status = "Complete" if task.completed else "Incomplete"
        tags_str = ", ".join(task.tags) if task.tags else "None"
        return f"[{task.id}] {task.title}\nStatus: {status}\nPriority: {task.priority}\nTags: {tags_str}\n"