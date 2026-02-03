import asyncio 
from typing import Optional,Any,Dict,List

from .protocols.auxiliar_info import PARAMETER_TRANSLATION, PARAMETERS_FOR_EVENTS, PARAMETERS_FOR_REPORT, PARAMETERS_CHART_ORDER, PREMADE_ORDERS
from OnDemand.report_generator.auxiliar.normal_graphs import chart_order as create_charts

import logging
logger = logging.getLogger(__name__)

async def clean_chart_data(circuits:List[int],measurements:List[Dict[str,Any]],start_date:str,end_date:str):
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

async def generate_report_charts(circuits:List[int],measurements:List[Dict[str,Any]],start_date:str,end_date:str): 

    clean_data=await clean_chart_data(circuits,measurements,start_date,end_date)
    if not clean_data:
        logger.error("Error preparing the measurements for chart generation")
        return None

    charts_per_meter=await create_charts(clean_data)
    if not charts_per_meter:
        logger.error("Error generating the required charts")
        return None

    return charts_per_meter


