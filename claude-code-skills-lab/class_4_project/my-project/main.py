from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Task API",
    description="A Simple task management API"
)

class Task(BaseModel):
    id: int
    title: str
    description: str
    completed: bool = False
    
@app.post("/")
def create_todo():
    