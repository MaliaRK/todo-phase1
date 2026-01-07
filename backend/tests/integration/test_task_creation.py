import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from src.main import app
from src.models.task_model import Task
from src.database import engine


client = TestClient(app)


def test_task_creation_integration():
    """Integration test for task creation endpoint"""
    # Create a task via the API
    task_data = {
        "title": "Integration Test Task",
        "description": "Test Description for Integration"
    }

    response = client.post("/api/v1/tasks", json=task_data)

    # Check that the API response is successful
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Integration Test Task"
    assert data["description"] == "Test Description for Integration"
    assert "id" in data

    # Verify the task was actually saved to the database
    with Session(engine) as session:
        created_task = session.get(Task, data["id"])
        assert created_task is not None
        assert created_task.title == "Integration Test Task"
        assert created_task.description == "Test Description for Integration"
        assert created_task.is_completed is False