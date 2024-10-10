from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    database_url: PostgresDsn
    secret_key: str

    debug: bool = False

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


config = Config()
