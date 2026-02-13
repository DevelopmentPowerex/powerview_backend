from typing import Any,Dict,List,Optional
from datetime import datetime, timedelta
from OnDemand.report_generator.auxiliar.event_graphs import event_chart_order as create_charts

import logging
logger = logging.getLogger(__name__)

async def clean_chart_data(events:List[Dict[str,Any]],measurements:List[Dict[str,Any]])->Optional[List[Dict[str,Any]]]:
    try:
        
        graphs_list=[]
        for event in events:
            event_data={}
            parameter_points={}

            timestamp_1st = datetime.fromisoformat(event['1st_ts'])
            timestamp_last = datetime.fromisoformat(event['last_ts'])

            timestamp_minus_5 = timestamp_1st - timedelta(minutes=5)
            timestamp_plus_5 = timestamp_last + timedelta(minutes=5)

            timestamp_minus_5_str = timestamp_minus_5.isoformat()
            timestamp_plus_5_str = timestamp_plus_5.isoformat()

            for measurement in measurements:
                
                if (event['meter_id']==measurement['id']) and (measurement['timestamp']>=timestamp_minus_5_str) and (measurement['timestamp']<=timestamp_plus_5_str): 
                    parameter=event['parameter']
                    parameter_points[measurement['timestamp']]=measurement['reading'][parameter]
            
            event_data[event['parameter']]=parameter_points
                               
            graphs_list.append(event_data)
        return graphs_list
    
    except Exception:
        logger.exception("Error preparing the data for chart generation")
        return None

async def generate_event_charts(events_list:List[Dict[str,Any]],measurements:List[Dict[str,Any]])->Optional[Dict[str,Any]]: 

    clean_data=await clean_chart_data(events_list,measurements)
    if not clean_data:
        logger.error("Error preparing the measurements for chart generation")
        return None

    event_charts=await create_charts(events_list,clean_data)
    if not event_charts:
        logger.error("Error generating the event charts")
        return None
    return event_charts
    