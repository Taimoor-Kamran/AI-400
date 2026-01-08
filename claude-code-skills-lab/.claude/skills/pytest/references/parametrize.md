# Parametrization

## Basic Pattern

```python
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (-1, 1, 0),
    (0, 0, 0),
])
def test_add(a, b, expected):
    assert a + b == expected
```

## Custom Test IDs

```python
@pytest.mark.parametrize("input,expected", [
    pytest.param("hello", 5, id="simple_word"),
    pytest.param("", 0, id="empty_string"),
    pytest.param("a b", 3, id="with_space"),
])
def test_length(input, expected):
    assert len(input) == expected
```

## Multiple Parametrize (Cartesian Product)

```python
@pytest.mark.parametrize("x", [1, 2])
@pytest.mark.parametrize("y", [10, 20])
def test_multiply(x, y):
    # Runs 4 times: (1,10), (1,20), (2,10), (2,20)
    assert x * y == x * y
```

## Marks on Specific Cases

```python
@pytest.mark.parametrize("input,expected", [
    ("valid", True),
    pytest.param("edge", True, marks=pytest.mark.slow),
    pytest.param("bug", False, marks=pytest.mark.xfail(reason="known bug")),
    pytest.param("skip", None, marks=pytest.mark.skip),
])
def test_validate(input, expected):
    assert validate(input) == expected
```

## Indirect Parametrization

Pass values through fixtures:

```python
@pytest.fixture
def user(request):
    return create_user(role=request.param)

@pytest.mark.parametrize("user", ["admin", "guest"], indirect=True)
def test_permissions(user):
    # user fixture receives "admin" then "guest"
    assert user.can_login()
```

## Dynamic Generation

```python
def generate_cases():
    return [(i, i**2) for i in range(5)]

@pytest.mark.parametrize("n,square", generate_cases())
def test_squares(n, square):
    assert n ** 2 == square
```

## pytest_generate_tests Hook

For advanced dynamic parametrization:

```python
# conftest.py
def pytest_generate_tests(metafunc):
    if "db_type" in metafunc.fixturenames:
        metafunc.parametrize("db_type", ["mysql", "postgres"])
```

```python
# test_db.py
def test_connection(db_type):
    # Automatically parametrized
    db = connect(db_type)
    assert db.ping()
```

## Class-Level Parametrization

```python
@pytest.mark.parametrize("n", [1, 2, 3])
class TestMath:
    def test_positive(self, n):
        assert n > 0

    def test_square(self, n):
        assert n ** 2 >= n
```
