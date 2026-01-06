from fastapi import FastAPI

app = FastAPI()

@app.get("/todo")
def todo() -> list[dict[str, int | int]]:
    return [{"id": 1, "task" : "Buy groceries"},
            {"id": 2, "task" : "Read a book"}]

