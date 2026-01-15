from fastapi import FastAPI, Depends
from dotenv import load_dotenv
import os
app = FastAPI()

load_dotenv()


@app.get("/hello")
def hello():
    print("\n NORMAL API: 2")
    return {"message": "all good", "geminikey": os.getenv("GEMINI_API_KEY")}
