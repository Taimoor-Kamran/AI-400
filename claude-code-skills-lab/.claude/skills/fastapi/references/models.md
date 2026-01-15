# Pydantic Models for FastAPI

## Basic Model

```python
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=100)

class UserCreate(UserBase):
    password: str = Field(min_length=8)

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Enable ORM mode
```

## Field Validation

```python
from pydantic import BaseModel, Field, field_validator
from typing import Annotated

class Product(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    price: float = Field(gt=0, description="Price must be positive")
    quantity: int = Field(ge=0, default=0)
    tags: list[str] = Field(default_factory=list, max_length=10)

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name cannot be blank")
        return v.strip()
```

## Nested Models

```python
class Address(BaseModel):
    street: str
    city: str
    country: str = "US"

class Company(BaseModel):
    name: str
    address: Address
    employees: list["Employee"] = []

class Employee(BaseModel):
    name: str
    role: str
```

## Optional and Union Types

```python
from typing import Literal

class Item(BaseModel):
    name: str
    description: str | None = None  # Optional
    status: Literal["draft", "published", "archived"] = "draft"
    metadata: dict[str, str] = Field(default_factory=dict)
```

## Model Inheritance Pattern

```python
# Base with shared fields
class ItemBase(BaseModel):
    title: str
    description: str | None = None

# Create: what client sends
class ItemCreate(ItemBase):
    pass

# Update: all fields optional
class ItemUpdate(BaseModel):
    title: str | None = None
    description: str | None = None

# Response: includes DB fields
class ItemResponse(ItemBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True
```

## Custom Serialization

```python
from pydantic import BaseModel, field_serializer
from datetime import datetime

class Event(BaseModel):
    name: str
    timestamp: datetime

    @field_serializer("timestamp")
    def serialize_dt(self, dt: datetime) -> str:
        return dt.isoformat()
```

## Generic Response Model

```python
from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int
    pages: int

# Usage
@app.get("/users", response_model=PaginatedResponse[UserResponse])
```

## Example Values for Docs

```python
class User(BaseModel):
    name: str
    email: EmailStr

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john@example.com"
            }
        }
```
