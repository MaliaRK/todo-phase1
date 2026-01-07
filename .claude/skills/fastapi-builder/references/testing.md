# FastAPI Testing Guide

## Unit Testing with Pytest

### Basic Test Setup

```python
# conftest.py
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
```

### Testing Endpoints

```python
# test_main.py
def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}

def test_create_item(client):
    item_data = {
        "name": "Test Item",
        "description": "A test item",
        "price": 10.5,
        "tax": 1.5
    }
    response = client.post("/items/", json=item_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Item"
```

## Testing with Database

### Test Database Configuration

```python
# test_database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
```

### Testing with Database Dependencies

```python
# test_items.py
from fastapi.testclient import TestClient
from main import app, get_db
from test_database import override_get_db

app.dependency_overrides[get_db] = override_get_db

def test_create_item_with_db():
    client = TestClient(app)
    item_data = {
        "name": "Test Item",
        "description": "A test item",
        "price": 10.5,
        "tax": 1.5
    }
    response = client.post("/items/", json=item_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert "id" in data
```

## Testing Dependencies

### Mocking Dependencies

```python
# test_auth.py
from unittest.mock import Mock
from fastapi.testclient import TestClient
from main import app
from dependencies import get_current_user

def test_protected_route_with_mock():
    # Create a mock user
    mock_user = {"username": "testuser", "id": 1}

    # Override the dependency
    app.dependency_overrides[get_current_user] = lambda: mock_user

    client = TestClient(app)
    response = client.get("/protected/")
    assert response.status_code == 200
    assert response.json()["user"] == mock_user

    # Clean up
    app.dependency_overrides.clear()
```

## Pydantic Model Testing

```python
# test_models.py
import pytest
from pydantic import ValidationError
from models import Item

def test_item_model_validation():
    # Valid item
    item = Item(name="Test Item", price=10.5)
    assert item.name == "Test Item"
    assert item.price == 10.5

def test_item_model_validation_error():
    # Invalid price (negative)
    with pytest.raises(ValidationError):
        Item(name="Test Item", price=-10.5)

def test_item_model_field_constraints():
    # Test field constraints
    with pytest.raises(ValidationError):
        Item(name="", price=10.5)  # Empty name
```

## Async Testing

```python
# test_async.py
import pytest
import asyncio
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_async_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/async-endpoint/")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_async_post_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/items/", json={
            "name": "Async Test",
            "price": 15.99
        })
    assert response.status_code == 200
    assert response.json()["name"] == "Async Test"
```

## Testing Background Tasks

```python
# test_background_tasks.py
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from main import app

def test_background_task():
    with patch('main.send_notification_email') as mock_send:
        client = TestClient(app)

        response = client.post("/users/", json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "password123"
        })

        assert response.status_code == 200
        # Verify the background task was called
        mock_send.assert_called_once()
```

## Testing Exception Handlers

```python
# test_exceptions.py
def test_custom_exception_handler(client):
    response = client.get("/error-test/")
    assert response.status_code == 418  # Custom error status
    assert "error" in response.json()
```

## Testing Security

### Testing Authentication

```python
# test_security.py
from jose import jwt
from main import SECRET_KEY, ALGORITHM

def create_test_token(username: str):
    data = {"sub": username}
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def test_protected_endpoint_with_token(client):
    token = create_test_token("testuser")
    response = client.get(
        "/protected/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

def test_protected_endpoint_without_token(client):
    response = client.get("/protected/")
    assert response.status_code == 401
```

## Comprehensive Test Example

```python
# test_comprehensive.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from models import User
from main import app
from database import get_db

class TestUserAPI:
    def setup_method(self):
        # Setup test database
        self.client = TestClient(app)

    def test_create_user(self):
        response = self.client.post("/users/", json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "password123"
        })

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["username"] == "testuser"
        assert "id" in data

    def test_get_user(self):
        # First create a user
        create_response = self.client.post("/users/", json={
            "email": "get@example.com",
            "username": "getuser",
            "password": "password123"
        })

        user_id = create_response.json()["id"]

        # Then get the user
        response = self.client.get(f"/users/{user_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "get@example.com"

    @pytest.mark.parametrize("email,password,expected_status", [
        ("invalid-email", "password123", 422),  # Invalid email
        ("test@example.com", "short", 422),    # Short password
        ("valid@example.com", "password123", 200),  # Valid
    ])
    def test_user_creation_validation(self, email, password, expected_status):
        response = self.client.post("/users/", json={
            "email": email,
            "username": "testuser",
            "password": password
        })
        assert response.status_code == expected_status

# Performance testing
def test_endpoint_performance(client):
    import time

    start_time = time.time()
    response = client.get("/")
    end_time = time.time()

    # Ensure response time is under 100ms
    assert (end_time - start_time) < 0.1
    assert response.status_code == 200
```

## Test Configuration

### pytest.ini

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --tb=short
    --strict-markers
    --mypy
    --cov=app
    --cov-report=html
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

### Makefile for Testing

```makefile
.PHONY: test test-unit test-integration coverage

test:
	pytest tests/

test-unit:
	pytest tests/ -m "unit"

test-integration:
	pytest tests/ -m "integration"

coverage:
	pytest --cov=app --cov-report=html tests/