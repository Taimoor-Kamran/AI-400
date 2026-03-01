from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Session, select, Field, create_engine
import os
from dotenv import load_dotenv

load_dotenv()

# Create Engine
engine = create_engine(os.getenv("DB_URL"), echo=True)

app = FastAPI(
    title="Task API",
    description="A simple task management APP"
)

# Model

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str
    completed: bool = False

# Create Session

def get_session():
    with Session(engine) as session:
        yield session

# Create Table


def create_table():
    SQLModel.metadata.create_all(engine)

create_table()

# Add Task 




@app.post("/tasks")
def add_task(task : Task, session: Session = Depends(get_session)):
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
    
# Get Task

@app.get("/tasks")
def get_tasks(session: Session = Depends(get_session)):
        task = session.exec(select(Task)).all()
        return task
 
# Get Single Task     

@app.get("/tasks/{task_id}")
def get_task(task_id: int, session: Session = Depends(get_session)):
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
    
# Udpate Task
    
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task, session: Session = Depends(get_session)):
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        task.title = updated_task.title
        task.description = updated_task.description
        task.completed = updated_task.completed
        
        session.commit()
        session.refresh(task)
        return task

# Marked Task as True
    
@app.patch("/tasks/{task_id}")
def mark_task(task_id: int, session: Session = Depends(get_session)):
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        task.completed = True
        session.commit()
        session.refresh(task)
        return task

# Delete Task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, session: Session = Depends(get_session)):
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        session.delete(task)
        session.commit()
        return {"message": "Task delete successfully"}