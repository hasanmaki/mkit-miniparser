from contextlib import asynccontextmanager

import httpx
import uvicorn
from fastapi import FastAPI
from loguru import logger

from config.settings import get_settings
from dpends import SettingsDeps
from src.api import register_routers
from src.config.cfg_logging import setup_logging

glob_config: SettingsDeps = get_settings("test_config.toml")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI app."""
    setup_logging()
    logger.info("Starting up...")
    app.state.settings = glob_config
    # test print
    logger.debug(f"Settings: {app.state.settings.model_dump_json(indent=2)}")
    app.state.request_client = httpx.AsyncClient()
    yield
    app.state.settings = None
    await app.state.request_client.aclose()
    logger.info("Shutting down...")


app = FastAPI(lifespan=lifespan)

# register routers
register_routers(app)


@app.get("/")
async def root(settings: SettingsDeps):
    """Just welcome message."""
    return {"message": "Hello World", "settings": settings}


if __name__ == "__main__":
    uvicorn.run(app="src.main:app", host="0.0.0.0", port=8000, reload=True)
