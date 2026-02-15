from fastapi import FastAPI, Depends
from dotenv import load_dotenv
import os
app = FastAPI()

load_dotenv()


def get_config():
    print("\n CONFIG FUNC: 1")
    return {"app": "taskapi", "gemini-key": os.getenv("GEMINI_API_KEY")}

@app.get("/hello")
def hello(config: dict = Depends(get_config)):
    print("\n NORMAL API FUNC: 1")
    # config = get_config()
    return {"message" : "all good", "gemini-key": config["geminikey"]}
