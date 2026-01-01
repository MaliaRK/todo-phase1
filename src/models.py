"""
Data models for the Todo Application CLI
"""
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Task:
    """
    Represents a single todo task
    """
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str = "Medium"  # High, Medium, Low
    tags: List[str] = None

    def __post_init__(self):
        """Validate the task after initialization"""
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")

        if len(self.title) > 200:
            raise ValueError("Task title cannot exceed 200 characters")

        if self.description and len(self.description) > 1000:
            raise ValueError("Task description cannot exceed 1000 characters")

        # Validate priority
        if self.priority not in ["High", "Medium", "Low"]:
            raise ValueError("Priority must be one of: High, Medium, Low")

        # Initialize tags as empty list if None
        if self.tags is None:
            self.tags = []

    def __str__(self):
        """String representation of the task including priority and tags"""
        status = "✓" if self.completed else "○"
        tags_str = ", ".join(self.tags) if self.tags else "None"
        return f"[{self.id}] {status} {self.title}\nStatus: {'Complete' if self.completed else 'Incomplete'}\nPriority: {self.priority}\nTags: {tags_str}"