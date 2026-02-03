import os

from dataclasses import dataclass

def env_int(name: str, default: int) -> int:
    v = os.getenv(name)
    return default if v is None else int(v)

@dataclass(frozen=True)
class Settings:
    
    env: str = os.getenv("ENV", "local")
    log_level: str = os.getenv("LOG_LEVEL", "INFO").upper()

    gateway_url: str = os.getenv("GATEWAY_REPORTER_URL", "http://127.0.0.1:8000/permanent/displayable")
    gateway_timeout:int=env_int("GATEWAY_TIMEOUT",30)
    
    #temp_graphs_path:str=os.getenv("TEMP_GEN_GRAPHS_PATH","C:\Users\jeras\Documents\PowerView\backend_pv\OnDemand\report_generator\temp\gen_graphs")
    #graph_path:str=os.getenv("GRAPH_PATH",'/OnDemand/report_generator/temp/gen_graphs')

settings = Settings()