import os

from dataclasses import dataclass

def env_int(name: str, default: int) -> int:
    v = os.getenv(name)
    return default if v is None else int(v)

@dataclass(frozen=True)
class Settings:
    
    env: str = os.getenv("ENV", "local")
    log_level: str = os.getenv("LOG_LEVEL", "INFO").upper()

    mqtt_broker: str = os.getenv("MQTT_BROKER", "localhost")
    mqtt_port: int = env_int("MQTT_PORT", 1883)
    mqtt_topic: str = os.getenv("MQTT_TOPIC", "powerview/+/reading/+")
    mqtt_identifier: str = os.getenv("MQTT_IDENTIFIER", "powerview_developer")
    mqtt_timeout: int = env_int("MQTT_TIMEOUT", 60)

    gateway_url: str = os.getenv("GATEWAY_COLLECTOR_URL", "http://gateway:8000/permanent/reading_collector")
    gateway_timeout:int=env_int("GATEWAY_TIMEOUT",30)
    tasks_max: int = env_int("TASKS_MAX", 50)

settings = Settings()