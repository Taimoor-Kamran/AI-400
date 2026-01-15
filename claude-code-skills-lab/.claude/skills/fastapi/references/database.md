# FastAPI Database Integration

## SQLAlchemy Setup (Sync)

```python
# db/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "postgresql://user:pass@localhost/dbname"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass
```

## SQLAlchemy Models

```python
# db/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    items = relationship("Item", back_populates="owner")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
```

## Database Dependency

```python
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

DbSession = Annotated[Session, Depends(get_db)]

@app.get("/users/{id}")
def get_user(id: int, db: DbSession):
    return db.query(User).filter(User.id == id).first()
```

## Async SQLAlchemy

```python
# db/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/dbname"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with async_session() as session:
        yield session

# Usage
from sqlalchemy import select

@app.get("/users/{id}")
async def get_user(id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(User).where(User.id == id))
    return result.scalar_one_or_none()
```

## CRUD Operations

```python
# crud/user.py
from sqlalchemy.orm import Session
from sqlalchemy import select

class UserCRUD:
    def __init__(self, db: Session):
        self.db = db

    def get(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def list(self, skip: int = 0, limit: int = 100) -> list[User]:
        return self.db.query(User).offset(skip).limit(limit).all()

    def create(self, user_in: UserCreate) -> User:
        user = User(**user_in.model_dump())
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: User, user_in: UserUpdate) -> User:
        for field, value in user_in.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()
```

## Alembic Migrations

```bash
# Initialize
alembic init alembic

# Edit alembic/env.py
from app.db.database import Base
from app.db.models import *  # Import all models
target_metadata = Base.metadata

# Create migration
alembic revision --autogenerate -m "Add users table"

# Apply
alembic upgrade head
```

## Transaction Patterns

```python
# Explicit transaction
async def transfer_funds(db: AsyncSession, from_id: int, to_id: int, amount: float):
    async with db.begin():
        from_account = await db.get(Account, from_id)
        to_account = await db.get(Account, to_id)
        from_account.balance -= amount
        to_account.balance += amount
        # Commits on exit, rolls back on exception
```

## MongoDB with Motor

```python
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.mydb

async def get_db():
    return db

@app.get("/items/{id}")
async def get_item(id: str, db = Depends(get_db)):
    item = await db.items.find_one({"_id": ObjectId(id)})
    return item
```
