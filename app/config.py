from pydantic.v1 import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    # Database variables
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    class Config:
        # Get the absolute path to the directory where config.py is located
        base_dir = Path(__file__).resolve().parent.parent
        # Set the absolute path to the .env file
        env_file = base_dir / ".env"
        env_file_encoding = "utf-8"


settings = Settings()
