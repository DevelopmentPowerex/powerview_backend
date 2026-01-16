import os

from dataclasses import dataclass

def env_int(name: str, default: int) -> int:
    v = os.getenv(name)
    return default if v is None else int(v)

@dataclass(frozen=True)
class Settings:
    env: str = os.getenv("ENV", "local")
    log_level: str = os.getenv("LOG_LEVEL", "INFO").upper()
    rabbit_thread:str = os.getenv("RABBIT_THREAD", 'EV_SEND')
    rabbit_url:str=os.getenv("RABBIT_THREAD","amqp://guest:guest@localhost/")
settings = Settings()