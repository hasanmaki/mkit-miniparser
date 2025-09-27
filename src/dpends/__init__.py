"""module for managing dependencies."""

from typing import Annotated

from config import AppSettings
from dpends.deps import get_appstate_settings
from fastapi import Depends


SettingsDeps = Annotated[AppSettings, Depends(get_appstate_settings)]
