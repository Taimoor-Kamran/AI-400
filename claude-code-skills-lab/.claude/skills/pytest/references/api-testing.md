# API Testing Patterns

## Table of Contents
- [FastAPI Testing](#fastapi-testing)
- [Flask Testing](#flask-testing)
- [Django Testing](#django-testing)
- [Common Patterns](#common-patterns)

## FastAPI Testing

### Basic Setup

```python
import pytest
from fastapi.testclient import TestClient
from myapp.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
```

### Database Override

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from myapp.database import get_db, Base

SQLALCHEMY_TEST_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_TEST_URL)
TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
```

### Async Testing

```python
import pytest
from httpx import AsyncClient
from myapp.main import app

@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_async_endpoint(async_client):
    response = await async_client.get("/async-data")
    assert response.status_code == 200
```

### Authentication Testing

```python
@pytest.fixture
def auth_headers(test_user):
    from myapp.auth import create_access_token
    token = create_access_token({"sub": test_user.email})
    return {"Authorization": f"Bearer {token}"}

def test_protected_endpoint(client, auth_headers):
    response = client.get("/protected", headers=auth_headers)
    assert response.status_code == 200

def test_unauthorized_access(client):
    response = client.get("/protected")
    assert response.status_code == 401
```

## Flask Testing

### Basic Setup

```python
import pytest
from myapp import create_app

@pytest.fixture
def app():
    app = create_app({"TESTING": True})
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
```

### Database Testing

```python
@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def db_session(app):
    with app.app_context():
        yield db.session
        db.session.rollback()
```

### Request Context

```python
def test_with_request_context(app):
    with app.test_request_context("/path", method="POST"):
        assert request.path == "/path"
        assert request.method == "POST"
```

## Django Testing

### Basic Setup

```python
import pytest
from django.test import Client

@pytest.fixture
def client():
    return Client()

@pytest.mark.django_db
def test_view(client):
    response = client.get("/api/items/")
    assert response.status_code == 200
```

### Django REST Framework

```python
import pytest
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.mark.django_db
def test_create_item(authenticated_client):
    response = authenticated_client.post(
        "/api/items/",
        {"name": "test"},
        format="json"
    )
    assert response.status_code == 201
```

### Model Testing

```python
import pytest
from myapp.models import User

@pytest.mark.django_db
def test_user_creation():
    user = User.objects.create_user(
        username="test",
        email="test@example.com",
        password="password123"
    )
    assert user.pk is not None
    assert user.check_password("password123")
```

## Common Patterns

### Testing CRUD Operations

```python
class TestUserAPI:
    def test_create_user(self, client):
        response = client.post("/users", json={
            "name": "test",
            "email": "test@example.com"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "test"
        assert "id" in data

    def test_read_user(self, client, user):
        response = client.get(f"/users/{user.id}")
        assert response.status_code == 200
        assert response.json()["id"] == user.id

    def test_update_user(self, client, user):
        response = client.put(
            f"/users/{user.id}",
            json={"name": "updated"}
        )
        assert response.status_code == 200
        assert response.json()["name"] == "updated"

    def test_delete_user(self, client, user):
        response = client.delete(f"/users/{user.id}")
        assert response.status_code == 204

        response = client.get(f"/users/{user.id}")
        assert response.status_code == 404
```

### Testing Error Responses

```python
@pytest.mark.parametrize("payload,expected_status,expected_error", [
    ({}, 422, "field required"),
    ({"email": "invalid"}, 422, "invalid email"),
    ({"email": "test@example.com", "name": ""}, 422, "empty"),
])
def test_validation_errors(client, payload, expected_status, expected_error):
    response = client.post("/users", json=payload)
    assert response.status_code == expected_status
    assert expected_error in response.text.lower()
```

### Testing Pagination

```python
def test_pagination(client, create_users):
    create_users(25)  # Create 25 users

    response = client.get("/users?page=1&per_page=10")
    data = response.json()

    assert len(data["items"]) == 10
    assert data["total"] == 25
    assert data["page"] == 1
    assert data["pages"] == 3
```

### Testing File Uploads

```python
def test_file_upload(client):
    from io import BytesIO

    file_content = b"test file content"
    data = {
        "file": (BytesIO(file_content), "test.txt")
    }

    response = client.post(
        "/upload",
        files=data
    )

    assert response.status_code == 200
    assert response.json()["filename"] == "test.txt"
```

### Testing WebSockets (FastAPI)

```python
def test_websocket(client):
    with client.websocket_connect("/ws") as websocket:
        websocket.send_json({"message": "hello"})
        data = websocket.receive_json()
        assert data["message"] == "hello"
```
