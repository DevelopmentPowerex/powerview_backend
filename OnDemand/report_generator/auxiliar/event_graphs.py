import pandas as pd

from datetime import datetime

from typing import Optional, Any, Dict, List

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

plt.style.use('seaborn-v0_8-whitegrid')

from ..protocols.auxiliar_info import PARAMETERS_FOR_EVENT_GRAPHS,TEMP_GEN_GRAPHS_PATH,PARAMETER_TRANSLATION

import logging
logger = logging.getLogger(__name__)

async def event_chart_order(events_list:List[Dict[str,Any]],measurements:List[Dict[str,Any]])->Optional[str]:

    events_charts=[]
    for i,event in enumerate(events_list):
        
        file_code=f'\event{i+1}_meter{event["meter_id"]}_{event["context"]}'
        filename= TEMP_GEN_GRAPHS_PATH+file_code
        
        order_file=filename+'.png'

        graph_title=PARAMETERS_FOR_EVENT_GRAPHS[event['parameter']]
        graph_label=PARAMETER_TRANSLATION[event['parameter']][0]

        generated_chart=await create_line_chart(graph_title, 
                                                graph_label,
                                                measurements[i][event["parameter"]],
                                                event['1st_ts'],
                                                event['last_ts'],
                                                filename, 
                                                order_file)
        
        if not generated_chart:
            logger.error(f"Error generating chart for {event['context']}")
            continue
        
        events_charts.append(generated_chart)

    return events_charts if events_charts else None 
    
async def create_line_chart(graph_title:str,graph_label:str,measurements:Dict[str,Any], first_mark:str,last_mark:str,filename:str,order_file:str)->Optional[str]:
    
    fig, ax = plt.subplots(figsize=(8, 4))

    line_colors = ["#0b4b79", '#ff7f0e', "#39a02c", '#d62728', '#9467bd', 
                    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    
    try:
        
        timestamps , values =zip(*measurements.items())
        dates = [datetime.fromisoformat(ts) for ts in timestamps]

        values_series = pd.Series(values, index=dates)
        values_filled = values_series.interpolate(method='time') 

        first_dt=datetime.fromisoformat(first_mark)
        last_dt=datetime.fromisoformat(last_mark)

        y_first = values_series[first_dt]
        y_last = values_series[last_dt]

        ymin, ymax = ax.get_ylim()

        ax.plot(dates, values_series, color='#d62728', linewidth=1.5, label=graph_label, alpha=0.8)

        ax.set_xticks([first_mark, last_mark])
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d\n%H:%M:%S'))

        plt.setp(ax.get_xticklabels(), rotation=0, ha="center")

        # Insertar unidades del parametro y título de la gráfica
        ax.set_title(graph_title, fontsize=12, fontweight='bold', pad=20)
        ax.set_ylabel(graph_label, fontsize=8, fontweight='bold')

        # Grid para mejor lectura de la gráfica
        ax.vlines(first_dt, ymin=ymin, ymax=y_first, color='blue', linestyle='--', linewidth=1)
        ax.vlines(last_dt, ymin=ymin, ymax=y_last, color='blue', linestyle='--', linewidth=1)

        ax.scatter(first_dt, y_first, marker="x", color='blue', s=40, zorder=5)
        ax.scatter(last_dt, y_last, marker="x", color='blue', s=40, zorder=5)

        ax.grid(True, which='both', color='lightgray', linestyle='--', linewidth=0.7, alpha=0.7)

        plt.tight_layout()
        #plt.show()

        fig.savefig(filename, dpi=150, bbox_inches='tight',transparent=False)
        
        plt.close(fig)

        return order_file if fig else None
    
    except Exception:
        logger.exception("Error generating report charts")
        return None