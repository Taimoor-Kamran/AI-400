def get_temp_file():
    """Provide a temporary file that gets cleaned up."""
    import tempfile
    import os

    # Setup: create the file
    fd, path = tempfile.mkstemp()
    file = os.fdopen(fd, 'w')

    try:
        yield file  # Provide to endpoint
    finally:
        # Cleanup: runs after endpoint completes
        file.close()
        os.unlink(path)


@app.post("/upload")
def process_upload(temp: file = Depends(get_temp_file)):
    temp.write("data")
    return {"status": "processed"}
