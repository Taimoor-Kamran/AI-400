import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_todo():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_todo():
    response = client.get("/todo")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "task": "Learn FastAPI"},
        {"id": 2, "task": "Build an API"},
    ]


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
