# Getting Started with Pytest

## Installation

```bash
# With pip
pip install pytest

# With uv
uv add --dev pytest

# With poetry
poetry add --dev pytest
```

## Your First Test

Create a file named `test_example.py`:

```python
def test_passing():
    assert 1 + 1 == 2

def test_failing():
    assert 1 + 1 == 3  # This will fail
```

Run with:

```bash
pytest test_example.py -v
```

## Test Discovery Rules

Pytest automatically discovers tests following these conventions:

| Convention | Example |
|------------|---------|
| Test files | `test_*.py` or `*_test.py` |
| Test functions | `test_*` |
| Test classes | `Test*` (no `__init__` method) |
| Test methods | `test_*` inside `Test*` classes |

## Basic Assertions

```python
# Equality
assert actual == expected
assert actual != unexpected

# Truthiness
assert value
assert not false_value

# Membership
assert item in collection
assert item not in collection

# Identity
assert obj is None
assert obj is not None

# Type checking
assert isinstance(obj, MyClass)
```

## Running Specific Tests

```bash
# Run all tests
pytest

# Run specific file
pytest test_users.py

# Run specific class
pytest test_users.py::TestUserCreation

# Run specific test
pytest test_users.py::TestUserCreation::test_valid_email

# Run tests matching keyword
pytest -k "email"  # Runs tests with "email" in name

# Run tests with specific marker
pytest -m slow
```

## Useful Command Line Options

| Option | Description |
|--------|-------------|
| `-v` | Verbose output |
| `-vv` | More verbose |
| `-q` | Quiet mode |
| `-x` | Stop on first failure |
| `--lf` | Run last failed tests only |
| `--ff` | Run failed tests first |
| `-s` | Show print statements |
| `--tb=short` | Shorter tracebacks |
| `--tb=no` | No tracebacks |
| `-n auto` | Parallel execution (needs pytest-xdist) |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All tests passed |
| 1 | Some tests failed |
| 2 | Test execution interrupted |
| 3 | Internal error |
| 4 | Command line usage error |
| 5 | No tests collected |
