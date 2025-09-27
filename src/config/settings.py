"""settings Loader and validator using pydantic_settings.

settings ini akan di store pada app state.settings untuk di akses pada seluruh bagian aplikasi.
"""

# ruff: noqa
from functools import lru_cache
from urllib.parse import urlparse
from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict, TomlConfigSettingsSource


class UrlSettings(BaseModel):
    base_url: str
    timeout: int = Field(gt=0, description="Timeout dalam detik")
    retries: int = Field(ge=0, description="Jumlah retry jika request gagal")

    @field_validator("base_url", mode="before")
    @classmethod
    def validate_base_url(cls, v: str) -> str:
        if not v.startswith("http"):
            raise ValueError("base_url harus diawali dengan http atau https")
        # Check port presence
        parsed = urlparse(v)
        if not parsed.port:
            raise ValueError(
                "base_url harus mengandung port (misal: http://localhost:8000)"
            )
        return v.rstrip("/")


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(toml_file=None, extra="forbid")

    url: UrlSettings

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
def get_settings(toml_path: str | None = None) -> AppSettings:
    class _CustomSettings(AppSettings):
        model_config = SettingsConfigDict(toml_file=toml_path, extra="forbid")

    return _CustomSettings()  # type: ignore
