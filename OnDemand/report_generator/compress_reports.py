from typing import Dict,Any
from pathlib import Path
import zipfile
import tempfile

import logging
logger = logging.getLogger(__name__)

async def compress_to_zip(pdf_report:str,
                           excel_report:str,
                           final_zip:str):
    
    pdf_path=Path(pdf_report)
    xlsx_path=Path(excel_report)
    zip_path=Path(final_zip)

    if not pdf_path.exists() or not xlsx_path.exists():
        logger.error("Missing archives")
        return None

    try:
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(pdf_path, arcname="report.pdf")
            zipf.write(xlsx_path, arcname="report.xlsx")
        
        return zip_path
        
    except Exception:
        logger.exception("Error compressing both reports")
        if zip_path.exists():
            zip_path.unlink()
        return None
