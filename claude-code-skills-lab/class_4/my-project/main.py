from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Field

app = FastAPI()

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str | None = Field(default=None)


@app.get("/tasks")
def create_task(task: Task):

    return {"message": "all good",}
