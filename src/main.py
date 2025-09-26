from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from loguru import logger

from src.config.cfg_logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001, RUF029
    """Lifespan context manager for FastAPI app."""
    setup_logging()
    logger.info("Starting up...")
    yield
    logger.info("Shutting down...")


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    """Just welcome message."""
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app="src.main:app", host="0.0.0.0", port=8000, reload=True)
