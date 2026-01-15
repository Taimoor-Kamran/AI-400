from fastapi import FastAPI, HTTPException
from from pydantic import BaseModel

app = FastAPI()

class TaskCreate(BaseModel):
    title: str
    description: str = None | None

class TaskUpdate(BaseModel):
    title: str
    description: str = None | None
    status: str = None | None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str = None
    status: str

# Storage

tasks: list[dict] = []
task_counter - 0

# Create

@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate):
    global task_counter
    task_counter += 1
    new_task = {
        "id": task_counter,
        "title": task.title,
        "description": task.description,
        "status": "pending"
    }
    tasks.append(new_task)
    return new_task

@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks():
    return tasks
