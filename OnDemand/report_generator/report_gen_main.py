import asyncio
from typing import Optional,Any,Dict,List

from OnDemand.uS.auxiliar.date_info import report_info as get_dates
from OnDemand.uS.auxiliar.project_info import project_data_extraction as get_project_and_fae
from OnDemand.uS.auxiliar.measures_obtain import extract_all as extract_measures
from OnDemand.uS.auxiliar.normal_graphs import chart_order as generate_individual_chart
from OnDemand.uS.auxiliar.extract_events import extract_order as extract_events
from OnDemand.uS.generate_report.html_render import generate_html_report as generate_html

import logging
logger = logging.getLogger(__name__)

PARAMETER_TRANSLATION={
    "vA":('V','Voltaje entre Fase A  y Neutro [vA]'),
    "vB":('V','Voltaje entre Fase B  y Neutro [vB]'),
    "vC":('V','Voltaje entre Fase C  y Neutro [vC]'),
    "vAB":('V','Voltaje entre Fases  A y B [vAB]'),
    "vBC":('V','Voltaje entre Fases  B y C [vBC]'),
    "vCA":('V','Voltaje entre Fases  C y A [vCA]'),
    "iA":('A','Corriente en Fase A [iA]'),
    "iB":('A','Corriente en Fase B [iB]'),
    "iC":('A','Corriente en Fase C [iC]'), 
    "PA":('W','Potencia Activa en Fase A [PA]'),
    "PB":('W','Potencia Activa en Fase B [PB]'), 
    "PC":('W','Potencia Activa en Fase C [PC]'),
    "P":('W','Potencia Activa Total [P]'),
    "QA":('VAR','Potencia Reactiva en Fase A [QA]'), 
    "QB":('VAR','Potencia Reactiva en Fase B [QB]'),
    "QC":('VAR','Potencia Reactiva en Fase C [QC]'),
    "Q":('VAR','Potencia Reactiva Total [Q]'),
    "SA":('VA','Potencia Aparente en Fase A [SA]'),
    "SB":('VA','Potencia Aparente en Fase B [SB]'), 
    "SC":('VA','Potencia Aparente en Fase C [SC]'), 
    "S" :('VA','Potencia Aparente Total [S]'),
    "PFA":('','Factor de Potencia en Fase A [PFA]'),
    "PFB":('','Factor de Potencia en Fase B [PFB]'),
    "PFC":('','Factor de Potencia en Fase C [PFC]'),
    "PF":('','Factor de Potencia General [PF]'),
    "F":('Hz','Frecuencia [F]'), 
    "TA":('°C','Temperatura en Fase A [TA]'),
    "TB":('°C','Temperatura en Fase B [TB]'), 
    "TC":('°C','Temperatura en Fase C [TC]'), 
    "TN":('°C','Temperatura en Neutro [N]'),
    "iF":('A','Corriente de Fuga [iF]'),
    "V_unb":('%','Porcentaje de Desbalance de Voltaje'),
    "I_unb":('%','Porcentaje de Desbalance de Corriente'),
    "P_kWh_T":('kWh','Energía Activa Positiva Total') ,
    "R_kWh_T":('kWh','Energía Activa Inversa Total'),
    "P_kvarh_T":('kVarh','Energía Reactiva Positiva Total'),
    "R_kvarh_T":('kVarh','Energía Reactiva Inversa Total'),
    "DI_status":('bit','Estado de las entradas digitales'), #(bit0:DI1,bit1:DI2,bit2:DI3,bit3:DI4)
    "P_kWh_A":('kWh','Energía activa en A: Positiva'),
    "R_kWh_A":('kWh','Energía activa en A: Inversa'),
    "P_kvarh_A":('kVarh','Energía reactiva en A: Positiva'),
    "R_kvarh_A":('kVarh','Energía reactiva en A: Inversa'),
    "P_kWh_B":('kWh','Energía activa en B: Positiva'),
    "R_kWh_B":('kWh','Energía activa en B: Inversa'),
    "P_kvarh_B":('kVarh','Energía reactiva en B: Positiva'),
    "R_kvarh_B":('kVarh','Energía reactiva en B: Inversa'),
    "P_kWh_C":('kWh','Energía activa en C: Positiva'),
    "R_kWh_C":('kWh','Energía activa en C: Inversa'),
    "P_kvarh_C":('kVarh','Energía reactiva en C: Positiva'),
    "R_kvarh_C":('kVarh','Energía reactiva en A: Inversa'),
    "THD_A":('%','Rate de armónicos en A'),
    "THD_B":('%','Rate de armónicos en B'),
    "THD_C":('%','Rate de armónicos en C'),
    "THDC_A":('%','Rate de armónicos de corriente en A'), 
    "THDC_B":('%','Rate de armónicos de corriente en B'), 
    "THDC_C":('%','Rate de armónicos de corriente en C')
}

PARAMETERS_FOR_EVENTS={
    "vA":'Voltaje entre Fase A  y Neutro [V]',
    "vB":'Voltaje entre Fase B  y Neutro [V]',
    "vC":'Voltaje entre Fase C  y Neutro [V]',

    "vAB":'Voltaje entre Fases  A y B [V]',
    "vBC":'Voltaje entre Fases  B y C [V]',
    "vCA":'Voltaje entre Fases  C y A [V]',

    "iA":'Corriente en Fase A [A]',
    "iB":'Corriente en Fase B [A]',
    "iC":'Corriente en Fase C [A]', 

    "PA":'Potencia Activa en Fase A [kW]',
    "PB":'Potencia Activa en Fase B [kW]', 
    "PC":'Potencia Activa en Fase C [kW]',
    "P":'Potencia Activa Total [kW]',

    "QA":'Potencia Reactiva en Fase A [kVar]', 
    "QB":'Potencia Reactiva en Fase B [kVar]',
    "QC":'Potencia Reactiva en Fase C [kVar]',
    "Q":'Potencia Reactiva Total [kVar]',

    "SA":'Potencia Aparente en Fase A [kVA]',
    "SB":'Potencia Aparente en Fase B [kVA]', 
    "SC":'Potencia Aparente en Fase C [kVA]', 
    "S" :'Potencia Aparente Total [kVA]',

    "PF":'Factor de Potencia General',
    "F":'Frecuencia [Hz]', 

    "P_kWh_A":'Energía activa en A: Positiva [kWh]',
    "P_kWh_B":'Energía activa en B: Positiva [kWh]',
    "P_kWh_C":'Energía activa en C: Positiva [kWh]',
    "P_kWh_T":'Energía Activa Positiva Total [kWh]',

    "R_kWh_A":'Energía activa en A: Inversa [kWh]',
    "R_kWh_B":'Energía activa en B: Inversa [kWh]',
    "R_kWh_C":'Energía activa en C: Inversa [kWh]',
    "R_kWh_T":'Energía Activa Inversa Total [kWh]',

    "P_kvarh_A":'Energía reactiva en A: Positiva [kVarh]',
    "P_kvarh_B":'Energía reactiva en B: Positiva [kVarh]',
    "P_kvarh_C":'Energía reactiva en C: Positiva [kVarh]',
    "P_kvarh_T":'Energía Reactiva Positiva Total [kVarh]',

    "R_kvarh_A":'Energía reactiva en A: Inversa [kVarh]',
    "R_kvarh_B":'Energía reactiva en B: Inversa [kVarh]',
    "R_kvarh_C":'Energía reactiva en C: Inversa [kVarh]',
    "R_kvarh_T":'Energía Reactiva Inversa Total [kVarh]',
}

PARAMETERS_FOR_REPORT={
    "Voltajes por línea [V]":["vA","vB","vC"],
    "Voltajes por fase [V]":["vAB","vBC","vCA"],
    "Corrientes por línea [A]":["iA","iB","iC"],
    "Potencia Activa [W]":['P',"PA","PB","PC"],
    "Potencia Reactiva [VAR]":["Q","QA","QB","QC"],
    "Potencia Aparente [VA]":["S","SA","SB","SC"],
    "Frecuencia[Hz]":['F'],
    'Factor de Potencia General':['PF'],
}

PARAMETERS_CHART_ORDER={
    "Voltajes por línea [V]":"V_all_1",
    "Voltajes por fase [V]":"V_all_2",
    "Corrientes por línea [A]":"I_all",
    "Potencia Activa [W]":"P_all",
    "Potencia Reactiva [VAR]":"Q_all",
    "Potencia Aparente [VA]":"S_all",
    "Frecuencia[Hz]":'F',
    'Factor de Potencia General':'PF',
}

TEMPLATE_DIR = "OnDemand/uS/generate_report/static/templates/"

OUTPUT_HTML = "OnDemand/uS/generate_report/result/editable_report.html"

async def get_project_details(project_name:str):
    """
    Entrego nombre del proyecto a buscar en la base de datos
    Retorna todos los datos del cliente, el fae, los modelos de los medidores usados

    Se extrae la lista de circuitos: Llave es id del medidior, Value es nombre del circuito
    """
    
    get_project=await get_project_and_fae(project_name)

    project_details={
        "client_name": get_project['client_name'],
        "project_name": get_project['project_name'],
        "fae": get_project['fae'],
        "meter_models": get_project['meters_models'],
    }

    csv_1st=get_project['csv_1st']
    circuit_names=get_project['circuits']

    #logger.info(f'Contact info and details for the required project {project_details}')
    #logger.info(f'Circuits of the required project: {circuit_names}')

    return project_details, csv_1st , circuit_names

async def get_report_dates(start_date:str,end_date:str,csv_1st:str): 
    """
    start_date & end_date: str en iso que contienen las fechas del reporte
    csv_1:  primera parte del nombre usado para el csv que se envía con el reporte
            la segunda parte es generada con las fechas 
    """
    date_result=await get_dates(start_date,end_date)

    dates={
        "gen_date": date_result['gen_date'],
        "date_range_start": date_result['date_range_start'],
        "date_range_end": date_result['date_range_end'],
        "csv_code":csv_1st+date_result['csv_2nd']
    }
    #logger.info(dates)
    return dates

async def get_values(circuit_list:Dict[str,Any],start_date:str,end_date:str): 
    """
    circuit_list: Diccionario ['meter_id':'nombre del circuito']
    
    Retorno: 2 listas-> 1 tiene todas las mediciones de cada uno de los medidores, cada item es un medidor
                     -> 2 tiene todos los valores extremos y promedio de cada una de las mediciones de la lista 1
    
    """
    measurements_list=[]
    extreme_values_list=[]

    for circuit_index in circuit_list.keys():
        circuit_measure,circuit_extremes= await extract_measures(circuit_index,start_date,end_date)
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
    
async def get_events(circuit_list:Dict[str,Any],start_date:str,end_date:str): 
    
    meter_list=[]

    for circuit_key in circuit_list.keys():
        meter_list.append(circuit_key)

    events_list= await extract_events(meter_list,start_date,end_date)
    
    return events_list

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

async def order_builder(project_part,circuit_list,dates_part,parameters_list,normal_graphs,events_table,events_graphs): #Formar la orden JSON para el renderizador de la plantilla HTML
    
    
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
        "project_info":project_part,
        "circuits_list": circuits_estructure,
        "events":{
            "table_info":events_table,
            "events_images":events_graphs
        }
    }
    
    #logger.info(report_data)
    
    return report_data

async def report_gen(project_name:str,start_date:str,end_date:str): #Ingreso nombre del proyecto y rango de fechas
    #OTENER TODOS LOS DATOS QUE SE NECESITAN DEL REPORTE
    project_part, csv_1st , circuit_dict=await get_project_details(project_name) #DATOS DEL PROYECTO
    if not csv_1st:
        logger.error('Error while getting project details')
        
    dates_part = await get_report_dates(start_date,end_date,csv_1st) #RANGO DE FECHAS Y CODIGO CSV
    if not dates_part:
        logger.error('Error while getting the date range')

    measurements,extreme_values=await get_values(circuit_dict,start_date,end_date) #EXTRAER MEDICIONES PARA EL REPORTE
    if not measurements:
        logger.error('Error while getting the measurements')
    
    parameters_list=await translate_values(extreme_values) #FORMATEAR VALORES EXTREMOS PARA SU USO
    if not parameters_list:
        logger.error('Error while ordering the measurements')
    
    """
    event_list,event_register=await get_events(circuit_dict,start_date,end_date) #EXTRAER EL REGISTRO DE EVENTOS 
    if not event_list:
        logger.error('Error while obtaining the events/alarms register')
    """
    normal_graphs_list=await get_normal_graphs(measurements,start_date,end_date) #GENERAR LAS GRÁFICAS PARA EL REPORTE
    if not normal_graphs_list:
        logger.error('Error while generating the normal charts')
    
    """
    event_graphs=await get_event_graphs(event_register) #GENERAR GRAFICAS ENFOCADAS EN MOSTRAR LOS EVENTOS ANTERIORES
    if not event_graphs:
        logger.error('Error while generating the event charts')
    """
    event_graphs=[]
    event_list=[]

    new_report_order= await order_builder(project_part,circuit_dict,dates_part,parameters_list,normal_graphs_list,event_list,event_graphs)
    if not normal_graphs_list:
        logger.error('Error while generating the report order')

    html_report= await generate_html(TEMPLATE_DIR, OUTPUT_HTML, new_report_order)
    if not html_report:
        logger.error('Error while rendering the html report')
    
    
    return []


async def main(project_name:str,start_date:str,end_date:str):
    
    test_report=await report_gen(project_name,start_date,end_date)

    return test_report


if __name__ == "__main__":  

    try:
        asyncio.run(main('Proyecto_test',"2025-10-01T12:48:00","2025-10-01T17:30:00"))
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt: Shutting down service")


