"""api digipos."""

from fastapi import APIRouter, Depends

from dpends.deps import get_appstate_http_client, get_appstate_settings

router = APIRouter()


@router.get("/status")
async def get_status(
    http_client=Depends(get_appstate_http_client),
    settings=Depends(get_appstate_settings),
):
    """Get status from digipos API."""
    endpoint = f"{settings.url.base_url.rstrip('/')}/status"
    return await http_client.get(endpoint)
