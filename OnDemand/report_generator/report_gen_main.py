from dotenv import load_dotenv
load_dotenv("./OnDemand/report_generator/.env.local")

import asyncio
from typing import Optional,Any,Dict,List

from OnDemand.report_generator.auxiliar.date_info import dates_info as get_report_dates
from OnDemand.report_generator.report_details import fetch_report_data
from OnDemand.report_generator.chart_generator import generate_report_charts
from OnDemand.report_generator.render_html import generate_html_report as generate_html
from OnDemand.report_generator.render_pdf import render_to_pdf as html_to_pdf
from OnDemand.report_generator.create_csv import generate_csv
from OnDemand.report_generator.compress_reports import compress_to_zip

from .config import settings

from .shared.logging_config import setup_logging
setup_logging(settings.log_level)

import logging
logger = logging.getLogger(__name__)

async def build_order(client_name:str,
                      project_name:str,
                      dates_part:Dict[str,Any],
                      circuits_per_project:List[Dict[str,Any]], 
                      readings_for_report:List[Dict[str,Any]], 
                      events_for_report:List[Dict[str,Any]],
                      charts_for_report:Dict[str,Any]
                      )->Dict[str,Any]:
    
    dates_part["csv"]=client_name.replace(" ","_").lower()+"_"+project_name.lower().replace(" ","_")+dates_part["csv"]
 
    models_list=[]
    clear_data_list=[]
    for circuit in circuits_per_project:
        
        models_list.append(circuit['model_name'])
        
        for data_set in readings_for_report:
            if data_set['meter_id']==circuit['id']:
                clear_data_list.append({
                    "name": circuit['nickname'],
                    "parameters_list":data_set['extreme_values'],
                    "behaviour_images": charts_for_report.get(circuit['id'],[])
                })
                break
        
    new_events_list=[]
    for event in events_for_report:
        match event.get('level'):
            case 1:
                new_level="LOW"
            case 2:
                new_level="MID"
            case 3:
                new_level="CRITICAL"
            case _:
                new_level="LOW"

        new_events_list.append({
            "circuit":event.get('circuit'),
            "context":event.get('context'),
            "rule":event.get('parameter')+event.get('comparator')+str(event.get('threshold')),
            "level":new_level,
            "first_event":event.get('1st_ts'),
            "last_event":event.get('last_ts'),
            "event_counter":event.get('event_counter')
        })

        
    project_info={
        "client_name":client_name,
        "project_name": project_name,
        "fae": {
            "company_name":"PREMIUMENERGIA SAS",
            "engineer_name":"Ing. Jeramhil Javier Solis Yari",
            "email_addr":"proyectos@premium-energia.com",
            "phone":"0984373697"
        },
        "meters_list": list(dict.fromkeys(models_list)),
    }

    report_data = {
        "report_info":dates_part,
        "project_info":project_info,
        "circuits_list": clear_data_list,
        "events":new_events_list
    }
     
    return report_data

async def report_gen(client_name:str,project_name:str,start_date:str, end_date:str)->Optional[str]:
    
    dates_part = await get_report_dates(start_date,
                                        end_date)
    if not dates_part:
        logger.error('Error while getting the date range')
        return None
    logger.debug(dates_part)

    report_readings= await fetch_report_data(client_name,
                                             project_name,
                                             start_date,
                                             end_date)
    if not report_readings:
        logger.error("Error fetching the project readings")
        return None
    logger.debug(report_readings['report'])

    charts_for_report=await generate_report_charts(report_readings.get('circuits'),
                                                   report_readings.get('readings'))
    if not charts_for_report:
        return None
    logger.debug(charts_for_report)

    new_report_order= await build_order(client_name,project_name,dates_part, 
                                        report_readings.get('circuits'), 
                                        report_readings.get('report'),
                                        report_readings.get('events'), 
                                        charts_for_report)
    if not new_report_order:
        logger.error('Error while generating the report order')
        return None
    logger.debug(new_report_order)

    html_parts= await generate_html(new_report_order)
    if not html_parts:
        logger.error('Error while rendering the html templates')
        return None
    logger.debug(html_parts)
    
    pdf_report= await html_to_pdf(html_parts)
    if not pdf_report:
        logger.error("Error rendering from html report to pdf")
        return None
    logger.debug(f'PDF report generated and saved on: {pdf_report}')

    excel_archive= await generate_csv(report_readings.get('circuits'),
                                    report_readings.get('readings'))
    if not excel_archive:
        logger.error("Error creating the csv register")
        return None
    logger.debug(f'Excel archive generated and saved on: {excel_archive}')

    final_zip= await compress_to_zip(pdf_report,
                                     excel_archive,
                                    r"OnDemand\report_generator\result\report.zip")
    if not final_zip:
        logger.error("Error compressing the report archives")
        return None
    logger.debug(f'Zip archive generated and saved on: {final_zip}')

    return final_zip
    
    

async def main():
    test_report=await report_gen('Cooperativa Jardín Azuayo','Proyecto A',"2026-01-19T17:48:00","2026-01-20T12:00:00")

if __name__ == "__main__":  

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt: Shutting down service")


