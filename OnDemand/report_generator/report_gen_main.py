from dotenv import load_dotenv
load_dotenv("./OnDemand/report_generator/.env.local")

import asyncio
from typing import Optional,Any,Dict,List

from OnDemand.report_generator.auxiliar.date_info import dates_info as get_report_dates
from OnDemand.report_generator.report_details import fetch_report_data
from OnDemand.report_generator.chart_generator import generate_report_charts
#from OnDemand.report_generator.html_render import generate_html_report as generate_html

from .config import settings

from .shared.logging_config import setup_logging
setup_logging(settings.log_level)

import logging
logger = logging.getLogger(__name__)

TEMPLATE_DIR = "OnDemand/uS/generate_report/static/templates/"

OUTPUT_HTML = "OnDemand/uS/generate_report/result/editable_report.html"

async def build_order(circuit_list,dates_part,parameters_list,normal_graphs,events_table,events_graphs): #Formar la orden JSON para el renderizador de la plantilla HTML
    
    """
    report_data = {
        "report_info":{
            "gen_date": "11/09/2025",
            "date_range_start": "01/08/2025",
            "date_range_end": "31/08/2025",
            "csv_code":"Indurama_0108_3108"
        },
        "project_info":{
            "client_name": "INDURAMA ECUADOR S.A.",
            "project_name": "Laboratorios RI",
            "fae": {
                "company_name":"PREMIUMENERGIA SAS",
                "engineer_name":"Ing. Jeramhil Javier Solis Yari",
                "email_addr":"proyectos@premium-energia.com",
                "phone":"0984373697"
            },
            "meters_list": ['PV-M3'],
        },
        "circuits_list": [
            {
                "name": "Alimentación Laboratorio 7",
                "parameters_list": [
                    {
                        "name": "FRECUENCIA [Hz]",
                        "param_values": [
                            {"name": "F", "max": 60.23, "min": 59.88, "prom": 59.98}
                        ]
                    }
                ],
                
                "behaviour_images": [
                    {
                    "name": "Voltajes por línea [V]",
                    "image": "/public_access/uS_public_service/generate_report/static/img/v1.png"
                    },
                    {
                    "name": "Corrientes por línea [A]",
                    "image":"/public_access/uS_public_service/generate_report/static/img/i2.png"
                    }
                ]
            }
        ],
        "events":{
            "table_info":[
                {
                "broken_rule":"iA>0",
                "first_event":"08:30",
                "last_event":"12:52",
                "event_counter":"20"
                },
                {
                "broken_rule":"VA=0",
                "first_event":"22:00",
                "last_event":"23:20",
                "event_counter":"30"
                }
            ],
            "events_images":[
                {
                "name": "Alarma 1",
                "image": "/public_access/uS_public_service/generate_report/static/img/grafica.jpg"
                },
                {
                "name": "Alarma 2",
                "image":"/public_access/uS_public_service/generate_report/static/img/grafica.jpg"
                }
            ]
        }
    }
    """
    circuits_estructure=[]

    for index,key in enumerate(circuit_list):
        circuits_estructure.append({
                "name": circuit_list[key],
                "parameters_list": parameters_list[index]['extreme_values'],
                "behaviour_images": normal_graphs[index]['behaviour_images']
            })
                
    report_data = {
        "report_info":dates_part,
        "circuits_list": circuits_estructure,
        "events":{
            "table_info":events_table,
            "events_images":events_graphs
        }
    }
    
    #logger.info(report_data)
    
    return report_data

async def report_gen(client_name:str,
                     project_name:str,
                     start_date:str,
                     end_date:str): 
    
    dates_part = await get_report_dates(start_date,end_date) #RANGO DE FECHAS Y CODIGO CSV
    logger.debug(dates_part)
    if not dates_part:
        logger.error('Error while getting the date range')
        return None
    
    report_readings= await fetch_report_data(client_name,project_name,start_date,end_date)
    logger.debug(report_readings['events'])
    if not report_readings:
        return None
    
    report_images=await generate_report_charts(report_readings)
    if not report_images:
        return None
    """
    new_report_order= await build_order(report_readings, report_images)
    if not new_report_order:
        logger.error('Error while generating the report order')

    html_report= await generate_html(TEMPLATE_DIR, OUTPUT_HTML, new_report_order)
    if not html_report:
        logger.error('Error while rendering the html report')
    
    return []
    """
    

async def main():
    test_report=await report_gen('ELECTROPROTECCIONES SAS','Proyecto A',"2026-01-19T17:48:00","2026-01-20T12:00:00")

if __name__ == "__main__":  

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt: Shutting down service")


