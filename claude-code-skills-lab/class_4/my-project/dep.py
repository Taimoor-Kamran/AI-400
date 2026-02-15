from fastapi import FastAPI, Depends
from dotenv import load_dotenv
import os
app = FastAPI()

load_dotenv()

GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")

def get_config():
    print("\n CONFIG FUNC: 1")
    return {"app": "taskapi", "storage": "in-memory"}

@app.get("/hello")
def hello(config: dict = Depends(get_config)):
    print("\n NORMAL API FUNC: 1")
    # config = get_config()
    return {"message" : "all good", "app-name": config["app"]}
