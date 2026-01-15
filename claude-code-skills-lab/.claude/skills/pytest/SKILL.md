---
name: pytest
description: Python testing with Pytest best practices. Use when writing, reviewing, or debugging Python tests. Covers fixtures, parametrization, mocking, markers, conftest patterns, and API testing for FastAPI/Flask/Django. Triggers on test file creation, test debugging, fixture design, or any pytest-related task.
---

# Pytest Best Practices

## Quick Reference

```python
# Test file naming: test_*.py or *_test.py
# Test function naming: test_<what>_<condition>_<expected>

def test_user_login_with_valid_credentials_returns_token():
    pass

def test_user_login_with_invalid_password_raises_401():
    pass
```

## Test Structure (AAA Pattern)

```python
def test_calculate_discount_for_premium_user():
    # Arrange
    user = User(tier="premium")
    cart = Cart(total=100)

    # Act
    discount = calculate_discount(user, cart)

    # Assert
    assert discount == 20
```

## Fixtures

Use fixtures for reusable setup. Scope controls lifecycle:

```python
import pytest

@pytest.fixture
def user():
    """Function scope (default) - created for each test."""
    return User(name="test")

@pytest.fixture(scope="module")
def db_connection():
    """Module scope - shared across tests in file."""
    conn = create_connection()
    yield conn
    conn.close()

@pytest.fixture(scope="session")
def app():
    """Session scope - shared across all tests."""
    return create_app(testing=True)
```

For detailed fixture patterns, see [references/fixtures.md](references/fixtures.md).

## Parametrization

Test multiple inputs without duplicating code:

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("", ""),
])
def test_uppercase(input, expected):
    assert input.upper() == expected

# Multiple parameters with IDs
@pytest.mark.parametrize("status,should_retry", [
    pytest.param(500, True, id="server_error"),
    pytest.param(429, True, id="rate_limited"),
    pytest.param(200, False, id="success"),
])
def test_retry_logic(status, should_retry):
    assert should_retry_request(status) == should_retry
```

## Markers

Categorize and control test execution:

```python
# pytest.ini or pyproject.toml
# [tool.pytest.ini_options]
# markers = [
#     "slow: marks tests as slow",
#     "integration: marks integration tests",
# ]

@pytest.mark.slow
def test_full_data_processing():
    pass

@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass

@pytest.mark.skipif(sys.platform == "win32", reason="Unix only")
def test_unix_permissions():
    pass

@pytest.mark.xfail(reason="Known bug #123")
def test_edge_case():
    pass
```

Run specific markers: `pytest -m "not slow"` or `pytest -m integration`

## Mocking

```python
from unittest.mock import Mock, patch, MagicMock

def test_send_email_calls_smtp():
    mock_smtp = Mock()
    send_email(mock_smtp, "test@example.com", "Hello")
    mock_smtp.send.assert_called_once()

@patch("myapp.services.external_api.fetch")
def test_service_handles_api_failure(mock_fetch):
    mock_fetch.side_effect = ConnectionError("timeout")
    result = my_service.process()
    assert result.status == "failed"

# Async mocking
@pytest.mark.asyncio
async def test_async_fetch(mocker):
    mock_response = mocker.patch("aiohttp.ClientSession.get")
    mock_response.return_value.__aenter__.return_value.json = AsyncMock(
        return_value={"data": "test"}
    )
    result = await fetch_data()
    assert result["data"] == "test"
```

For advanced mocking patterns, see [references/mocking.md](references/mocking.md).

## Exception Testing

```python
def test_invalid_input_raises_value_error():
    with pytest.raises(ValueError) as exc_info:
        process_data(None)
    assert "cannot be None" in str(exc_info.value)

def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)
```

## Conftest.py Patterns

Place shared fixtures in `conftest.py`:

```
tests/
├── conftest.py          # Shared fixtures for all tests
├── unit/
│   ├── conftest.py      # Unit test specific fixtures
│   └── test_models.py
└── integration/
    ├── conftest.py      # Integration test fixtures
    └── test_api.py
```

```python
# tests/conftest.py
import pytest

@pytest.fixture
def auth_headers(test_user):
    token = create_token(test_user)
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(autouse=True)
def reset_database(db):
    """Automatically run before each test."""
    db.rollback()
    yield
    db.rollback()
```

## API Testing

For FastAPI, Flask, and Django testing patterns, see [references/api-testing.md](references/api-testing.md).

Quick FastAPI example:

```python
from fastapi.testclient import TestClient

@pytest.fixture
def client(app):
    return TestClient(app)

def test_create_user(client, db_session):
    response = client.post("/users", json={"name": "test", "email": "test@example.com"})
    assert response.status_code == 201
    assert response.json()["name"] == "test"
```

## Async Testing

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await async_fetch_data()
    assert result is not None

# Async fixtures
@pytest.fixture
async def async_client():
    async with AsyncClient(app, base_url="http://test") as client:
        yield client
```

## Best Practices Summary

1. **One assertion concept per test** - test one behavior, multiple asserts OK if related
2. **Descriptive names** - `test_<what>_<condition>_<expected>`
3. **Isolate tests** - no dependencies between tests
4. **Use fixtures** - avoid setup duplication
5. **Prefer `pytest.raises`** - over try/except for exception testing
6. **Use parametrize** - for data-driven tests
7. **Organize with markers** - separate fast/slow, unit/integration
8. **Mock at boundaries** - external APIs, databases, time
