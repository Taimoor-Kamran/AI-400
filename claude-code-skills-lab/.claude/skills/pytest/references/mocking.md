# Mocking

## Patch Decorator

```python
from unittest.mock import patch, Mock

@patch("mymodule.external_api")
def test_with_mock(mock_api):
    mock_api.return_value = {"data": "mocked"}
    result = function_that_calls_api()
    assert result["data"] == "mocked"
    mock_api.assert_called_once()
```

**Critical:** Patch where it's used, not where it's defined:
```python
# mymodule.py imports requests
# WRONG: @patch("requests.get")
# RIGHT: @patch("mymodule.requests.get")
```

## Multiple Patches

```python
@patch("mymodule.func_a")
@patch("mymodule.func_b")
def test_multiple(mock_b, mock_a):  # Reverse order!
    mock_a.return_value = 1
    mock_b.return_value = 2
```

## Context Manager

```python
def test_with_context():
    with patch("mymodule.get_data") as mock_get:
        mock_get.return_value = [1, 2, 3]
        result = process_data()
        assert len(result) == 3
```

## pytest-mock (Recommended)

```python
# pip install pytest-mock

def test_with_mocker(mocker):
    mock_api = mocker.patch("mymodule.api_call")
    mock_api.return_value = {"status": "ok"}

    result = my_function()

    mock_api.assert_called_once_with(expected_arg)
```

## monkeypatch Fixture

Built-in pytest fixture for simpler cases:

```python
def test_env(monkeypatch):
    monkeypatch.setenv("API_KEY", "test-key")
    monkeypatch.delenv("DEBUG", raising=False)

def test_attribute(monkeypatch):
    monkeypatch.setattr("os.getcwd", lambda: "/fake/path")

def test_dict(monkeypatch):
    monkeypatch.setitem(config, "key", "new_value")
```

## Return Values

```python
mock = Mock()
mock.return_value = 42                    # Single value
mock.side_effect = [1, 2, 3]              # Sequence
mock.side_effect = ValueError("error")    # Raise exception

# Conditional
def side_effect(arg):
    return "positive" if arg > 0 else "negative"
mock.side_effect = side_effect
```

## Asserting Calls

```python
from unittest.mock import call

mock(1, key="a")
mock(2, key="b")

mock.assert_called()
mock.assert_called_with(2, key="b")       # Last call
mock.assert_any_call(1, key="a")          # Any call
assert mock.call_count == 2

assert mock.call_args_list == [
    call(1, key="a"),
    call(2, key="b"),
]
```

## Async Mocking

```python
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_async(mocker):
    mock_fetch = mocker.patch("mymodule.fetch", new_callable=AsyncMock)
    mock_fetch.return_value = {"data": "async"}

    result = await my_async_function()
    assert result["data"] == "async"
```

## Spec for Safety

Ensure mock matches real object's interface:

```python
from unittest.mock import create_autospec

mock = create_autospec(RealClass)
mock.real_method()      # Works
mock.nonexistent()      # AttributeError
mock.real_method("wrong", "args")  # TypeError
```
