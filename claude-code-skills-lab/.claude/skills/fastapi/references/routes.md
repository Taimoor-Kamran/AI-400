# FastAPI Routes

## HTTP Methods

```python
@app.get("/items")           # List/Read
@app.post("/items")          # Create
@app.put("/items/{id}")      # Full update
@app.patch("/items/{id}")    # Partial update
@app.delete("/items/{id}")   # Delete
```

## Path Parameters

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):  # Auto-validated as int
    return {"user_id": user_id}

# Constrained paths
@app.get("/files/{file_path:path}")  # Matches /files/a/b/c
def get_file(file_path: str):
    return {"path": file_path}
```

## Query Parameters

```python
from typing import Annotated
from fastapi import Query

@app.get("/items")
def list_items(
    skip: int = 0,
    limit: int = Query(default=10, le=100),
    q: str | None = None,
    tags: Annotated[list[str] | None, Query()] = None
):
    return {"skip": skip, "limit": limit, "q": q}
```

## Request Body

```python
from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    price: float
    description: str | None = None

@app.post("/items")
def create_item(item: ItemCreate):
    return item
```

## Response Models

```python
class ItemResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True  # For ORM mode

@app.get("/items/{id}", response_model=ItemResponse)
def get_item(id: int):
    return db.get(id)

# Exclude fields
@app.get("/items", response_model=list[ItemResponse], response_model_exclude={"description"})
```

## Status Codes

```python
from fastapi import status

@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate):
    return item

@app.delete("/items/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(id: int):
    return None
```

## File Uploads

```python
from fastapi import File, UploadFile

@app.post("/upload")
async def upload(file: UploadFile):
    contents = await file.read()
    return {"filename": file.filename, "size": len(contents)}

# Multiple files
@app.post("/uploads")
async def upload_multiple(files: list[UploadFile]):
    return [{"filename": f.filename} for f in files]
```

## Form Data

```python
from fastapi import Form

@app.post("/login")
def login(username: str = Form(), password: str = Form()):
    return {"username": username}
```

## Background Tasks

```python
from fastapi import BackgroundTasks

def send_email(email: str, message: str):
    # Send email logic
    pass

@app.post("/send")
def send(background_tasks: BackgroundTasks, email: str):
    background_tasks.add_task(send_email, email, "Welcome!")
    return {"message": "Email queued"}
```
