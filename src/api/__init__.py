from api.digipos import router as digipos_router


def register_routers(app):
    """Register API routers."""
    app.include_router(digipos_router, prefix="/digipos", tags=["digipos"])
