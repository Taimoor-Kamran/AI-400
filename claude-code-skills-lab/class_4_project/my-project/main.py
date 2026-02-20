from fastapi import FastAPI

app = FastAPI(
    title="Task API",
    description="A simple task management API"
)

@app.get("/")
def read_root():
    return {"message": "Task Api Is Running"}