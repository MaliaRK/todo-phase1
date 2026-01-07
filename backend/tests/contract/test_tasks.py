import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.models.task_model import TaskCreate


client = TestClient(app)


def test_create_task_contract():
    """Contract test for POST /api/v1/tasks"""
    task_data = {
        "title": "Test Task",
        "description": "Test Description"
    }

    response = client.post("/api/v1/tasks", json=task_data)

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert "created_at" in data
    assert "updated_at" in data


def test_get_tasks_contract():
    """Contract test for GET /api/v1/tasks"""
    response = client.get("/api/v1/tasks")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)