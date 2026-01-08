from fastapi import FastAPI

app = FastAPI(title="FastAPI Hello World")


@app.get("/")
def read_todo():
    """Root endpoint returning a Hello World message."""
    return {"message": "Hello World"}


@app.get("/todo")
def todo():
    my_todo_list = [
        {"id": 1, "task": "Learn FastAPI"},
        {"id": 2, "task": "Build an API"},
    ]
    return my_todo_list


@app.post("/todo")
def add_todo(todo: dict):
    return todo


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
