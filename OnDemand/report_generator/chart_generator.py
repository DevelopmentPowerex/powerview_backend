import asyncio 
from typing import Optional,Any,Dict,List

from .protocols.auxiliar_info import PARAMETER_TRANSLATION, PARAMETERS_FOR_EVENTS, PARAMETERS_FOR_REPORT, PARAMETERS_CHART_ORDER, PREMADE_ORDERS
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

async def clean_normal_chart_data(circuits:List[int],measurements:List[Dict[str,Any]],start_date:str,end_date:str):
    try:
        graphs_list=[]
        
        for circuit in circuits:
            circuit_graphs={}
            parameter_reading={}
            
            circuit_graphs['meter_id']=circuit['id']
            for report_parameter in PREMADE_ORDERS.keys():
                
                specific_val=PREMADE_ORDERS[report_parameter][0]           
                measurement_points=[]
                for measurement in measurements:
                    
                    if circuit['id']==measurement['id']: 
                        parameter_point={}

                        for parameter in specific_val:
                            parameter_point[parameter]=measurement['reading'][parameter]

                        parameter_point['point']=measurement['timestamp']
                        measurement_points.append(parameter_point)

                parameter_reading[report_parameter]=measurement_points
                
            circuit_graphs['graphs']=parameter_reading
            graphs_list.append(circuit_graphs)

        return graphs_list
    except Exception:
        logger.exception("Error preparing the data for chart generation")
        return None

async def gen_normal_graphs(circuits:List[int],measurements:List[Dict[str,Any]],start_date:str,end_date:str): 

    clean_data=await clean_normal_chart_data(circuits,measurements,start_date,end_date)
    if not clean_data:
        logger.error("Error preparing the measurements for chart generation")
        return None

    """
    graph_path=await generate_individual_chart(PREMADE_ORDERS[report_parameter],meter_reading)
    
    graphs_list.append({
        "name": report_parameter,  
        "image": graph_path
    })
                
    new_graphs_list.append({
        'meter_id':circuit['id'],
        'start_time':start_date,
        'end_time':end_date,
        "behaviour_images":graphs_list,
    })
            
    logger.info(new_graphs_list)
    """

    return new_graphs_list

async def generate_report_charts(circuits,readings,events,start_date,end_date):
    
    normal_graphs_list=await gen_normal_graphs(circuits,readings,start_date,end_date) #GENERAR LAS GRÁFICAS PARA EL REPORTE
    
    if not normal_graphs_list:
        logger.error('Error while generating the normal charts')
    
    """
    event_graphs=await get_event_graphs(event_register) #GENERAR GRAFICAS ENFOCADAS EN MOSTRAR LOS EVENTOS ANTERIORES
    if not event_graphs:
        logger.error('Error while generating the event charts')
    """

    return []

