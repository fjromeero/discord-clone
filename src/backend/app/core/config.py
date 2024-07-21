from typing import Literal

from dotenv import find_dotenv, load_dotenv
from pydantic import (
    PostgresDsn,
    computed_field,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


env_file = find_dotenv(".env")


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=env_file, env_ignore_empty=True, extra="ignore"
    )


    PROJECT_NAME: str
    API_V1_STR: str = "/api/v1"
    DOMAIN: str = "localhost"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"


    @computed_field  # type: ignore[misc]
    @property
    def server_host(self) -> str:
        # Use HTTPS for anything other than local development
        if self.ENVIRONMENT == "local":
            return f"http://{self.DOMAIN}:8000"
        return f"https://{self.DOMAIN}"


    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @computed_field  # type: ignore[misc]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )
    
    SMTP_TOKEN: str
    SMTP_SENDER: str
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48


settings = Settings()