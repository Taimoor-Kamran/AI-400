from fastapi import FastAPI
from sqlmodel import SQLModel, Field

app = FastAPI()

# DB Structure/Tables + Same used at API level
class Task(SQLModel, table=True):
     id: int | None = Field(default=None, primary_key=True)
     title: str
     description: str | None = Field(default=None)
    
# DB Configuration    
    
@app.post("/tasks")
def create_task(task: Task):
    return {"message": "all good"}