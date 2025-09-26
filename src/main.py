import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    """Just welcome message."""
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app="src.main:app", host="0.0.0.0", port=8000, reload=True)
