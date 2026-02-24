from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, Session, select, create_engine
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="Task API",
    description="A simple task management app"
    )

engine = create_engine(os.getenv("DB_URL"), echo=True)
print(engine)


# Model

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str
    completed: bool = False
    
# Create Task
    
@app.post("/tasks")
def create_task(task: Task):
    with Session(engine) as session:
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
    
# Get all task    
    
@app.get("/tasks")
def get_tasks(task: Task):
    with Session(engine) as session:
        session.exec(select(Task)).all()
        return task
    
# Get single task

@app.get("/tasks")
def get_task(task: Task, task_id: int):
    with Session(engine) as session:
        tasks = session.get(Task, task_id)
        if not tasks
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    
    
# Create Table

def create_table():
    SQLModel.metadata.create_all(engine)


create_table()