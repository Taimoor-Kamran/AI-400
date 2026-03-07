
import os
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Field, create_engine, Session, select
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv("DB_URL"), echo=True)

class User(SQLModel, table=true):
    id: int | None = Field(default=None, primary_key=True)
    name: str | None = Field(default=None)
    email: str
    password: str

# Migration Command
# SQLModel.metadata.create_all(engine)


# How to actually interact with tables?

def get_session():
    with Session(engine) as session:
        yield session

app = FastAPI()

# Create User
@app.post("/users")
def create_user(user: User, session: Session = Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user