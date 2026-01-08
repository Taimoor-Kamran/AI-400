# Mocking Patterns

## Table of Contents
- [Basic Mocking](#basic-mocking)
- [Patching](#patching)
- [Mock Assertions](#mock-assertions)
- [Side Effects](#side-effects)
- [Async Mocking](#async-mocking)
- [pytest-mock Plugin](#pytest-mock-plugin)

## Basic Mocking

```python
from unittest.mock import Mock, MagicMock

# Simple mock
mock = Mock()
mock.method()
mock.method.assert_called_once()

# Mock with return value
mock = Mock(return_value=42)
assert mock() == 42

# Mock with attributes
mock = Mock()
mock.name = "test"
mock.value = 100

# MagicMock supports magic methods
mock = MagicMock()
mock.__len__.return_value = 5
assert len(mock) == 5
```

## Patching

### Decorator Pattern

```python
from unittest.mock import patch

@patch("myapp.module.external_function")
def test_with_mock(mock_func):
    mock_func.return_value = "mocked"
    result = my_function()
    assert result == "mocked"
    mock_func.assert_called_once()
```

### Context Manager Pattern

```python
def test_with_context():
    with patch("myapp.module.external_function") as mock_func:
        mock_func.return_value = "mocked"
        result = my_function()
        assert result == "mocked"
```

### Patch Object Attributes

```python
@patch.object(MyClass, "method")
def test_method(mock_method):
    mock_method.return_value = "mocked"
    obj = MyClass()
    assert obj.method() == "mocked"
```

### Patch Dictionary

```python
@patch.dict(os.environ, {"API_KEY": "test-key"})
def test_with_env():
    assert os.environ["API_KEY"] == "test-key"
```

### Patch Multiple

```python
@patch("myapp.module.func_a")
@patch("myapp.module.func_b")
def test_multiple(mock_b, mock_a):  # Note: reverse order
    mock_a.return_value = "a"
    mock_b.return_value = "b"
```

## Mock Assertions

```python
mock = Mock()

# Call assertions
mock()
mock.assert_called()
mock.assert_called_once()

# Argument assertions
mock("arg1", key="value")
mock.assert_called_with("arg1", key="value")
mock.assert_called_once_with("arg1", key="value")

# Any call matching
from unittest.mock import ANY
mock(123, data={"key": "value"})
mock.assert_called_with(ANY, data=ANY)

# Call count
assert mock.call_count == 2

# Call history
mock.reset_mock()
mock("first")
mock("second")
assert mock.call_args_list == [call("first"), call("second")]

# Not called
mock.reset_mock()
mock.assert_not_called()
```

## Side Effects

```python
# Raise exception
mock = Mock(side_effect=ValueError("invalid"))
with pytest.raises(ValueError):
    mock()

# Return sequence of values
mock = Mock(side_effect=[1, 2, 3])
assert mock() == 1
assert mock() == 2
assert mock() == 3

# Custom function
def custom_side_effect(x):
    if x < 0:
        raise ValueError("negative")
    return x * 2

mock = Mock(side_effect=custom_side_effect)
assert mock(5) == 10
with pytest.raises(ValueError):
    mock(-1)
```

## Async Mocking

```python
from unittest.mock import AsyncMock

# AsyncMock for coroutines
@pytest.mark.asyncio
async def test_async_function():
    mock = AsyncMock(return_value={"data": "test"})
    result = await mock()
    assert result == {"data": "test"}

# Patching async functions
@patch("myapp.client.fetch", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_async_service(mock_fetch):
    mock_fetch.return_value = {"status": "ok"}
    result = await my_service.process()
    assert result["status"] == "ok"

# Async side effects
async def async_side_effect():
    return {"async": "response"}

mock = AsyncMock(side_effect=async_side_effect)
```

## pytest-mock Plugin

Install: `pip install pytest-mock`

```python
def test_with_mocker(mocker):
    # Cleaner syntax than unittest.mock
    mock = mocker.patch("myapp.module.function")
    mock.return_value = "mocked"

    result = my_function()

    assert result == "mocked"
    mock.assert_called_once()

def test_spy(mocker):
    # Spy on real function
    spy = mocker.spy(mymodule, "real_function")
    result = mymodule.real_function(1, 2)
    spy.assert_called_once_with(1, 2)
    # Real function was called, result is real

def test_stub(mocker):
    # Create stub
    stub = mocker.stub(name="my_stub")
    stub.return_value = "stubbed"
```

## Common Patterns

### Mock HTTP Responses

```python
@patch("requests.get")
def test_api_call(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": "test"}
    mock_get.return_value = mock_response

    result = fetch_api_data()

    assert result == {"data": "test"}
```

### Mock Datetime

```python
from datetime import datetime

@patch("myapp.module.datetime")
def test_time_sensitive(mock_datetime):
    mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0, 0)
    mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)

    result = get_current_hour()
    assert result == 12
```

### Mock File Operations

```python
from unittest.mock import mock_open

@patch("builtins.open", mock_open(read_data="file content"))
def test_read_file():
    result = read_config_file()
    assert result == "file content"
```
