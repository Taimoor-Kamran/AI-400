# FastAPI Dependency Injection

## Basic Dependency

```python
from typing import Annotated
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users")
def list_users(db: Annotated[Session, Depends(get_db)]):
    return db.query(User).all()
```

## Reusable Type Alias

```python
from typing import Annotated
from fastapi import Depends

# Define once
DbSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]

# Use everywhere
@app.get("/items")
def list_items(db: DbSession, user: CurrentUser):
    return db.query(Item).filter(Item.owner_id == user.id).all()
```

## Class-Based Dependencies

```python
class Pagination:
    def __init__(self, skip: int = 0, limit: int = Query(default=10, le=100)):
        self.skip = skip
        self.limit = limit

@app.get("/items")
def list_items(pagination: Annotated[Pagination, Depends()]):
    return items[pagination.skip : pagination.skip + pagination.limit]
```

## Dependency with Parameters

```python
def get_user_by_role(required_role: str):
    def dependency(user: CurrentUser):
        if user.role != required_role:
            raise HTTPException(403, "Insufficient permissions")
        return user
    return dependency

AdminUser = Annotated[User, Depends(get_user_by_role("admin"))]

@app.delete("/users/{id}")
def delete_user(id: int, admin: AdminUser):
    pass
```

## Chained Dependencies

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_service(db: Annotated[Session, Depends(get_db)]):
    return UserService(db)

@app.get("/users/{id}")
def get_user(
    id: int,
    service: Annotated[UserService, Depends(get_user_service)]
):
    return service.get(id)
```

## Router-Level Dependencies

```python
router = APIRouter(
    prefix="/admin",
    dependencies=[Depends(require_admin)]  # Applied to all routes
)

@router.get("/stats")
def admin_stats():  # require_admin runs automatically
    return {"users": 100}
```

## Global Dependencies

```python
app = FastAPI(dependencies=[Depends(verify_api_key)])
```

## Dependencies with Yield (Context Manager)

```python
async def get_redis():
    redis = await aioredis.from_url("redis://localhost")
    try:
        yield redis
    finally:
        await redis.close()
```

## Common Patterns

```python
# Query params validation
def common_params(
    q: str | None = None,
    skip: int = 0,
    limit: int = 100
):
    return {"q": q, "skip": skip, "limit": limit}

CommonParams = Annotated[dict, Depends(common_params)]

# Service injection
def get_email_service(settings: Annotated[Settings, Depends(get_settings)]):
    return EmailService(settings.smtp_host, settings.smtp_port)
```
