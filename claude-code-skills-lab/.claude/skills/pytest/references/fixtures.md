# Fixture Patterns

## Table of Contents
- [Fixture Scopes](#fixture-scopes)
- [Fixture Factories](#fixture-factories)
- [Dependency Injection](#dependency-injection)
- [Database Fixtures](#database-fixtures)
- [Cleanup Patterns](#cleanup-patterns)

## Fixture Scopes

```python
import pytest

# Function scope (default) - new instance per test
@pytest.fixture
def user():
    return User(name="test")

# Class scope - shared within test class
@pytest.fixture(scope="class")
def shared_resource():
    return ExpensiveResource()

# Module scope - shared across test file
@pytest.fixture(scope="module")
def db_connection():
    conn = create_connection()
    yield conn
    conn.close()

# Package scope - shared across test package
@pytest.fixture(scope="package")
def package_config():
    return load_config()

# Session scope - shared across entire test run
@pytest.fixture(scope="session")
def app():
    return create_app(testing=True)
```

## Fixture Factories

Create fixtures dynamically with parameters:

```python
@pytest.fixture
def make_user():
    """Factory fixture for creating users with custom attributes."""
    created_users = []

    def _make_user(name="test", email=None, role="user"):
        email = email or f"{name}@example.com"
        user = User(name=name, email=email, role=role)
        created_users.append(user)
        return user

    yield _make_user

    # Cleanup
    for user in created_users:
        user.delete()

def test_admin_permissions(make_user):
    admin = make_user(name="admin", role="admin")
    regular = make_user(name="regular", role="user")
    assert admin.can_delete(regular)
```

## Dependency Injection

Fixtures can depend on other fixtures:

```python
@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()

@pytest.fixture
def session(db):
    Session = sessionmaker(bind=db)
    session = Session()
    yield session
    session.close()

@pytest.fixture
def user(session):
    user = User(name="test")
    session.add(user)
    session.commit()
    return user

def test_user_orders(session, user):
    # Both session and user fixtures are available
    order = Order(user_id=user.id)
    session.add(order)
    session.commit()
    assert len(user.orders) == 1
```

## Database Fixtures

### Transaction Rollback Pattern

```python
@pytest.fixture
def db_session(db_engine):
    """Each test runs in a transaction that rolls back."""
    connection = db_engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()
```

### Test Database Setup

```python
@pytest.fixture(scope="session")
def db_engine():
    """Create test database once per session."""
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()
```

## Cleanup Patterns

### Using yield

```python
@pytest.fixture
def temp_file():
    path = Path("/tmp/test_file.txt")
    path.write_text("test content")
    yield path
    path.unlink()  # Cleanup after test
```

### Using finalizers

```python
@pytest.fixture
def resource(request):
    res = acquire_resource()

    def cleanup():
        res.release()

    request.addfinalizer(cleanup)
    return res
```

### Autouse fixtures

```python
@pytest.fixture(autouse=True)
def reset_environment():
    """Automatically runs before each test."""
    original_env = os.environ.copy()
    yield
    os.environ.clear()
    os.environ.update(original_env)
```

## Parametrized Fixtures

```python
@pytest.fixture(params=["sqlite", "postgresql", "mysql"])
def database(request):
    """Test runs once for each database type."""
    db = create_database(request.param)
    yield db
    db.drop()

def test_query_performance(database):
    # This test runs 3 times, once per database
    result = database.query("SELECT 1")
    assert result is not None
```

## Fixture Caching

```python
@pytest.fixture(scope="session")
def expensive_data():
    """Computed once and cached for entire session."""
    return compute_expensive_data()

@pytest.fixture
def data_copy(expensive_data):
    """Each test gets a fresh copy."""
    return expensive_data.copy()
```
