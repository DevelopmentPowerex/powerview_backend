import os

from dataclasses import dataclass

def env_int(name: str, default: int) -> int:
    v = os.getenv(name)
    return default if v is None else int(v)

@dataclass(frozen=True)
class Settings:
    env: str = os.getenv("ENV", "local")
    log_level: str = os.getenv("LOG_LEVEL", "INFO").upper()
    gateway_url: str = os.getenv("GATEWAY_EVALUATOR_URL", "http://gateway:8000/permanent/rule_evaluator")
    gateway_timeout:int=env_int("GATEWAY_TIMEOUT",30)
    rabbit_thread:str=os.getenv("RABBIT_EVALUATOR_THREAD","EV_RECV")
    rabbit_url:str=os.getenv("RABBIT_URL","amqp://powerview:powerview@rabbitmq/")

settings = Settings()