# Pytest Parametrization

Run the same test with different inputs without duplicating code.

## Basic Parametrization

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    (1, 1),
    (2, 4),
    (3, 9),
    (4, 16),
])
def test_square(input, expected):
    assert input ** 2 == expected
```

Output:
```
test_math.py::test_square[1-1] PASSED
test_math.py::test_square[2-4] PASSED
test_math.py::test_square[3-9] PASSED
test_math.py::test_square[4-16] PASSED
```

## Custom Test IDs

Make test output more readable:

```python
@pytest.mark.parametrize("a,b,expected", [
    pytest.param(2, 3, 5, id="positive_numbers"),
    pytest.param(-1, 1, 0, id="negative_and_positive"),
    pytest.param(0, 0, 0, id="zeros"),
    pytest.param(1.5, 2.5, 4.0, id="floats"),
])
def test_addition(a, b, expected):
    assert a + b == expected
```

Output:
```
test_math.py::test_addition[positive_numbers] PASSED
test_math.py::test_addition[negative_and_positive] PASSED
test_math.py::test_addition[zeros] PASSED
test_math.py::test_addition[floats] PASSED
```

## Multiple Parameter Sets

Combine multiple parametrize decorators:

```python
@pytest.mark.parametrize("x", [1, 2])
@pytest.mark.parametrize("y", [10, 20])
def test_multiply(x, y):
    result = x * y
    assert result == x * y

# Runs: (1,10), (1,20), (2,10), (2,20)
```

## Parametrize with Marks

Apply marks to specific test cases:

```python
@pytest.mark.parametrize("test_input,expected", [
    ("3+5", 8),
    ("2+4", 6),
    pytest.param("6*9", 42, marks=pytest.mark.xfail(reason="known bug")),
    pytest.param("slow_op()", 100, marks=pytest.mark.slow),
])
def test_eval(test_input, expected):
    assert eval(test_input) == expected
```

## Parametrize Classes

Apply to all methods in a class:

```python
@pytest.mark.parametrize("n", [1, 2, 3])
class TestMultiplication:
    def test_double(self, n):
        assert n * 2 == n + n

    def test_triple(self, n):
        assert n * 3 == n + n + n
```

## Indirect Parametrization

Pass values through fixtures:

```python
@pytest.fixture
def database(request):
    """Setup database based on parameter"""
    db_type = request.param
    db = connect_to(db_type)
    yield db
    db.close()

@pytest.mark.parametrize("database", ["mysql", "postgres"], indirect=True)
def test_connection(database):
    assert database.is_connected()
```

## Parametrize Fixtures

Alternative to indirect:

```python
@pytest.fixture(params=["chrome", "firefox", "safari"])
def browser(request):
    driver = create_driver(request.param)
    yield driver
    driver.quit()

def test_page_title(browser):
    browser.get("https://example.com")
    assert "Example" in browser.title
```

## Complex Objects as Parameters

```python
from dataclasses import dataclass

@dataclass
class TestCase:
    input: str
    expected: int
    description: str

test_cases = [
    TestCase("hello", 5, "simple_word"),
    TestCase("", 0, "empty_string"),
    TestCase("hello world", 11, "with_space"),
]

@pytest.mark.parametrize("case", test_cases, ids=lambda c: c.description)
def test_length(case):
    assert len(case.input) == case.expected
```

## Parametrize with Fixtures Combined

```python
@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.parametrize("endpoint,status", [
    ("/users", 200),
    ("/admin", 403),
    ("/missing", 404),
])
def test_endpoints(api_client, endpoint, status):
    response = api_client.get(endpoint)
    assert response.status_code == status
```

## Dynamic Parametrization

Generate parameters at collection time:

```python
def generate_test_data():
    """Generate test cases dynamically"""
    return [
        (i, i**2) for i in range(1, 6)
    ]

@pytest.mark.parametrize("n,square", generate_test_data())
def test_squares(n, square):
    assert n ** 2 == square
```

## pytest_generate_tests Hook

For advanced dynamic parametrization:

```python
# conftest.py
def pytest_generate_tests(metafunc):
    if "db_type" in metafunc.fixturenames:
        metafunc.parametrize("db_type", ["mysql", "postgres", "sqlite"])
```

```python
# test_database.py
def test_connection(db_type):
    # Automatically runs for each db_type
    db = connect(db_type)
    assert db.ping()
```

## Best Practices

1. **Use descriptive IDs** - `pytest.param(..., id="descriptive_name")`
2. **Keep parameter lists manageable** - Extract to variables if too long
3. **Group related test cases** - Use classes or separate parametrize calls
4. **Use indirect for expensive setup** - Avoid recreating in each test
5. **Consider data classes** - For complex test case objects
6. **Mark edge cases** - Use `xfail` for known issues, `skip` for conditional
7. **Test boundaries** - Include edge cases (0, negative, max values)
