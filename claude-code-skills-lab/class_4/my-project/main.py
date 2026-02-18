from fastapi import FastAPI
from sqlmodel import SQLModel, Field

app = FastAPI()

class Task(SQLModel):
    

@app.get("/hello")
def hello():
    return {"message": "all good"}