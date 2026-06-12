
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_name: str
    database_password: str
    database_username: str

    SECRET_KEY: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = Path(__file__).parent / ".env"


settings = Settings()