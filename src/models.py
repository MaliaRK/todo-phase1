"""
Data models for the Todo Application CLI
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    """
    Represents a single todo task
    """
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

    def __post_init__(self):
        """Validate the task after initialization"""
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")

        if len(self.title) > 200:
            raise ValueError("Task title cannot exceed 200 characters")

        if self.description and len(self.description) > 1000:
            raise ValueError("Task description cannot exceed 1000 characters")