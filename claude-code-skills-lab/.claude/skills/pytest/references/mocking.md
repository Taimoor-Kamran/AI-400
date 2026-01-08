# Pytest Mocking

Replace parts of your system with mock objects for isolated testing.

## Using unittest.mock

```python
from unittest.mock import Mock, patch, MagicMock

# Create a mock object
mock = Mock()
mock.method.return_value = 42
assert mock.method() == 42

# Track calls
mock.method("arg1", key="value")
mock.method.assert_called_once_with("arg1", key="value")
```

## The patch Decorator

```python
from unittest.mock import patch

# Patch a function
@patch("mymodule.external_api_call")
def test_with_mock(mock_api):
    mock_api.return_value = {"data": "mocked"}
    result = function_that_calls_api()
    assert result["data"] == "mocked"
    mock_api.assert_called_once()

# Patch multiple things
@patch("mymodule.function_a")
@patch("mymodule.function_b")
def test_multiple(mock_b, mock_a):  # Note: reverse order!
    mock_a.return_value = 1
    mock_b.return_value = 2
```

## Context Manager Patching

```python
from unittest.mock import patch

def test_with_context():
    with patch("mymodule.get_data") as mock_get:
        mock_get.return_value = [1, 2, 3]
        result = process_data()
        assert len(result) == 3
```

## patch.object

Patch attributes on objects:

```python
from unittest.mock import patch

class MyService:
    def fetch(self):
        return "real data"

def test_patch_method():
    service = MyService()
    with patch.object(service, "fetch", return_value="mocked"):
        assert service.fetch() == "mocked"
```

## pytest-mock Plugin

Cleaner fixture-based mocking:

```python
# pip install pytest-mock

def test_with_mocker(mocker):
    # mocker is a fixture from pytest-mock
    mock_api = mocker.patch("mymodule.api_call")
    mock_api.return_value = {"status": "ok"}

    result = my_function()

    assert result["status"] == "ok"
    mock_api.assert_called_once()
```

## Monkeypatch Fixture

Built-in pytest fixture for patching:

```python
def test_env_variable(monkeypatch):
    # Set environment variable
    monkeypatch.setenv("API_KEY", "test-key-123")
    assert os.environ["API_KEY"] == "test-key-123"

def test_delete_env(monkeypatch):
    monkeypatch.delenv("PATH", raising=False)

def test_patch_attribute(monkeypatch):
    # Patch module attribute
    monkeypatch.setattr("os.getcwd", lambda: "/fake/path")
    assert os.getcwd() == "/fake/path"

def test_patch_dict(monkeypatch):
    # Patch dictionary
    monkeypatch.setitem(my_dict, "key", "new_value")
```

## Mock Return Values

```python
from unittest.mock import Mock

mock = Mock()

# Single return value
mock.return_value = 42

# Different values on successive calls
mock.side_effect = [1, 2, 3]
assert mock() == 1
assert mock() == 2
assert mock() == 3

# Raise exception
mock.side_effect = ValueError("error")

# Conditional returns
def custom_side_effect(arg):
    if arg > 0:
        return "positive"
    return "non-positive"

mock.side_effect = custom_side_effect
```

## Asserting Calls

```python
from unittest.mock import Mock, call

mock = Mock()
mock(1, 2, key="value")
mock(3, 4)

# Assert called
mock.assert_called()
mock.assert_called_once()  # Fails - called twice

# Assert with arguments
mock.assert_called_with(3, 4)  # Last call
mock.assert_any_call(1, 2, key="value")  # Any call

# Check all calls
assert mock.call_args_list == [
    call(1, 2, key="value"),
    call(3, 4),
]

# Call count
assert mock.call_count == 2

# Not called
mock2 = Mock()
mock2.assert_not_called()
```

## MagicMock

Mock with magic methods pre-configured:

```python
from unittest.mock import MagicMock

mock = MagicMock()

# Works with len(), iteration, etc.
mock.__len__.return_value = 5
assert len(mock) == 5

mock.__iter__.return_value = iter([1, 2, 3])
assert list(mock) == [1, 2, 3]

# Context manager
mock.__enter__.return_value = "entered"
with mock as m:
    assert m == "entered"
```

## Async Mocking

```python
from unittest.mock import AsyncMock, patch
import pytest

@pytest.mark.asyncio
async def test_async_function():
    mock = AsyncMock(return_value={"data": "mocked"})
    result = await mock()
    assert result == {"data": "mocked"}

@pytest.mark.asyncio
@patch("mymodule.async_api_call", new_callable=AsyncMock)
async def test_patch_async(mock_api):
    mock_api.return_value = {"status": "ok"}
    result = await my_async_function()
    assert result["status"] == "ok"
```

## Spec and Autospec

Ensure mocks match real object signatures:

```python
from unittest.mock import Mock, create_autospec

class UserService:
    def get_user(self, user_id: int) -> dict:
        pass

# Basic spec - has same attributes
mock = Mock(spec=UserService)
mock.get_user(1)  # Works
mock.nonexistent()  # AttributeError

# Autospec - also checks method signatures
mock = create_autospec(UserService)
mock.get_user(1)  # Works
mock.get_user()  # TypeError - missing argument
```

## Common Patterns

### Mocking External APIs

```python
@patch("requests.get")
def test_api_integration(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"id": 1}

    result = fetch_user(1)

    assert result["id"] == 1
    mock_get.assert_called_with("https://api.example.com/users/1")
```

### Mocking Database

```python
def test_save_user(mocker):
    mock_db = mocker.patch("myapp.db.session")

    save_user({"name": "Alice"})

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
```

### Mocking Time

```python
from unittest.mock import patch
from datetime import datetime

@patch("mymodule.datetime")
def test_time_dependent(mock_datetime):
    mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0)
    result = get_greeting()
    assert result == "Good afternoon"
```

## Best Practices

1. **Patch where used, not defined** - `patch("mymodule.requests")` not `patch("requests")`
2. **Use autospec** - Catch interface mismatches early
3. **Don't over-mock** - Test real code when practical
4. **Reset mocks between tests** - Use fixtures for isolation
5. **Verify call arguments** - Don't just check return values
6. **Use pytest-mock** - Cleaner than raw unittest.mock
7. **Mock at boundaries** - APIs, databases, filesystem
