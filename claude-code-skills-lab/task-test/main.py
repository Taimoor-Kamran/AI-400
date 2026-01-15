from fastapi import FastAPI

app = FastAPI(title="FastAPI Hello World")

@app.get("/")
def read_todo():
    """Root endpoint returning a Hello World message."""
    return {"message": "Hello World"}

@app.get("/health")
def health_check():
    """health check endpoint."""
    return {"status" : "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
    