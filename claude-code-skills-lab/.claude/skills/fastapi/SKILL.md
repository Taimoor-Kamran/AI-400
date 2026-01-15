---
name: fastapi
description: FastAPI Python web framework development assistance. Use when building REST APIs with FastAPI, including project setup, route creation, Pydantic models, dependency injection, JWT/OAuth2 authentication, SQLAlchemy database integration, async endpoints, and testing. Triggers on FastAPI project creation, endpoint implementation, API authentication setup, database integration, or any FastAPI-related development task.
---

# FastAPI Development

Build modern, high-performance Python APIs with automatic OpenAPI documentation.

## Quick Reference

| Task | Reference |
|------|-----------|
| Project setup | [project-structure.md](references/project-structure.md) |
| Routes & endpoints | [routes.md](references/routes.md) |
| Pydantic models | [models.md](references/models.md) |
| Dependency injection | [dependencies.md](references/dependencies.md) |
| Authentication | [auth.md](references/auth.md) |
| Database integration | [database.md](references/database.md) |
| Testing | [testing.md](references/testing.md) |

## Core Patterns

### Minimal App

```python
from fastapi import FastAPI

app = FastAPI(title="My API", version="1.0.0")

@app.get("/")
def root():
    return {"message": "Hello"}
```

### Standard Endpoint Pattern

```python
from typing import Annotated
from fastapi import Depends, HTTPException, status
from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    price: float

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        from_attributes = True

@app.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate, db: Annotated[Session, Depends(get_db)]):
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Annotated[Session, Depends(get_db)]):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
```

### Protected Endpoint Pattern

```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
CurrentUser = Annotated[User, Depends(get_current_user)]

@app.get("/users/me")
def get_me(user: CurrentUser):
    return user
```

## Best Practices

1. **Use Annotated for dependencies** - Cleaner, reusable type hints
2. **Separate models** - `*Create`, `*Update`, `*Response` schemas
3. **Use routers** - Organize endpoints by domain in `routers/`
4. **Dependency injection** - Database sessions, services, auth via `Depends()`
5. **Async when needed** - Use `async def` only for I/O-bound operations with async libraries
6. **Response models** - Always specify `response_model` for documentation and validation
7. **Status codes** - Use `status.HTTP_*` constants for clarity
8. **Error handling** - Raise `HTTPException` with appropriate status codes

## Running

```bash
# Development
uvicorn app.main:app --reload

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

API docs available at `/docs` (Swagger) and `/redoc` (ReDoc).
