---
name: pytest
description: Python testing with pytest framework. Use when writing tests, setting up fixtures, parametrizing test cases, using assertions, mocking, and testing FastAPI/Django/Flask applications. Triggers on test file creation, test debugging, fixture setup, or any pytest-related development task.
---

# Pytest Testing Framework

Write clean, maintainable Python tests with pytest's powerful features.

## Quick Reference

| Task | Reference |
|------|-----------|
| Getting started | [getting-started.md](references/getting-started.md) |
| Fixtures | [fixtures.md](references/fixtures.md) |
| Parametrization | [parametrize.md](references/parametrize.md) |
| Assertions | [assertions.md](references/assertions.md) |
| Mocking | [mocking.md](references/mocking.md) |
| FastAPI testing | [fastapi-testing.md](references/fastapi-testing.md) |

## Core Patterns

### Basic Test Structure

```python
# test_example.py
import pytest

def test_addition():
    """Test names must start with test_"""
    result = 1 + 1
    assert result == 2

class TestMath:
    """Group related tests in classes starting with Test"""

    def test_multiplication(self):
        assert 3 * 4 == 12

    def test_division(self):
        assert 10 / 2 == 5
```

### Fixtures Pattern

```python
import pytest

@pytest.fixture
def sample_user():
    """Fixtures provide reusable test data/setup"""
    return {"id": 1, "name": "John", "email": "john@example.com"}

@pytest.fixture
def db_session():
    """Setup and teardown with yield"""
    session = create_session()
    yield session  # Test runs here
    session.close()  # Cleanup after test

def test_user_name(sample_user):
    """Fixtures are injected by name"""
    assert sample_user["name"] == "John"
```

### Parametrize Pattern

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    (1, 1),
    (2, 4),
    (3, 9),
    (4, 16),
])
def test_square(input, expected):
    """Run same test with multiple inputs"""
    assert input ** 2 == expected

@pytest.mark.parametrize("a,b,expected", [
    pytest.param(1, 2, 3, id="positive"),
    pytest.param(-1, 1, 0, id="mixed"),
    pytest.param(0, 0, 0, id="zeros"),
])
def test_add_with_ids(a, b, expected):
    """Use pytest.param for readable test IDs"""
    assert a + b == expected
```

### Exception Testing

```python
import pytest

def test_raises_exception():
    """Test that code raises expected exception"""
    with pytest.raises(ValueError) as exc_info:
        int("not a number")

    assert "invalid literal" in str(exc_info.value)

def test_raises_with_match():
    """Use match for regex pattern on exception message"""
    with pytest.raises(ValueError, match=r"invalid literal.*base 10"):
        int("abc")
```

## Best Practices

1. **Name tests descriptively** - `test_user_creation_with_valid_email_succeeds`
2. **One assertion per test** - Makes failures clear (flexible rule)
3. **Use fixtures for setup** - Avoid repetition, improve readability
4. **Parametrize similar tests** - Don't copy-paste test functions
5. **Use `pytest.raises`** - For testing exceptions
6. **Scope fixtures appropriately** - `function`, `class`, `module`, `session`
7. **Use `conftest.py`** - Share fixtures across test files
8. **Mark slow tests** - `@pytest.mark.slow` and skip with `-m "not slow"`
9. **Use `tmp_path` fixture** - For tests needing temporary files
10. **Isolate tests** - Each test should be independent

## Running Tests

```bash
# Run all tests
pytest

# Verbose output
pytest -v

# Run specific file
pytest test_example.py

# Run specific test
pytest test_example.py::test_addition

# Run tests matching pattern
pytest -k "user"

# Stop on first failure
pytest -x

# Show print statements
pytest -s

# Run with coverage
pytest --cov=myapp

# Parallel execution (requires pytest-xdist)
pytest -n auto
```

## Project Structure

```
project/
├── src/
│   └── myapp/
│       ├── __init__.py
│       └── core.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py      # Shared fixtures
│   ├── test_core.py
│   └── unit/
│       └── test_utils.py
├── pyproject.toml
└── pytest.ini           # Optional config
```

## Configuration (pyproject.toml)

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "-v --tb=short"
markers = [
    "slow: marks tests as slow",
    "integration: marks integration tests",
]
```
