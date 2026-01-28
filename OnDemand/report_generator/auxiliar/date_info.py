import asyncio
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
    
    except Exception as e:
        logger.error(f"Error while making the csv stamp")
        return None

async def format_gen_date()->Optional[datetime]:
    gen_date=date.today().isoformat()
    return gen_date

async def separate_range(start_info:str,end_info:str)->Optional[Dict[str,Any]]:

    date_start, hour_start = start_info.split("T")
    date_end, hour_end = end_info.split("T")

    final_range={
        "date_start":date_start,
        "hour_start":hour_start,
        "date_end":date_end,
        "hour_end":hour_end,
    }

    return final_range

async def report_info(start_report:str,end_report:str)->Optional[Dict[str,Any]]:
    
    gen_date=await format_gen_date()

    datestamp=await get_csv_date(start_report,end_report)

    final_date_range=await separate_range(start_report,end_report)

    report_info={
        "gen_date": gen_date,
        "date_range_start": final_date_range['date_start'],
        "hour_start":final_date_range['hour_start'],
        "date_range_end": final_date_range['date_end'],
        "hour_end":final_date_range['hour_end'],
        "csv_2nd":datestamp
    }

    return report_info

if __name__ == "__main__":  
    
    start_date = '2025-09-15T23:50:12'
    end_date = '2025-09-16T09:48:33'

    formated = asyncio.run(report_info(start_date,end_date))

    if formated:
        logger.info(formated) 
        
    else:
        logger.error('mal mal mal') 