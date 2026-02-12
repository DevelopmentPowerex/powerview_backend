from fastapi.responses import FileResponse
from pathlib import Path


from OnDemand.report_generator.report_gen_main import report_gen

from fastapi import APIRouter, Query

import logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/report",  
    tags=["Archive generator"]    
)

@router.get("/generate")
async def obtain_events(client_name: str = Query(...), 
                        project_name:str= Query(...),
                        from_date:str= Query(...),
                        to_date: str = Query(...)):
    try:
        report_archives=await report_gen(client_name,project_name,from_date,to_date)
        if report_archives:
            zip_path = Path(report_archives)

            return FileResponse(
                    path=zip_path,
                    media_type="application/zip",
                    filename="report.zip"
            )
        
    except Exception:
        logger.exception(f"Error while generating pdf and excel report for {project_name}")
        return None
    
