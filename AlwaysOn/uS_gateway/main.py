#script principal para el uS de gaeway
#Este uS es la única con acceso a la DB, todos los otros uS deben comunicarse con la Db através de él
from fastapi import FastAPI
from DB.database import init_db
from contextlib import asynccontextmanager

from .routes.evaluate_readings_routes import router as evaluator_router
from .routes.collect_readings_routes import router as collector_router
from .routes.notify_events_routes import router as notifier_router

from OnDemand.gateway_connection.routes.extract_events_routes import router as extract_event_router
from OnDemand.gateway_connection.routes.extract_readings_routes import router as extract_measurements_router

#Aqui van los protocolos

from dotenv import load_dotenv
load_dotenv("./AlwaysOn/uS_gateway/.env.local")

from .config import settings
from .shared.logging_config import setup_logging

setup_logging(settings.log_level)

import logging
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init_db()  
        logger.info("DB initialized")
        yield
    except Exception as e:
        logger.critical(f"Error DB init: {e}")
        raise
    
app = FastAPI(
    title="PowerView Internal Gateway",
    description="API gateway dedicated to PowerView structure",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(collector_router)
app.include_router(evaluator_router)
app.include_router(notifier_router)
app.include_router(extract_measurements_router)
app.include_router(extract_event_router)

@app.get("/")
async def root():
    return {"message": "Gateway de microservicios en línea"}


@app.get("/health")
async def health():
    return {"status": "Todo bien padre santo"}
