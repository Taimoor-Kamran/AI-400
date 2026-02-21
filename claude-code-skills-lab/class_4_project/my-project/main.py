from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel

app = FastAPI(
    title="Task API",
    description="A simple task management API"
)

# Model

class Task(BaseModel):
    id: int
    title: str
    description: str
    completed: bool = False

# Fake Database (In Memory)
    
tasks: List[Task] = []


# Create Task

@app.post("/tasks")
def create_tasks(task: Task):
    tasks.append(task)
    return {"message": "Task Created Successfully","task": task}
    
# Read All Task    
    
@app.get("/tasks")
def get_tasks():
    return tasks

# Read Single Task 

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
        raise HTTPException(status_code=404, details="Task not found")