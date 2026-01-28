import asyncio 
from typing import Optional,Any,Dict,List

from protocols.auxiliar_info import PARAMETER_TRANSLATION, PARAMETERS_FOR_EVENTS, PARAMETERS_FOR_REPORT, PARAMETERS_CHART_ORDER
from OnDemand.report_generator.auxiliar.normal_graphs import chart_order as generate_individual_chart

import logging
logger = logging.getLogger(__name__)

async def get_event_graphs(event_register): 
    #logger.info(event_register)
    return[
                {
                "name": "Alarma 1",
                "image": "/OnDemand/uS/generate_report/static/img/grafica.jpg"
                },
                {
                "name": "Alarma 2",
                "image":"/OnDemand/uS/generate_report/static/img/grafica.jpg"
                }
            ]
async def get_normal_graphs(measurements:List[List[Dict[str,Any]]],start_date:str,end_date:str): 
    """
    measurements: Lista cuyos elementos son otras listas
                  Las listas internas tienen cada una de las mediciones para cada medidor

    [
        [
            {
                'meter_id': int, 
                'parameters': {'F': 59.96, 'R_kvarh_C': 106, 'R_kvarh_T': 388}, 
                'timestamp': str}
            }
        ]
    ]
    """
    new_graphs_list=[]
    graphs_list=[]

    for individual_meter in measurements:
        
        for report_parameter in PARAMETERS_FOR_REPORT.keys():
            graph_path=await generate_individual_chart([PARAMETERS_CHART_ORDER[report_parameter]],individual_meter)
            
            graphs_list.append({
                "name": report_parameter,
                "image": graph_path
            })
                    
        new_graphs_list.append({
            'meter_id':individual_meter[0]['meter_id'],
            'start_time':start_date,
            'end_time':end_date,
            "behaviour_images":graphs_list,
        })
        
    #logger.info(new_graphs_list)
    return new_graphs_list

async def generate_report_charts():

    normal_graphs_list=await get_normal_graphs(measurements,start_date,end_date) #GENERAR LAS GRÁFICAS PARA EL REPORTE
    if not normal_graphs_list:
        logger.error('Error while generating the normal charts')
    
    """
    event_graphs=await get_event_graphs(event_register) #GENERAR GRAFICAS ENFOCADAS EN MOSTRAR LOS EVENTOS ANTERIORES
    if not event_graphs:
        logger.error('Error while generating the event charts')
    """

    return []

