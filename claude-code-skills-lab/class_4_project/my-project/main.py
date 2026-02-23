from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, create_engine, Session, select
import os
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv("DB_URL"), echo=True)
print(engine)
print(os.getenv("DB_URL"))

app = FastAPI(
    title="Task API",
    description="A simple task management api"
)

# Model

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str
    completed: bool = False

# Create Table

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# Create Task

@app.post("/tasks")
def create_task(task: Task):
    with Session(engine) as session:
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

# Read All Task

@app.get("/tasks")
def get_tasks():
    with Session(engine) as session:
        tasks = session.exec(select(Task)).all()
        return tasks
        

# Read Single Task

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
    
    
# Update Task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        task.title = updated_task.title
        task.description = updated_task.description
        task.completed = updated_task.completed
        
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
        
    
# Patch (Mark Complete)

@app.patch("/tasks/{task_id}")
def complete_task(task_id: int):
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
    
        task.completed = True
        task.commit()
        task.refresh()
        return task 
    
# Delete Task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404)