from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_name: str = Field(default="")
    database_username: str = Field(default="")
    database_password: str = Field(default="")
    database_host: str = Field(default="")
    database_port: int = Field(default=5432)

    database_debug: bool = Field(default=False)
    database_pool_size: int = Field(default=5)
    database_max_overflow: int = Field(default=10)
    database_pool_recycle: int = Field(default=3600)

    recognition_providers: list[str] = Field(default=["CPUExecutionProvider"])
    recognition_allowed_modules: list[str] = Field(default=["detection", "recognition"])
    recognition_det_size: int = Field(default=1280, ge=128, le=2048)
    recognition_det_thresh: float = Field(default=0.35, ge=0.0, le=1.0)
    recognition_min_similarity: float = Field(default=0.55, ge=0.0, le=2.0)
    recognition_default_limit: int = Field(default=5, ge=1, le=20)


base_config = BaseConfig()
