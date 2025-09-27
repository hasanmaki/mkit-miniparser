"""settings Loader and validator using pydantic_settings.

settings ini akan di store pada app state.settings untuk di akses pada seluruh bagian aplikasi.
"""

# ruff: noqa
from functools import lru_cache
from pydantic import BaseModel, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict, TomlConfigSettingsSource
from urllib.parse import urlparse


class ApiSettings(BaseModel):
    base_url: str
    username: str
    password: str
    pin: str
    retries: int = 3
    timeout: int = 10
    wait: int = 10

    @field_validator("base_url")
    @classmethod
    def validate_base_url(cls, v: str) -> str:
        parsed = urlparse(v)
        if not all([parsed.scheme, parsed.netloc]):
            raise ValueError("Invalid URL format")
        return v


class EndpointSettings(BaseModel):
    login: str
    logout: str
    balance: str
    profile: str


class ModuleConfig(BaseModel):
    api: ApiSettings
    endpoint: EndpointSettings | None = None


class AppSettings(BaseSettings):
    digipos: ModuleConfig

    model_config = SettingsConfigDict(
        extra="forbid",
        validate_assignment=True,
        from_attributes=True,
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ) -> tuple[TomlConfigSettingsSource, ...]:
        return (TomlConfigSettingsSource(settings_cls),)


@lru_cache
def get_settings(toml_file_path: str | None) -> AppSettings:
    """Get application settings with caching, without mutating global config."""
    if not toml_file_path:
        raise ValueError("TOML file path must be provided")
    # Dynamically set the TOML file path in model_config
    AppSettings.model_config["toml_file"] = toml_file_path
    return AppSettings()  # type: ignore
