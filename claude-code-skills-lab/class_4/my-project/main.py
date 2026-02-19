import os

from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Field, create_engine, Session
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv("DB_URL"), echo=True)



# DB Structure/Tables + Same used at API level
class Task(SQLModel, table=True):
     id: int | None = Field(default=None, primary_key=True)
     title: str
     description: str | None = Field(default=None)

# How to actually interact with tables?

def get_session():
    with Session(engine) as session:
        yield session

app = FastAPI()
    
# DB Configuration    
    
@app.post("/tasks")
def create_task(task: Task, session: Session = Depends(get_session)):
    return {"message": "all good"}

@app.get("/tasks")
def get_task(task: Task):
    return {"message": "all good"}

# How to create Table?
# def create_tables():
#     print("trying to create table")
#     SQLModel.metadata.create_all(engine)
#     print("Tables Function Completed")

# create_tables()