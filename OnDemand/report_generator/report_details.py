import asyncio
from typing import Optional,Any,Dict,List

from OnDemand.report_generator.auxiliar.circuits_per_project import get_project_circuits
from OnDemand.report_generator.auxiliar.date_info import dates_info as get_report_dates
from OnDemand.report_generator.auxiliar.measures_obtain import extract_all as extract_measures
from OnDemand.report_generator.auxiliar.extract_events import extract_order as extract_events

from protocols.auxiliar_info import PARAMETER_TRANSLATION, PARAMETERS_FOR_EVENTS, PARAMETERS_FOR_REPORT, PARAMETERS_CHART_ORDER

import logging
logger = logging.getLogger(__name__)

async def get_readings(circuit_list:Dict[str,Any],start_date:str,end_date:str): 
    """
    circuit_list: [{
            'meter_id':int,
            'circuit_name':str,
            'meter_model': str,
            'sn':str
        },...]
    
    Retorno: 2 listas-> 1 tiene todas las mediciones de cada uno de los medidores, cada item es un medidor
                     -> 2 tiene todos los valores extremos y promedio de cada una de las mediciones de la lista 1
    
    """
    measurements_list=[]
    extreme_values_list=[]

    for circuit_index in circuit_list:
        circuit_measure,circuit_extremes= await extract_measures(circuit_index['meter_id'],start_date,end_date)
        measurements_list.append(circuit_measure)
        extreme_values_list.append(circuit_extremes)

    return measurements_list,extreme_values_list

async def translate_values(extreme_values:List[Dict[str,Any]]): 
    """
    extreme_values: Lista con todos los valores extremos de cada parámetro eléctrico 
                    bajo el formato de:

                    [{'meter_id': int,
                    'start_time': str, 
                    'end_time': str, 
                    'extreme_values': {
                                        'param_name': {'max': , 'min': , 'prom': }
                                        }
                    }]

    Retorno una lista de diccionarios, con formato:
        [
            {
                'meter_id': int, 
                'start_time': str, 
                'end_time': str, 
                'extreme_values': {
                    Orden1: [
                        {'name': 'vA', 'max': 120.9, 'min': 118.1, 'prom': 119.7}, 
                        {'name': 'vB', 'max': 124.8, 'min': 120.9, 'prom': 123.34}, 
                        {'name': 'vC', 'max': 124.7, 'min': 122, 'prom': 123.1}
                    ],
                    Orden2:[]
                }
            }
        ]
    """

    translated_extremes=[]

    for extremes_item in extreme_values:
        extreme_dict=extremes_item['extreme_values']
        new_extremes={}

        for report_parameter in PARAMETERS_FOR_REPORT.keys():
            new_param_values=[] 
            for parameter in PARAMETERS_FOR_REPORT[report_parameter]:
                
                if not(extreme_dict[parameter]['max'] == 0 and extreme_dict[parameter]['min'] ==0 and extreme_dict[parameter]['prom'] == 0)  :
                    item={
                        'name':parameter,
                        'max':extreme_dict[parameter]['max'],
                        'min':extreme_dict[parameter]['min'],
                        'prom':extreme_dict[parameter]['prom']
                    }
                    
                    new_param_values.append(item)

            new_extremes.update({
                report_parameter:new_param_values
            })

        translated_extremes.append({
            'meter_id':extremes_item['meter_id'],
            'start_time':extremes_item['start_time'],
            'end_time':extremes_item['end_time'],
            'extreme_values':new_extremes,
        })
    #logger.info(translated_extremes)
    return translated_extremes
    
async def get_events(circuit_list:Dict[str,Any],start_date:str,end_date:str): 
    
    meter_list=[]

    for circuit_key in circuit_list.keys():
        meter_list.append(circuit_key)

    events_list= await extract_events(meter_list,start_date,end_date)
    
    return events_list

async def fetch_report_data(client_name:str,
                     project_name:str,
                     start_date:str,
                     end_date:str):
    
    circuits_dict=await get_project_circuits(client_name,project_name) #DATOS DEL PROYECTO
    if not circuits_dict:
        logger.error(f'Error fetching the meters of {project_name}')
        return None
    
    dates_part = await get_report_dates(start_date,end_date) #RANGO DE FECHAS Y CODIGO CSV
    if not dates_part:
        logger.error('Error while getting the date range')

    measurements,extreme_values=await get_readings(circuits_dict,start_date,end_date) #EXTRAER MEDICIONES PARA EL REPORTE
    if not (measurements and extreme_values):
        logger.error('Error while getting the readings information')
    
    parameters_list=await translate_values(extreme_values) #FORMATEAR VALORES EXTREMOS PARA SU USO
    if not parameters_list:
        logger.error('Error while ordering the measurements')
    
    event_list,event_register=await get_events(circuits_dict,start_date,end_date) #EXTRAER EL REGISTRO DE EVENTOS 
    if not event_list:
        logger.error('Error while obtaining the events/alarms register')
    
    report_details={

    }

    return report_details