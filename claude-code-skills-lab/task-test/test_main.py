"""
Test suite for Tasks API following Pytest Best Practices.

Best Practices Applied (from pytest skill):
- Test naming: test_<what>_<condition>_<expected>
- AAA Pattern: Arrange, Act, Assert
- Fixtures for reusable setup
- Parametrization for multiple inputs
- Organized test structure with classes
- One assertion concept per test
"""

import pytest
from fastapi.testclient import TestClient

from main import app


# ============================================================================
# FIXTURES - Reusable test setup (from references/fixtures.md)
# ============================================================================

@pytest.fixture
def client():
    """Function scope fixture - create TestClient for each test."""
    return TestClient(app)


@pytest.fixture
def expected_tasks():
    """Return expected task list for validation."""
    return [
        {"id": 1, "task": "Buy groceries"},
        {"id": 2, "task": "Read a book"}
    ]


@pytest.fixture
def make_task_request(client):
    """Factory fixture for making task requests with custom parameters."""
    def _make_request(task_id: int, include_details: bool = False):
        params = {"include_details": include_details} if include_details else {}
        return client.get(f"/tasks/{task_id}", params=params)
    return _make_request


# ============================================================================
# TEST CLASS: GET /tasks endpoint
# ============================================================================

class TestGetAllTasks:
    """Tests for GET /tasks endpoint."""

    def test_get_tasks_returns_200_status(self, client):
        """GET /tasks with valid request returns 200 status code."""
        # Arrange - client fixture provides TestClient

        # Act
        response = client.get("/tasks")

        # Assert
        assert response.status_code == 200

    def test_get_tasks_returns_list_type(self, client):
        """GET /tasks returns response as list type."""
        # Act
        response = client.get("/tasks")
        data = response.json()

        # Assert
        assert isinstance(data, list)

    def test_get_tasks_returns_correct_count(self, client, expected_tasks):
        """GET /tasks returns expected number of tasks."""
        # Act
        response = client.get("/tasks")
        data = response.json()

        # Assert
        assert len(data) == len(expected_tasks)

    def test_get_tasks_contains_required_fields(self, client):
        """GET /tasks response items contain id and task fields."""
        # Act
        response = client.get("/tasks")
        data = response.json()

        # Assert
        for task in data:
            assert "id" in task
            assert "task" in task

    def test_get_tasks_returns_expected_content(self, client, expected_tasks):
        """GET /tasks returns matching task data."""
        # Act
        response = client.get("/tasks")
        data = response.json()

        # Assert
        assert data == expected_tasks

    def test_get_tasks_returns_json_content_type(self, client):
        """GET /tasks response has application/json content type."""
        # Act
        response = client.get("/tasks")

        # Assert
        assert "application/json" in response.headers.get("content-type", "")


# ============================================================================
# TEST CLASS: GET /tasks/{task_id} endpoint
# ============================================================================

class TestGetSingleTask:
    """Tests for GET /tasks/{task_id} endpoint."""

    def test_get_task_with_valid_id_returns_200(self, client):
        """GET /tasks/{task_id} with valid ID returns 200 status."""
        # Act
        response = client.get("/tasks/1")

        # Assert
        assert response.status_code == 200

    def test_get_task_returns_dict_type(self, client):
        """GET /tasks/{task_id} returns dictionary response."""
        # Act
        response = client.get("/tasks/1")
        data = response.json()

        # Assert
        assert isinstance(data, dict)

    def test_get_task_contains_required_fields(self, client):
        """GET /tasks/{task_id} response contains id and task fields."""
        # Act
        response = client.get("/tasks/1")
        data = response.json()

        # Assert
        assert "id" in data
        assert "task" in data

    def test_get_task_id_matches_request(self, client):
        """GET /tasks/{task_id} returns task with matching ID."""
        # Arrange
        task_id = 5

        # Act
        response = client.get(f"/tasks/{task_id}")
        data = response.json()

        # Assert
        assert data["id"] == task_id

    def test_get_task_without_details_excludes_details_field(self, client):
        """GET /tasks/{task_id} without include_details omits details field."""
        # Act
        response = client.get("/tasks/1")
        data = response.json()

        # Assert
        assert "details" not in data

    # Parametrized test for multiple valid IDs (from SKILL.md)
    @pytest.mark.parametrize("task_id", [1, 5, 10, 100, 999])
    def test_get_task_with_various_valid_ids_returns_matching_id(self, client, task_id):
        """GET /tasks/{task_id} with various valid IDs returns correct ID."""
        # Act
        response = client.get(f"/tasks/{task_id}")
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert data["id"] == task_id


# ============================================================================
# TEST CLASS: Query Parameters (include_details)
# ============================================================================

class TestTaskDetails:
    """Tests for include_details query parameter."""

    def test_include_details_true_adds_details_field(self, client):
        """GET /tasks/{id}?include_details=true includes details field."""
        # Act
        response = client.get("/tasks/1", params={"include_details": True})
        data = response.json()

        # Assert
        assert "details" in data

    def test_include_details_false_excludes_details_field(self, client):
        """GET /tasks/{id}?include_details=false omits details field."""
        # Act
        response = client.get("/tasks/1", params={"include_details": False})
        data = response.json()

        # Assert
        assert "details" not in data

    def test_include_details_returns_expected_content(self, client):
        """GET /tasks/{id}?include_details=true returns correct details content."""
        # Act
        response = client.get("/tasks/1", params={"include_details": True})
        data = response.json()

        # Assert
        assert data["details"] == "Buy groceries for the week"

    def test_include_details_response_has_all_fields(self, client):
        """GET /tasks/{id}?include_details=true has id, task, and details."""
        # Act
        response = client.get("/tasks/1", params={"include_details": True})
        data = response.json()

        # Assert
        assert "id" in data
        assert "task" in data
        assert "details" in data

    # Parametrized test with IDs for better test identification
    @pytest.mark.parametrize("include_details,has_details", [
        pytest.param(True, True, id="include_details_true"),
        pytest.param(False, False, id="include_details_false"),
        pytest.param("true", True, id="include_details_string_true"),
        pytest.param("false", False, id="include_details_string_false"),
    ])
    def test_include_details_parameter_variations(self, client, include_details, has_details):
        """GET /tasks/{id} handles various include_details values correctly."""
        # Act
        response = client.get("/tasks/1", params={"include_details": include_details})
        data = response.json()

        # Assert
        assert ("details" in data) == has_details


# ============================================================================
# TEST CLASS: Error Handling & Edge Cases
# ============================================================================

class TestErrorHandling:
    """Tests for error handling and edge cases."""

    def test_get_task_with_zero_id_returns_error(self, client):
        """GET /tasks/0 returns error response."""
        # Act
        response = client.get("/tasks/0")
        data = response.json()

        # Assert
        assert "error" in data

    def test_get_task_error_response_has_message(self, client):
        """GET /tasks/0 error response contains message text."""
        # Act
        response = client.get("/tasks/0")
        data = response.json()

        # Assert
        assert "error" in data
        assert len(data["error"]) > 0

    def test_get_task_error_response_excludes_task_fields(self, client):
        """GET /tasks/0 error response omits id and task fields."""
        # Act
        response = client.get("/tasks/0")
        data = response.json()

        # Assert
        assert "id" not in data
        assert "task" not in data

    # Parametrized test for invalid IDs
    @pytest.mark.parametrize("invalid_id", [
        pytest.param(0, id="zero"),
        pytest.param(-1, id="negative_one"),
        pytest.param(-100, id="large_negative"),
    ])
    def test_get_task_with_invalid_id_returns_error(self, client, invalid_id):
        """GET /tasks/{invalid_id} with non-positive ID returns error."""
        # Act
        response = client.get(f"/tasks/{invalid_id}")
        data = response.json()

        # Assert
        assert "error" in data


# ============================================================================
# TEST CLASS: Boundary Conditions
# ============================================================================

class TestBoundaryConditions:
    """Tests for boundary conditions."""

    def test_task_id_one_is_valid_boundary(self, client):
        """GET /tasks/1 (boundary value) is valid and returns task."""
        # Act
        response = client.get("/tasks/1")
        data = response.json()

        # Assert
        assert "error" not in data
        assert data["id"] == 1

    def test_task_id_zero_is_invalid_boundary(self, client):
        """GET /tasks/0 (boundary value) is invalid and returns error."""
        # Act
        response = client.get("/tasks/0")
        data = response.json()

        # Assert
        assert "error" in data

    def test_large_task_id_is_valid(self, client):
        """GET /tasks/{large_id} handles large ID correctly."""
        # Arrange
        large_id = 999999

        # Act
        response = client.get(f"/tasks/{large_id}")
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert data["id"] == large_id


# ============================================================================
# TEST CLASS: HTTP Methods (from references/api-testing.md)
# ============================================================================

class TestHTTPMethods:
    """Tests for HTTP method handling."""

    def test_tasks_endpoint_get_method_allowed(self, client):
        """GET method on /tasks returns 200."""
        # Act
        response = client.get("/tasks")

        # Assert
        assert response.status_code == 200

    def test_tasks_endpoint_post_method_not_allowed(self, client):
        """POST method on /tasks returns 405 Method Not Allowed."""
        # Act
        response = client.post("/tasks", json={})

        # Assert
        assert response.status_code == 405

    def test_tasks_endpoint_put_method_not_allowed(self, client):
        """PUT method on /tasks returns 405 Method Not Allowed."""
        # Act
        response = client.put("/tasks", json={})

        # Assert
        assert response.status_code == 405

    def test_tasks_endpoint_delete_method_not_allowed(self, client):
        """DELETE method on /tasks returns 405 Method Not Allowed."""
        # Act
        response = client.delete("/tasks")

        # Assert
        assert response.status_code == 405

    def test_single_task_endpoint_get_method_allowed(self, client):
        """GET method on /tasks/{id} returns 200."""
        # Act
        response = client.get("/tasks/1")

        # Assert
        assert response.status_code == 200

    def test_single_task_endpoint_post_method_not_allowed(self, client):
        """POST method on /tasks/{id} returns 405 Method Not Allowed."""
        # Act
        response = client.post("/tasks/1", json={})

        # Assert
        assert response.status_code == 405


# ============================================================================
# TEST CLASS: Using Factory Fixture
# ============================================================================

class TestWithFactoryFixture:
    """Tests demonstrating factory fixture pattern."""

    def test_factory_fixture_with_default_params(self, make_task_request):
        """Factory fixture creates valid request with defaults."""
        # Act
        response = make_task_request(task_id=1)
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert data["id"] == 1
        assert "details" not in data

    def test_factory_fixture_with_details_enabled(self, make_task_request):
        """Factory fixture handles include_details parameter."""
        # Act
        response = make_task_request(task_id=1, include_details=True)
        data = response.json()

        # Assert
        assert "details" in data
