# Testing FastAPI Applications

Test FastAPI endpoints using pytest and TestClient.

## Setup

```bash
# Install dependencies
uv add --dev pytest httpx

# Or with pip
pip install pytest httpx
```

## Basic Testing

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

# Create test client
client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
```

## Test File Structure

```python
# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestUsers:
    def test_list_users(self):
        response = client.get("/users")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_create_user(self):
        response = client.post(
            "/users",
            json={"name": "Alice", "email": "alice@example.com"}
        )
        assert response.status_code == 201
        assert response.json()["name"] == "Alice"
```

## Testing HTTP Methods

```python
# GET request
response = client.get("/items")
response = client.get("/items/123")
response = client.get("/items", params={"skip": 0, "limit": 10})

# POST request
response = client.post("/items", json={"name": "Item", "price": 9.99})

# PUT request
response = client.put("/items/123", json={"name": "Updated"})

# PATCH request
response = client.patch("/items/123", json={"price": 19.99})

# DELETE request
response = client.delete("/items/123")
```

## Testing with Query Parameters

```python
@app.get("/search")
def search(q: str, limit: int = 10):
    return {"query": q, "limit": limit}

def test_search_with_params():
    response = client.get("/search", params={"q": "python", "limit": 5})
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "python"
    assert data["limit"] == 5
```

## Testing with Path Parameters

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}

def test_get_user():
    response = client.get("/users/42")
    assert response.status_code == 200
    assert response.json()["user_id"] == 42

def test_invalid_user_id():
    response = client.get("/users/invalid")
    assert response.status_code == 422  # Validation error
```

## Testing with Request Body

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

@app.post("/items")
def create_item(item: Item):
    return {"id": 1, **item.model_dump()}

def test_create_item():
    response = client.post(
        "/items",
        json={"name": "Widget", "price": 29.99}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Widget"
    assert data["price"] == 29.99

def test_invalid_item():
    response = client.post(
        "/items",
        json={"name": "Widget"}  # Missing price
    )
    assert response.status_code == 422
```

## Testing with Headers

```python
@app.get("/protected")
def protected(x_token: str = Header()):
    return {"token": x_token}

def test_with_headers():
    response = client.get(
        "/protected",
        headers={"X-Token": "secret-token"}
    )
    assert response.status_code == 200

def test_missing_header():
    response = client.get("/protected")
    assert response.status_code == 422
```

## Testing Authentication

```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/users/me")
def get_current_user(token: str = Depends(oauth2_scheme)):
    return {"token": token}

def test_authenticated_endpoint():
    response = client.get(
        "/users/me",
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 200

def test_unauthenticated():
    response = client.get("/users/me")
    assert response.status_code == 401
```

## Using Fixtures

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
def test_protected_route(client, auth_headers):
    response = client.get("/protected", headers=auth_headers)
    assert response.status_code == 200
```

## Testing with Database

```python
# conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from main import app, get_db
from database import Base

# Use SQLite for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
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

## Dependency Overrides

```python
from main import app, get_settings

def get_settings_override():
    return Settings(api_key="test-key", debug=True)

@pytest.fixture
def client():
    app.dependency_overrides[get_settings] = get_settings_override
    yield TestClient(app)
    app.dependency_overrides.clear()
```

## Testing Async Endpoints

```python
import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_async_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/async-endpoint")
        assert response.status_code == 200
```

## Testing File Uploads

```python
@app.post("/upload")
def upload_file(file: UploadFile):
    return {"filename": file.filename}

def test_file_upload():
    response = client.post(
        "/upload",
        files={"file": ("test.txt", b"file content", "text/plain")}
    )
    assert response.status_code == 200
    assert response.json()["filename"] == "test.txt"
```

## Testing WebSockets

```python
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive_text()
    await websocket.send_text(f"Echo: {data}")

def test_websocket():
    with client.websocket_connect("/ws") as websocket:
        websocket.send_text("Hello")
        data = websocket.receive_text()
        assert data == "Echo: Hello"
```

## Common Assertions

```python
def test_comprehensive(client):
    response = client.get("/items")

    # Status code
    assert response.status_code == 200

    # Response type
    assert response.headers["content-type"] == "application/json"

    # JSON body
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    # Specific fields
    item = data[0]
    assert "id" in item
    assert "name" in item
    assert item["id"] > 0
```

## Best Practices

1. **Use fixtures** - Share TestClient and test data
2. **Override dependencies** - Use test databases and mocked services
3. **Test validation** - Verify 422 responses for invalid data
4. **Test authentication** - Both authenticated and unauthenticated requests
5. **Use descriptive names** - `test_create_user_with_invalid_email_returns_422`
6. **Isolate tests** - Each test should be independent
7. **Clean up** - Use fixtures with teardown for database tests
8. **Test error cases** - 404, 401, 403, 500 responses
