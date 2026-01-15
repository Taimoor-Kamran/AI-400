from fastapi import FastAPI, Depends
from dotenv import load_dotenv
import os
app = FastAPI()

load_dotenv()


def get_config():
    print("\n CONFIG FUNC: 1")
    return {"app": "taskapi", "storage": "in-memory", "gemini_key": os.getenv("GEMINI_API_KEY")}

@app.get("/hello")
def hello(config: dict = Depends(get_config)):
    print("\n NORMAL API: 2")
    # config = get_config()
    return {"message": "all good", "geminikey": config["gemini_key"]}

# import tempfile
# import os

# def get_temp_file():
#     """Provide a temporary file that gets cleaned up."""


#     # Setup: create the file
#     fd, path = tempfile.mkstemp()
#     file = os.fdopen(fd, 'w')

#     try:
#         yield file  # Provide to endpoint
#     finally:
#         # Cleanup: runs after endpoint completes
#         file.close()
#         os.unlink(path)


# @app.post("/upload")
# def process_upload(temp: TextIO = Depends(get_temp_file)):
#     temp.write("data")
#     return {"status": "processed"}
