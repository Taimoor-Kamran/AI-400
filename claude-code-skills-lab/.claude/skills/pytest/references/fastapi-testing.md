# FastAPI Testing

## Setup

```bash
uv add --dev pytest httpx
```

## Basic Pattern

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_items():
    response = client.get("/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

## HTTP Methods

```python
# GET with query params
response = client.get("/search", params={"q": "python", "limit": 10})

# POST with JSON body
response = client.post("/items", json={"name": "Item", "price": 9.99})

# With headers
response = client.get("/protected", headers={"Authorization": "Bearer token"})

# With path params
response = client.get("/items/123")
```

## Fixtures

```python
# conftest.py
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def auth_headers():
    return {"Authorization": "Bearer test-token"}

# test_api.py
def test_protected(client, auth_headers):
    response = client.get("/me", headers=auth_headers)
    assert response.status_code == 200
```

## Dependency Overrides

Replace dependencies for testing:

```python
from main import app, get_db, get_current_user

# Override database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Override auth
def override_get_current_user():
    return User(id=1, name="Test User")

@pytest.fixture
def client():
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    yield TestClient(app)
    app.dependency_overrides.clear()
```

## Database Testing

```python
# conftest.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)
```

## Async Testing

```python
import pytest
from httpx import AsyncClient, ASGITransport

@pytest.mark.asyncio
async def test_async_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/async-endpoint")
        assert response.status_code == 200
```

## File Uploads

```python
def test_upload():
    response = client.post(
        "/upload",
        files={"file": ("test.txt", b"content", "text/plain")}
    )
    assert response.status_code == 200
```

## WebSocket Testing

```python
def test_websocket():
    with client.websocket_connect("/ws") as ws:
        ws.send_text("hello")
        data = ws.receive_text()
        assert data == "Echo: hello"
```

## Common Assertions

```python
def test_crud(client):
    # Create
    response = client.post("/items", json={"name": "Test"})
    assert response.status_code == 201
    item_id = response.json()["id"]

    # Read
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test"

    # Update
    response = client.put(f"/items/{item_id}", json={"name": "Updated"})
    assert response.status_code == 200

    # Delete
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 204

    # Verify deleted
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 404
```
