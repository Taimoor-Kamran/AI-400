# Assertions

## Float Comparison

Never use `==` with floats. Use `pytest.approx`:

```python
assert 0.1 + 0.2 == pytest.approx(0.3)
assert result == pytest.approx(expected, rel=1e-3)  # Relative tolerance
assert result == pytest.approx(expected, abs=0.01)  # Absolute tolerance

# Works with collections
assert [0.1, 0.2] == pytest.approx([0.1, 0.2])
assert {"a": 0.1} == pytest.approx({"a": 0.1})
```

## Exception Testing

```python
# Basic
with pytest.raises(ValueError):
    int("not a number")

# With message check
with pytest.raises(ValueError, match=r"invalid literal.*base 10"):
    int("abc")

# Access exception details
with pytest.raises(CustomError) as exc_info:
    raise CustomError(code=404)
assert exc_info.value.code == 404

# Multiple exception types
with pytest.raises((TypeError, ValueError)):
    risky_function()
```

## Warning Testing

```python
with pytest.warns(DeprecationWarning):
    deprecated_function()

with pytest.warns(UserWarning, match="will be removed"):
    warn_function()

# Capture multiple warnings
with pytest.warns() as record:
    multiple_warnings()
assert len(record) == 2
```

## Custom Assertion Helpers

```python
def assert_valid_response(response, status=200):
    """Reusable assertion for API responses."""
    assert response.status_code == status, f"Expected {status}, got {response.status_code}"
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert "error" not in data, f"Unexpected error: {data.get('error')}"
    return data

def test_api():
    response = client.get("/users")
    data = assert_valid_response(response)
    assert len(data) > 0
```

## Soft Assertions (pytest-check)

Continue after failures to see all issues:

```python
# pip install pytest-check
import pytest_check as check

def test_multiple():
    result = get_result()
    check.equal(result.status, 200)     # Continues if fails
    check.is_true(result.success)       # Continues if fails
    check.greater(len(result.items), 0) # Continues if fails
    # Report shows ALL failures
```

## Common Patterns

```python
# Membership
assert item in collection
assert key in dictionary

# String patterns
assert "error" in message.lower()
assert text.startswith("Hello")

# Collection checks
assert len(items) == 5
assert all(x > 0 for x in items)
assert any(x.is_valid for x in items)
assert sorted(items) == expected_order

# Type checking
assert isinstance(result, dict)
assert isinstance(obj, (str, int))
```

## Adding Context to Failures

```python
assert result == expected, f"Failed for user {user.id}: got {result}"
```
