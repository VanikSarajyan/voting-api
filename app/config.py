from pydantic import BaseSettings


class Settings(BaseSettings):
    db_hostname: str
    db_port: int
    db_name: str
    db_username: str
    db_password: str

    class Config:
        env_file = ".env"
