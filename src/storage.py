"""
In-memory storage for the Todo Application CLI
"""
from typing import Dict, List, Optional
from .models import Task


class InMemoryStorage:
    """
    In-memory storage for tasks with auto-incrementing ID generation
    """
    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(self, task: Task) -> Task:
        """
        Add a task to storage with auto-generated ID
        """
        task.id = self._next_id
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by ID
        """
        return self._tasks.get(task_id)

    def update_task(self, task_id: int, updated_task: Task) -> Optional[Task]:
        """
        Update a task by ID
        """
        if task_id not in self._tasks:
            return None

        updated_task.id = task_id  # Preserve the original ID
        self._tasks[task_id] = updated_task
        return updated_task

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by ID
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def list_tasks(self) -> List[Task]:
        """
        Return all tasks in storage
        """
        return list(self._tasks.values())

    def get_next_id(self) -> int:
        """
        Get the next available ID (for internal use)
        """
        return self._next_id