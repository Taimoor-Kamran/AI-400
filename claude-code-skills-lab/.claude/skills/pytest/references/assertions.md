# Pytest Assertions

Pytest uses plain `assert` statements with enhanced error messages.

## Basic Assertions

```python
# Equality
assert actual == expected
assert actual != unexpected

# Comparison
assert value > 0
assert value >= minimum
assert value < maximum
assert value <= limit

# Truthiness
assert result  # True-like
assert not error  # False-like

# Identity
assert obj is None
assert obj is not None
assert a is b  # Same object

# Membership
assert item in collection
assert item not in collection
assert key in dictionary

# Type checking
assert isinstance(obj, MyClass)
assert isinstance(obj, (str, int))  # Multiple types
```

## Approximate Equality (Floats)

```python
import pytest

# Floating point comparison with tolerance
assert 0.1 + 0.2 == pytest.approx(0.3)

# Custom tolerance
assert result == pytest.approx(expected, rel=1e-3)  # Relative tolerance
assert result == pytest.approx(expected, abs=0.01)  # Absolute tolerance

# With collections
assert [0.1, 0.2] == pytest.approx([0.1, 0.2])
assert {"a": 0.1} == pytest.approx({"a": 0.1})
```

## Testing Exceptions

```python
import pytest

# Basic exception test
def test_raises_value_error():
    with pytest.raises(ValueError):
        int("not a number")

# Check exception message
def test_exception_message():
    with pytest.raises(ValueError) as exc_info:
        int("abc")
    assert "invalid literal" in str(exc_info.value)

# Match with regex
def test_exception_match():
    with pytest.raises(ValueError, match=r"invalid literal.*base 10"):
        int("xyz")

# Multiple exception types
def test_multiple_exceptions():
    with pytest.raises((TypeError, ValueError)):
        some_function()

# Exception attributes
def test_exception_attributes():
    with pytest.raises(CustomError) as exc_info:
        raise CustomError(code=404, message="Not found")
    assert exc_info.value.code == 404
```

## Testing Warnings

```python
import pytest
import warnings

def test_warning_raised():
    with pytest.warns(UserWarning):
        warnings.warn("deprecated", UserWarning)

def test_warning_message():
    with pytest.warns(DeprecationWarning, match="old function"):
        old_function()

def test_multiple_warnings():
    with pytest.warns() as record:
        warnings.warn("first", UserWarning)
        warnings.warn("second", DeprecationWarning)
    assert len(record) == 2
    assert "first" in str(record[0].message)
```

## Collection Assertions

```python
# Lists
assert result == [1, 2, 3]
assert len(result) == 3
assert all(x > 0 for x in result)
assert any(x == 2 for x in result)
assert sorted(result) == [1, 2, 3]

# Sets
assert set(result) == {1, 2, 3}
assert set_a.issubset(set_b)
assert set_a & set_b  # Intersection not empty

# Dictionaries
assert result == {"key": "value"}
assert result.keys() == {"a", "b", "c"}
assert "key" in result
assert result.get("key") == "value"

# Strings
assert "substring" in text
assert text.startswith("Hello")
assert text.endswith("world")
```

## Custom Assertion Messages

```python
# Add context to failures
assert result == expected, f"Expected {expected}, got {result}"

# With more detail
assert user.is_active, f"User {user.id} should be active but has status {user.status}"
```

## Assertion Helpers

Create reusable assertion functions:

```python
def assert_valid_user(user):
    """Custom assertion helper for user validation"""
    assert user is not None, "User should not be None"
    assert user.id > 0, f"User ID should be positive, got {user.id}"
    assert "@" in user.email, f"Invalid email: {user.email}"
    assert len(user.name) > 0, "User name should not be empty"

def test_create_user():
    user = create_user("Alice", "alice@example.com")
    assert_valid_user(user)
```

## Soft Assertions (pytest-check)

Continue testing after assertion failures:

```python
# pip install pytest-check
import pytest_check as check

def test_multiple_conditions():
    result = get_result()

    # All checks run even if some fail
    check.equal(result.status, 200)
    check.is_true(result.success)
    check.is_in("data", result.body)
    check.greater(len(result.items), 0)
```

## Assertion Introspection

Pytest rewrites assertions to show detailed failure info:

```python
def test_complex_comparison():
    data = {"users": [{"name": "Alice", "age": 30}]}
    expected = {"users": [{"name": "Alice", "age": 25}]}
    assert data == expected

# Output shows:
# AssertionError: assert {'users': [{'age': 30, 'name': 'Alice'}]} == {'users': [{'age': 25, 'name': 'Alice'}]}
#   At index 0 diff: {'age': 30, 'name': 'Alice'} != {'age': 25, 'name': 'Alice'}
```

## Disabling Assertion Rewriting

For specific modules if needed:

```python
# In conftest.py
import sys
sys.modules["mymodule"] = None  # Before pytest rewrites it
```

Or via `pytest.ini`:
```ini
[pytest]
addopts = --assert=plain  # Disable globally (not recommended)
```

## Best Practices

1. **One logical assertion per test** - Multiple related `assert` is fine
2. **Use specific assertions** - `assert x == y` not `assert x`
3. **Add messages for context** - Help future debugging
4. **Use `pytest.approx` for floats** - Never use `==` with floats
5. **Test exception messages** - Use `match` parameter
6. **Create assertion helpers** - For complex repeated checks
7. **Avoid `assert True/False`** - Use meaningful conditions
8. **Check state, not implementation** - Assert results, not how they were computed
