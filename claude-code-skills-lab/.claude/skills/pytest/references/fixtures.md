# Pytest Fixtures

Fixtures provide a way to set up test data, connections, or state that tests need.

## Basic Fixture

```python
import pytest

@pytest.fixture
def user_data():
    """Returns sample user data for tests"""
    return {
        "id": 1,
        "name": "Alice",
        "email": "alice@example.com"
    }

def test_user_has_name(user_data):
    assert user_data["name"] == "Alice"

def test_user_has_email(user_data):
    assert "@" in user_data["email"]
```

## Setup and Teardown with Yield

```python
import pytest

@pytest.fixture
def database_connection():
    # Setup: runs before test
    conn = create_connection()
    conn.begin_transaction()

    yield conn  # Provide the fixture value

    # Teardown: runs after test (even if test fails)
    conn.rollback()
    conn.close()

def test_insert_user(database_connection):
    database_connection.execute("INSERT INTO users ...")
    # Transaction is rolled back after test
```

## Fixture Scopes

Control how often fixtures are created:

```python
@pytest.fixture(scope="function")  # Default: new for each test
def per_test_fixture():
    return create_resource()

@pytest.fixture(scope="class")  # Once per test class
def per_class_fixture():
    return create_resource()

@pytest.fixture(scope="module")  # Once per test file
def per_module_fixture():
    return create_resource()

@pytest.fixture(scope="session")  # Once per test run
def per_session_fixture():
    return create_resource()
```

### Scope Hierarchy

```
session (broadest)
    └── module
        └── class
            └── function (narrowest)
```

Fixtures can use other fixtures of equal or broader scope.

## Autouse Fixtures

Run automatically for all tests in scope:

```python
@pytest.fixture(autouse=True)
def reset_environment():
    """Runs before every test automatically"""
    os.environ["MODE"] = "test"
    yield
    os.environ.pop("MODE", None)
```

## Fixture Parametrization

Run tests with multiple fixture values:

```python
@pytest.fixture(params=["mysql", "postgresql", "sqlite"])
def database(request):
    """Test runs 3 times, once for each database"""
    db = connect_to(request.param)
    yield db
    db.close()

def test_query(database):
    # This test runs 3 times with different databases
    result = database.query("SELECT 1")
    assert result is not None
```

### With Custom IDs

```python
@pytest.fixture(params=[
    pytest.param({"host": "localhost"}, id="local"),
    pytest.param({"host": "remote.server"}, id="remote"),
])
def config(request):
    return request.param
```

## conftest.py - Sharing Fixtures

Put fixtures in `conftest.py` to share across multiple test files:

```
tests/
├── conftest.py          # Fixtures available to all tests
├── test_users.py
├── test_orders.py
└── integration/
    ├── conftest.py      # Additional fixtures for integration tests
    └── test_api.py
```

```python
# tests/conftest.py
import pytest

@pytest.fixture
def app():
    """Available to all tests in tests/"""
    return create_app(testing=True)

@pytest.fixture
def client(app):
    """Depends on app fixture"""
    return app.test_client()
```

## Built-in Fixtures

Pytest provides useful fixtures out of the box:

```python
def test_temp_files(tmp_path):
    """tmp_path: pathlib.Path to temp directory"""
    file = tmp_path / "test.txt"
    file.write_text("hello")
    assert file.read_text() == "hello"

def test_temp_directory(tmp_path_factory):
    """tmp_path_factory: create multiple temp dirs"""
    dir1 = tmp_path_factory.mktemp("data1")
    dir2 = tmp_path_factory.mktemp("data2")

def test_capture_output(capsys):
    """capsys: capture stdout/stderr"""
    print("hello")
    captured = capsys.readouterr()
    assert captured.out == "hello\n"

def test_capture_logs(caplog):
    """caplog: capture log messages"""
    import logging
    logging.warning("test warning")
    assert "test warning" in caplog.text

def test_monkeypatch(monkeypatch):
    """monkeypatch: modify objects during test"""
    monkeypatch.setenv("API_KEY", "test-key")
    monkeypatch.setattr(module, "function", mock_function)
```

## Factory Fixtures

Return a factory function for flexible test data:

```python
@pytest.fixture
def make_user():
    """Factory fixture for creating users"""
    created_users = []

    def _make_user(name="Test", email=None):
        email = email or f"{name.lower()}@test.com"
        user = User(name=name, email=email)
        created_users.append(user)
        return user

    yield _make_user

    # Cleanup all created users
    for user in created_users:
        user.delete()

def test_multiple_users(make_user):
    user1 = make_user("Alice")
    user2 = make_user("Bob", email="bob@custom.com")
    assert user1.email == "alice@test.com"
    assert user2.email == "bob@custom.com"
```

## Best Practices

1. **Keep fixtures focused** - One responsibility per fixture
2. **Use appropriate scope** - Don't over-scope (wastes isolation)
3. **Name fixtures clearly** - `authenticated_client` not `client2`
4. **Use yield for cleanup** - Ensures cleanup even on test failure
5. **Prefer factories for flexibility** - When tests need variations
6. **Put shared fixtures in conftest.py** - Don't repeat across files
7. **Avoid fixture dependencies on test internals** - Keep them reusable
