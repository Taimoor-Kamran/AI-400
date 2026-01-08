from fastapi import FastAPI

app = FastAPI()
@app.get("/tasks")
def todo() -> list[dict[str, int | str]]:
    return [{"id": 1, "task": "Buy groceries"},
            {"id": 2, "task": "Read a book"}]
    
@app.get("/tasks/{task_id}")
async def todo_one(task_id: int = 1, include_details: bool = False) -> dict[str, int | str]:
    if task_id < 1:
        return {"error" : "Task ID must be gerater than 0"}
    if include_details:
        return {"id" : task_id, "task": "Buy groceries", "details": "Buy groceries for the week"}
    return {"id" : task_id, "task": "Buy groceries"}
 