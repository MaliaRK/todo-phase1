"""
Utility functions for the Todo Application CLI
"""


class TaskError(Exception):
    """Base exception for task-related errors"""
    pass


class TaskNotFoundError(TaskError):
    """Raised when a task is not found"""
    pass


class InvalidTaskError(TaskError):
    """Raised when a task is invalid"""
    pass


class ValidationError(Exception):
    """Raised when validation fails"""
    pass


def validate_task_content(title: str, description: str = None) -> None:
    """
    Validate task content according to specifications
    """
    if not title or not title.strip():
        raise ValidationError("Task title cannot be empty")

    if len(title) > 200:
        raise ValidationError("Task title cannot exceed 200 characters")

    if description and len(description) > 1000:
        raise ValidationError("Task description cannot exceed 1000 characters")


def validate_task_id(task_id: int) -> None:
    """
    Validate that a task ID is valid
    """
    if not isinstance(task_id, int) or task_id <= 0:
        raise ValidationError("Task ID must be a positive integer")