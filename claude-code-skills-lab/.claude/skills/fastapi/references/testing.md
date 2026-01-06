# FastAPI Testing

## Basic Test Setup

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db):
    def override_get_db():
        yield db
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
```

## Basic Tests

```python
# tests/test_users.py
def test_create_user(client):
    response = client.post("/users", json={"email": "test@example.com", "password": "secret123"})
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_get_user(client, db):
    # Setup
    user = User(email="test@example.com", hashed_password="xxx")
    db.add(user)
    db.commit()

    # Test
    response = client.get(f"/users/{user.id}")
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

def test_get_user_not_found(client):
    response = client.get("/users/999")
    assert response.status_code == 404
```

## Async Tests

```python
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_async_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/items")
        assert response.status_code == 200
```

## Testing with Authentication

```python
@pytest.fixture
def auth_client(client, db):
    # Create user
    user = User(email="test@example.com", hashed_password=hash_password("password"))
    db.add(user)
    db.commit()

    # Get token
    response = client.post("/token", data={"username": "test@example.com", "password": "password"})
    token = response.json()["access_token"]

    client.headers["Authorization"] = f"Bearer {token}"
    return client

def test_protected_endpoint(auth_client):
    response = auth_client.get("/users/me")
    assert response.status_code == 200
```

## Mocking Dependencies

```python
from unittest.mock import Mock, AsyncMock

def test_with_mocked_service(client):
    mock_service = Mock()
    mock_service.get_user.return_value = User(id=1, email="test@example.com")

    app.dependency_overrides[get_user_service] = lambda: mock_service

    response = client.get("/users/1")
    assert response.status_code == 200
    mock_service.get_user.assert_called_once_with(1)

    app.dependency_overrides.clear()
```

## Testing File Uploads

```python
def test_upload_file(client):
    response = client.post(
        "/upload",
        files={"file": ("test.txt", b"file content", "text/plain")}
    )
    assert response.status_code == 200
    assert response.json()["filename"] == "test.txt"
```

## Testing WebSockets

```python
def test_websocket(client):
    with client.websocket_connect("/ws") as websocket:
        websocket.send_json({"message": "hello"})
        data = websocket.receive_json()
        assert data["message"] == "hello"
```

## Parametrized Tests

```python
@pytest.mark.parametrize("email,password,expected_status", [
    ("valid@example.com", "password123", 201),
    ("invalid-email", "password123", 422),
    ("valid@example.com", "short", 422),
])
def test_create_user_validation(client, email, password, expected_status):
    response = client.post("/users", json={"email": email, "password": password})
    assert response.status_code == expected_status
```
