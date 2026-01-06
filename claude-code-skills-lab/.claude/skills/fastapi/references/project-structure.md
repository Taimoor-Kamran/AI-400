# FastAPI Project Structure

## Standard Layout

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app instance, middleware
│   ├── config.py            # Settings with pydantic-settings
│   ├── dependencies.py      # Shared dependencies
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── items.py
│   ├── models/              # Pydantic schemas
│   │   ├── __init__.py
│   │   └── user.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py      # Engine, session
│   │   └── models.py        # SQLAlchemy models
│   └── services/            # Business logic
│       └── user_service.py
├── tests/
│   ├── conftest.py
│   └── test_users.py
├── alembic/                 # Migrations (if using)
├── requirements.txt
└── pyproject.toml
```

## Minimal Setup

```python
# main.py
from fastapi import FastAPI

app = FastAPI(title="My API", version="1.0.0")

@app.get("/health")
def health():
    return {"status": "ok"}
```

## Config Pattern

```python
# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    debug: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
```

## Router Organization

```python
# main.py
from fastapi import FastAPI
from app.routers import users, items

app = FastAPI()
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(items.router, prefix="/items", tags=["items"])
```

```python
# routers/users.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_users():
    return []
```

## Startup/Shutdown Events

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()

app = FastAPI(lifespan=lifespan)
```
