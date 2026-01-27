import os

from dataclasses import dataclass

def env_int(name: str, default: int) -> int:
    v = os.getenv(name)
    return default if v is None else int(v)

@dataclass(frozen=True)
class Settings:
    env: str = os.getenv("ENV", "local")
    log_level: str = os.getenv("LOG_LEVEL", "INFO").upper()

    gateway_url: str = os.getenv("GATEWAY_NOTIFIER_URL", "http://gateway:8000/permanent/alarm_processing")
    gateway_timeout:int=env_int("GATEWAY_TIMEOUT",30)
    tasks_max: int = env_int("TASKS_MAX", 50)
    rabbit_thread:str = os.getenv("RABBIT_NOTIFIER_THREAD", "NOTIF")
    rabbit_URL:str = os.getenv("RABBIT_URL","amqp://powerview:powerview@rabbitmq/")
    
    smtp_server:str = os.getenv("SMTP_SERVER","mail.premium-energia.com")
    smtp_port:int = env_int("SMTP_PORT",465)
    smtp_user:str = os.getenv("SMTP_USERNAME","monitoreo@premium-energia.com")
    smtp_password:str = os.getenv("SMTP_PASSWORD","m0n1t0r30.")

settings = Settings() 