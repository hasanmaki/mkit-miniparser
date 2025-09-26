from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from loguru import logger

from dpends import SettingsDeps
from src.config import AppSettings, get_settings
from src.config.cfg_logging import setup_logging

glob_config: AppSettings = get_settings("config.toml")


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: RUF029
    """Lifespan context manager for FastAPI app."""
    setup_logging()
    logger.bind(request_id="app-startup").info("Starting up...")
    # set app state
    app.state.settings = glob_config
    yield
    logger.bind(request_id="app-shutdown").info("Shutting down...")


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root(settings: SettingsDeps):
    """Just welcome message."""
    return {"message": "Hello World", "settings": settings}


if __name__ == "__main__":
    uvicorn.run(app="src.main:app", host="0.0.0.0", port=8000, reload=True)
