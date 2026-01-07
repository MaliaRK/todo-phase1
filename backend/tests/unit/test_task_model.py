import pytest
from src.models.task_model import Task, TaskCreate


def test_task_creation():
    """Test creating a task with valid data"""
    task_data = TaskCreate(title="Test Task", description="Test Description")
    task = Task.model_validate(task_data)

    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.is_completed is False


def test_task_creation_required_fields():
    """Test creating a task with only required fields"""
    task_data = TaskCreate(title="Test Task")
    task = Task.model_validate(task_data)

    assert task.title == "Test Task"
    assert task.description is None
    assert task.is_completed is False


def test_task_title_validation():
    """Test task title validation"""
    # This would normally test the validation constraints
    # For now, just test that we can create a task with a valid title
    task_data = TaskCreate(title="Valid Title")
    task = Task.model_validate(task_data)

    assert task.title == "Valid Title"