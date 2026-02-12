from datetime import datetime, date
from typing import Optional,Any,Dict

import logging
logger = logging.getLogger(__name__)

async def get_csv_date(start_date:str,end_date:str)->Optional[str]:
    try:
        start_nmr = datetime.fromisoformat(start_date)
        end_nmr = datetime.fromisoformat(end_date)
        start_format=start_nmr.strftime("%d%m")
        end_format=end_nmr.strftime("%d%m")
        datestamp="_"+start_format+"_"+end_format
        
        return datestamp
    
    except Exception:
        logger.exception(f"Error making the csv stamp")
        return None

async def format_gen_date()->Optional[datetime]:
    try:
        gen_date=date.today().isoformat()
        return gen_date
    except Exception:
        logger.exception(f"Error formatting the dates")
        return None
    
async def separate_range(start_info:str,end_info:str)->Optional[Dict[str,Any]]:
    try:

        date_start, hour_start = start_info.split("T")
        date_end, hour_end = end_info.split("T")

        final_range={
            "date_start":date_start,
            "hour_start":hour_start,
            "date_end":date_end,
            "hour_end":hour_end,
        }

        return final_range
    
    except Exception:
        logger.exception(f"Error while separating the dates")
        return None

async def dates_info(start_report:str,end_report:str)->Optional[Dict[str,Any]]:
    try:
        gen_date=await format_gen_date()
        if not gen_date:
            return None
        
        datestamp=await get_csv_date(start_report,end_report)
        if not datestamp:
            return None

        final_date_range=await separate_range(start_report,end_report)
        if not final_date_range:
            return None
        
        return{
            "gen_date": gen_date,
            "date_range_start": final_date_range['date_start'],
            "date_range_end": final_date_range['date_end'],
            "csv":datestamp
        }

    except Exception:
        logger.exception("Error processing the report dates")
        return None
