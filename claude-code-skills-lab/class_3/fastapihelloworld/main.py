from fastapi import FastAPI
from pydantic import BaseModel
from typing_extensions import Dict

app = FastAPI(title="FastAPI Hello World")


class todoItem(BaseModel):
    id: int
    task: str
    time_estimate: int = None


class TodoItemResponse(BaseModel):
    id: int
    task: str
    time_estimate: int = None
    completed: bool = False



@app.get("/")
def read_todo():
    """Root endpoint returning a Hello World message."""
    return {"message": "Hello World"}


@app.get("/todo")
def todo() -> list[TodoItemResponse]:
    my_todo_list = [
        TodoItemResponse(id=1, task="Learn FastAPI", completed=False),
        TodoItemResponse(id=2, task="Build an API", completed=False),
    ]
    return my_todo_list


@app.post("/todo")
def add_todo(todo: todoItem) -> TodoItemResponse:
    todo_response = TodoItemResponse(**todo.dict(), completed=True)
    return todo_response


@app.delete("/todo/{item_id}")
def delete_tood(item_id: int):
    """Delete a todo item by its ID."""
    return {"message": f"Todo item with id {item_id} deleted."}


@app.put("/todo/{item_id}")
def update_todo(item_id: int, todo: todoItem) -> TodoItemResponse:
    todo_response = TodoItemResponse(**todo.dict(), completed=True)
    return todo_response


@app.patch("/todo/{item_id}/complete")
def complete_todo(item_id: int) -> TodoItemResponse:
    """Mark a todo item as completed."""
    todo_response = TodoItemResponse(
        id=item_id, task="Sample Task",completed=True
    )
    return todo_response


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
