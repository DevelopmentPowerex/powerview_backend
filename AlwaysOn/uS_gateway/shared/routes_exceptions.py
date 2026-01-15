from fastapi import HTTPException

import logging
logger = logging.getLogger(__name__)

def handle_service_errors(logger, exc: Exception):
    if isinstance(exc, ValueError):
        raise HTTPException(400, detail=str(exc))
    logger.exception("Unexpected service error")
    raise HTTPException(500, detail="Internal server error")
