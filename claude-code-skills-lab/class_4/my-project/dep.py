from fastapi import FastAPI, Depends
# import tempfile
# import os

app = FastAPI()

def get_config():
    return {"app": "taskapi", "storage": "in-memory"}


@app.get("/hello")
def hello(config: dict = Depends(get_config)):
    # config = get_config()
    return {"message" : "all good", "app-name": config["app"]}


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
# def process_upload(temp: file = Depends(get_temp_file)):
#     temp.write("data")
#     return {"status": "processed"}