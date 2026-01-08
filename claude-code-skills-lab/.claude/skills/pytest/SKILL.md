---
name: pytest
description: Python testing with pytest. Use when writing tests, debugging test failures, setting up fixtures, parametrizing tests, mocking dependencies, or testing FastAPI/Flask/Django applications. Triggers on test file creation, test debugging, fixture design, or pytest configuration questions.
---

# Pytest

Write effective Python tests with pytest's fixtures, parametrization, and assertions.

## Workflow

1. **Determine test type:**
   - Unit test → Test single function/class in isolation
   - Integration test → Test multiple components together
   - API test → Use TestClient (FastAPI) or test client (Flask/Django)

2. **Choose appropriate pattern:**
   - Simple test → Basic assertions
   - Multiple inputs → Use `@pytest.mark.parametrize`
   - Shared setup → Use fixtures
   - External dependencies → Use mocking

## Quick Patterns

### Basic Test
```python
def test_function_name():
    result = my_function(input)
    assert result == expected
```

### Fixture with Cleanup
```python
@pytest.fixture
def resource():
    obj = create_resource()
    yield obj
    obj.cleanup()
```

### Parametrize
```python
@pytest.mark.parametrize("input,expected", [
    (1, 1),
    (2, 4),
    pytest.param(3, 9, id="three_squared"),
])
def test_square(input, expected):
    assert input ** 2 == expected
```

### Exception Testing
```python
def test_raises():
    with pytest.raises(ValueError, match=r"invalid.*"):
        raise ValueError("invalid input")
```

### FastAPI Testing
```python
from fastapi.testclient import TestClient
client = TestClient(app)

def test_endpoint():
    response = client.get("/items", params={"limit": 10})
    assert response.status_code == 200
```

## References

Detailed guidance for specific topics:

- **Fixtures**: See [references/fixtures.md](references/fixtures.md) for scopes, factories, conftest.py patterns
- **Parametrization**: See [references/parametrize.md](references/parametrize.md) for indirect params, dynamic generation
- **Assertions**: See [references/assertions.md](references/assertions.md) for pytest.approx, custom assertions
- **Mocking**: See [references/mocking.md](references/mocking.md) for patch, monkeypatch, pytest-mock
- **FastAPI Testing**: See [references/fastapi-testing.md](references/fastapi-testing.md) for dependency overrides, async tests

## Best Practices

1. **Name tests descriptively** - `test_create_user_with_invalid_email_returns_422`
2. **One concept per test** - Easier to debug failures
3. **Use fixtures for shared setup** - Avoid repetition
4. **Parametrize similar tests** - Don't copy-paste
5. **Scope fixtures appropriately** - `function` (default), `class`, `module`, `session`
6. **Put shared fixtures in conftest.py** - Auto-discovered, no imports needed
7. **Use `pytest.raises` with match** - Verify exception messages
8. **Prefer `pytest.approx` for floats** - Never use `==` with floats

## Running Tests

```bash
pytest                      # All tests
pytest -v                   # Verbose
pytest -x                   # Stop on first failure
pytest -k "user"            # Tests matching pattern
pytest --lf                 # Last failed only
pytest -s                   # Show print output
pytest --cov=myapp          # With coverage
```

## Configuration (pyproject.toml)

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --tb=short"
markers = ["slow: slow tests", "integration: integration tests"]
```
