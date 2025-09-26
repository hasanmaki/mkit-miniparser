from fastapi import Request

# Adjust import as needed


async def get_appstate_settings(request: Request):  # noqa: RUF029
    """Dependency to get app state settings."""
    return request.app.state.settings
