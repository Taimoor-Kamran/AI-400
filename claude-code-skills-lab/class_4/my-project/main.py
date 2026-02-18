from fastapi import FastAPI
from sqlmodel import SQLModel

app = FastAPI()

@app.get("/hello")
def hello():
    return {"message": "all good"}