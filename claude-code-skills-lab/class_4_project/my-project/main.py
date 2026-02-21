from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="Task API",
    description="A simple task management API"
)

class Task(BaseModel):
    id: int
    title: str
    description: str
    completed: bool = False
    
tasks: List[Task] = []

@app.post("/tasks")
def create_task(task: Task):
    tasks.append(task)
    return {"message": "Task Created Successfully", "task": task}