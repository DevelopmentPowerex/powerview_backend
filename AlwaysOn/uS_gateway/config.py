import os

from dataclasses import dataclass

def env_int(name: str, default: int) -> int:
    v = os.getenv(name)
    return default if v is None else int(v)

def env_bool(name: str, default: bool) -> bool:
    v = os.getenv(name)
    if v is None:
        return default
    return v.strip().lower() in ("1", "true", "t", "yes", "y", "on")

@dataclass(frozen=True)
class Settings:
    env: str = os.getenv("ENV", "local")
    log_level: str = os.getenv("LOG_LEVEL", "INFO").upper()
    
    rabbit_thread:str = os.getenv("RABBIT_COLLECTOR_THREAD", 'EV_SEND')
    rabbit_url:str=os.getenv("RABBIT_URL","amqp://guest:guest@localhost/")
    
    db_url:str=os.getenv("DB_URL","postgresql+asyncpg://jera:105181@localhost:5432/powerview")
    db_echo:bool=env_bool("DB_ECHO",False)
    db_pool_size: int = env_int("DB_POOL_SIZE", 10)
    db_max_overflow: int = env_int("DB_MAX_OVERFLOW", 5)

settings = Settings()