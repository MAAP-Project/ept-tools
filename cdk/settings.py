from pydantic import BaseSettings
from pathlib import Path

env_file = Path.joinpath(Path.cwd(), '.env')


class Settings(BaseSettings):
    STACKNAME: str = "ept-server"
    STAGE: str = "dev"
    ROOT: str
    FILE: str = ""

    class Config:
        env_file = env_file


settings = Settings()
