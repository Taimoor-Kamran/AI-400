from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Task API",
    description="A Simple task management API"
)