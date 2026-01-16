from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Field, create_engine, Session, select
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(os.getenv("DB_URL"), echo=True)


# DB Structure/Tables + same used at API Level
class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str | None = Field(default=None)

def get_session():
    with Session(engine) as session:
        yield session

app = FastAPI()


@app.post("/tasks")
def create_task(task: Task, session: Session = Depends(get_session)):
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@app.get("/tasks")
def get_task(session: Session = Depends(get_session)):
    tasks = session.exec(select(Task)).all()
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    return task


# How to create Table?
# How to actually interact with tables?



# DB Configuration


# def create_table():
#     print("Trying to create table")
#     SQLModel.metadata.create_all(engine)
#     print("Tables Function Completed")

# create_table()
