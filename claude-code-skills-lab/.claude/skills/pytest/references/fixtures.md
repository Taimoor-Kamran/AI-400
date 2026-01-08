# Fixtures

## Scopes

```python
@pytest.fixture(scope="function")  # Default: new instance per test
@pytest.fixture(scope="class")     # Once per test class
@pytest.fixture(scope="module")    # Once per test file
@pytest.fixture(scope="session")   # Once per test run
```

**Rule:** Fixtures can use other fixtures of equal or broader scope only.

## Setup/Teardown with Yield

```python
@pytest.fixture
def db_session():
    session = create_session()
    session.begin()
    yield session          # Test runs here
    session.rollback()     # Cleanup (runs even if test fails)
    session.close()
```

## Factory Pattern

For flexible test data creation:

```python
@pytest.fixture
def make_user():
    created = []

    def _make_user(name="Test", **kwargs):
        user = User(name=name, **kwargs)
        created.append(user)
        return user

    yield _make_user

    for user in created:
        user.delete()

def test_users(make_user):
    admin = make_user("Admin", role="admin")
    guest = make_user("Guest", role="guest")
```

## conftest.py

Place shared fixtures in `conftest.py` - auto-discovered, no imports needed:

```
tests/
├── conftest.py           # Available to all tests
├── test_users.py
└── integration/
    ├── conftest.py       # Additional fixtures for this folder
    └── test_api.py
```

## Parametrized Fixtures

```python
@pytest.fixture(params=["mysql", "postgres", "sqlite"])
def database(request):
    db = connect(request.param)
    yield db
    db.close()

def test_query(database):
    # Runs 3 times, once per database
    assert database.execute("SELECT 1")
```

With custom IDs:

```python
@pytest.fixture(params=[
    pytest.param({"host": "localhost"}, id="local"),
    pytest.param({"host": "remote"}, id="remote"),
])
def config(request):
    return request.param
```

## Built-in Fixtures

| Fixture | Purpose |
|---------|---------|
| `tmp_path` | `pathlib.Path` to temp directory |
| `tmp_path_factory` | Create multiple temp directories |
| `capsys` | Capture stdout/stderr |
| `caplog` | Capture log messages |
| `monkeypatch` | Modify objects/env during test |
| `request` | Access fixture metadata |

## Autouse

Run for all tests without explicit request:

```python
@pytest.fixture(autouse=True)
def reset_db():
    yield
    db.rollback()
```

**Caution:** Makes dependencies implicit - use sparingly.
