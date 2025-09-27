from fastapi import Request


async def get_appstate_settings(request: Request):  # noqa: RUF029
    """Dependency to get app state settings."""
    return request.app.state.settings


async def get_appstate_http_client(request: Request):  # noqa: RUF029
    """Dependency to get app state http client."""
    return request.app.state.request_client
