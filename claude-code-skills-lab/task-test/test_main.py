from fastapi.testclient import TestClient

from main import app

# Create a TestClient instance
# This lets us make HTTP requests to our app without running a server
client = TestClient(app)


def test_get_all_tasks():
    """Test that GET /tasks returns a list of tasks."""
    # Make a GET request to /tasks
    response = client.get("/tasks")

    # Check the status code is 200 (OK)
    assert response.status_code == 200

    # Parse the JSON response
    data = response.json()

    # Verify it's a list with 2 items
    assert isinstance(data, list)
    assert len(data) == 2

    # Verify the structure of the first task
    assert data[0]["id"] == 1
    assert data[0]["task"] == "Buy groceries"


def test_get_single_task():
    """Test that GET /tasks/{task_id} returns a single task."""
    # Request task with ID 5
    response = client.get("/tasks/5")

    assert response.status_code == 200

    data = response.json()

    # Verify the task ID matches what we requested
    assert data["id"] == 5
    assert data["task"] == "Buy groceries"
    # Without include_details, there should be no "details" key
    assert "details" not in data


def test_get_task_with_details():
    """Test that include_details=true adds details to response."""
    # Query parameters are passed via params dict
    response = client.get("/tasks/3", params={"include_details": True})

    assert response.status_code == 200

    data = response.json()

    # Now we should have the details field
    assert data["id"] == 3
    assert "details" in data
    assert data["details"] == "Buy groceries for the week"


def test_get_task_invalid_id():
    """Test that task_id < 1 returns an error."""
    response = client.get("/tasks/0")

    assert response.status_code == 200  # Your API returns 200 with error message

    data = response.json()

    # Verify error message is returned
    assert "error" in data
