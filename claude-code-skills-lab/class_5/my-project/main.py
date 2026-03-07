
import os
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Field, create_engine, Session, select
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv("DB_URL"), echo=True)

# Migration Command
# SQLModel.metadata.create_all(engine)


# How to actually interact with tables?

def get_session():
    with Session(engine) as session:
        yield session

app = FastAPI()

