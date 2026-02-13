import pandas as pd

from datetime import datetime

from typing import Optional, Any, Dict, List

from matplotlib.ticker import MaxNLocator, FixedLocator
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

plt.style.use('seaborn-v0_8-whitegrid')

from ..protocols.auxiliar_info import PARAMETERS_FOR_REPORT, PREMADE_ORDERS, TEMP_GEN_GRAPHS_PATH

import logging
logger = logging.getLogger(__name__)

async def chart_order(charts_data:List[Dict[str,Any]])->Optional[str]:
    separator='_'
    circuits_n_charts={}
    for circuit in charts_data:
        generated_chart_list=[]
        for chart_name in (circuit['graphs']).keys():
            parameters_to_plot=PREMADE_ORDERS[chart_name][0]
            
            #for parameter in parameters_to_plot:
            logger.debug(parameters_to_plot)
            
            graph_title=PARAMETERS_FOR_REPORT[chart_name][1] if chart_name in PREMADE_ORDERS.keys() else separator.join(chart_name)
            logger.debug(graph_title)

            file_code=f'\meter{circuit["meter_id"]}_{PREMADE_ORDERS[chart_name][1]}' if chart_name in PREMADE_ORDERS.keys() else f'\meter{(circuit["meter_id"])}chart_{separator.join(chart_name)}'
            logger.debug(file_code)
            filename= TEMP_GEN_GRAPHS_PATH+file_code
            logger.debug(filename)
            
            order_file=filename+'.png'
            logger.debug(order_file)

            generated_chart=await create_line_chart(circuit["graphs"][chart_name], parameters_to_plot, filename, order_file,graph_title)
            
            if not generated_chart:
                logger.error(f"Error generating charts for order {chart_name}")
                continue
            
            generated_chart_list.append({"name":graph_title,"image":generated_chart})
        circuits_n_charts[circuit["meter_id"]]=generated_chart_list

    return circuits_n_charts if circuits_n_charts else None 
    
async def create_line_chart(measurement_list:List[Dict[str,Any]], parameters_order:List[str], filename:str,order_file:str,graph_title:str)->Optional[str]:
    fig, ax = plt.subplots(figsize=(10, 4))

    line_colors = ["#0b4b79", '#ff7f0e', "#39a02c", '#d62728', '#9467bd', 
                    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    
    try:

        timestamps = [measurement['point'] for measurement in measurement_list]
        dates = [datetime.fromisoformat(ts) for ts in timestamps]
    
        unique_dates = sorted(set(dates))

        day_ranges = {}
        for d in unique_dates:
            key = d.date()
            if key not in day_ranges:
                day_ranges[key] = [d, d]
            else:
                if d < day_ranges[key][0]:
                    day_ranges[key][0] = d
                if d > day_ranges[key][1]:
                    day_ranges[key][1] = d
                    
        midpoints = [start + (end-start)/2 for start, end in day_ranges.values()]


        for i, parameter in enumerate(parameters_order):
            # Extraer timestamps y valores
            
            values = [measurement[parameter] for measurement in measurement_list]
            
            # Convertir a Series y suavizar
            values_series = pd.Series(values, index=dates)
            values_filled = values_series.interpolate(method='time')  # Rellenar con NaN para saltos vacíos

            # Graficar línea suavizada
            line_color = line_colors[i % len(line_colors)]
            ax.plot(dates, values_series, color=line_color, linewidth=1.5, label=PARAMETERS_FOR_REPORT[parameter][2], alpha=0.8)

            # Máximo y mínimo
            max_idx = values_filled.idxmax()
            min_idx = values_filled.idxmin()
            max_val = values_filled[max_idx]
            min_val = values_filled[min_idx]

            if max_val != min_val:
                # Destacar max y mínimos del parametro graficado
                ax.scatter([max_idx], [max_val], color=line_color, s=100, 
                        marker='x', zorder=5, edgecolors='black', linewidth=1)
                ax.scatter([min_idx], [min_val], color=line_color, s=100, 
                        marker='v', zorder=5, edgecolors='black', linewidth=1)

        # Eje principal en X, marcas de hora
        ax.xaxis.set_major_locator(MaxNLocator(nbins=7))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        plt.setp(ax.get_xticklabels(), rotation=0, ha="center")

        if len(day_ranges)>1:
            ax2 = ax.secondary_xaxis('bottom')
            ax2.xaxis.set_major_locator(FixedLocator([mdates.date2num(d) for d in midpoints]))
            ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
            ax2.spines['bottom'].set_position(('outward', 40))
            ax2.tick_params(axis='x', which='major', labelsize=10)

        # Insertar unidades del parametro y título de la gráfica
        ax.set_title(graph_title, fontsize=14, fontweight='bold', pad=20)
        ax.set_ylabel(PARAMETERS_FOR_REPORT[parameter][0], fontsize=12, fontweight='bold')

        # Etiqueta de color vs parametro
        if len(parameters_order)>1: #Si hay mas de un solo parametro no se coloca etiqueta o título
            ax.legend(loc='upper left', bbox_to_anchor=(1, 0.5), ncol=1, fontsize=10, frameon=True)
        
        # Grid para mejor lectura de la gráfica
        ax.grid(True, which='both', color='lightgray', linestyle='--', linewidth=0.7, alpha=0.7)

        plt.tight_layout()
        #plt.show()

        fig.savefig(filename, dpi=150, bbox_inches='tight',transparent=True)
        
        plt.close(fig)

        return order_file if fig else None
    
    except Exception:
        logger.exception("Error generating report charts")
        return None
