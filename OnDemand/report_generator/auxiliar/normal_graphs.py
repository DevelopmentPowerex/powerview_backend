import asyncio
from datetime import datetime
from typing import Optional, Any, Dict, List
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator, FixedLocator
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

# Configurar un estilo más profesional
plt.style.use('seaborn-v0_8-whitegrid')

from ..protocols.auxiliar_info import PARAMETERS_FOR_REPORT, PREMADE_ORDERS, DATOS_PRUEBA

from ..config import settings

import logging
logger = logging.getLogger(__name__)

async def chart_order(graph_order:tuple,measurements_data=List[Dict[str,Any]])->Optional[str]:

    """
    graph_order: Str de nombre de la receta del gráfico. Ejm: 'V_all_1' grafica 'vA','vB','vC'
    
    """    
    separator='_'
    parameters_to_plot=PREMADE_ORDERS[graph_order[0]][0] if graph_order[0] in PREMADE_ORDERS.keys() else graph_order
    data_dict = {}
    for param in parameters_to_plot:
        
        ts_values = [
            {
                'timestamp': datetime.fromisoformat(measure['timestamp']).isoformat(), 
                'parameters': {param: measure['parameters'][param]}
            } for measure in measurements_data
            ]
        
        data_dict[param] = ts_values

    file_code=f'\{PREMADE_ORDERS[graph_order[0]][1]}' if graph_order[0] in PREMADE_ORDERS.keys() else f'chart_{separator.join(graph_order)}'
    
    graph_title=PARAMETERS_FOR_REPORT[graph_order[0]][1] if graph_order[0] in PREMADE_ORDERS.keys() else separator.join(graph_order)
    
    filename= settings.temp_graphs_path+file_code+'_meter'+section_id
    order_file=settings.graph_path+file_code+'_meter'+section_id+'.png'

    generated_chart=await create_line_chart(data_dict, parameters_to_plot, filename, graph_title)

    return order_file
    
async def create_line_chart(measurement_list:List[Dict[str,Any]], parameters_order:List[str], filename:str, graph_title:str,smooth_window=5):
    fig, ax = plt.subplots(figsize=(10, 4))

    line_colors = ["#0b4b79", '#ff7f0e', "#39a02c", '#d62728', '#9467bd', 
                    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

    for i, parameter in enumerate(parameters_order):
        # Extraer timestamps y valores
        timestamps = [measurement['timestamp'] for measurement in measurement_list[parameter]]
        values = [measurement['parameters'][parameter] for measurement in measurement_list[parameter]]
        dates = [datetime.fromisoformat(ts) for ts in timestamps]

        # Convertir a Series y suavizar
        values_series = pd.Series(values, index=dates)
        values_filled = values_series.interpolate(method='time')  # Rellenar con NaN para saltos vacíos

        # Graficar línea suavizada
        line_color = line_colors[i % len(line_colors)]
        ax.plot(dates, values_series, color=line_color, linewidth=1.5, label=parameter, alpha=0.8)

        # Máximo y mínimo
        max_idx = values_filled.idxmax()
        min_idx = values_filled.idxmin()
        max_val = values_filled[max_idx]
        min_val = values_filled[min_idx]

        # Destacar max y mínimos del parametro graficado
        ax.scatter([max_idx], [max_val], color=line_color, s=100, 
                  marker='^', zorder=5, edgecolors='black', linewidth=1)
        ax.scatter([min_idx], [min_val], color=line_color, s=100, 
                  marker='v', zorder=5, edgecolors='black', linewidth=1)

        # Etiquetas de valores máx y min
        ax.annotate(f"Máx: {max_val:.2f}",
                    xy=(max_idx, max_val),
                    xytext=(0, 15), textcoords='offset points',
                    ha='center', va='bottom',
                    fontsize=9, fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=line_color, alpha=0.8),
                    arrowprops=dict(arrowstyle='->', lw=1.5, color=line_color))

        ax.annotate(f"Mín: {min_val:.2f}",
                    xy=(min_idx, min_val),
                    xytext=(0, -25), textcoords='offset points',
                    ha='center', va='top',
                    fontsize=9, fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=line_color, alpha=0.8),
                    arrowprops=dict(arrowstyle='->', lw=1.5, color=line_color))

    # Eje principal en X, marcas de hora
    ax.xaxis.set_major_locator(MaxNLocator(nbins=7))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    plt.setp(ax.get_xticklabels(), rotation=0, ha="center")

    # Eje secundario en X, marcas del día
    all_dates = sorted(set(d for parameter in parameters_order for d in 
                        [datetime.fromisoformat(ts) for ts in [item['timestamp'] for item in measurement_list[parameter]]]))
    
    day_ranges = {}
    for d in all_dates:
        key = d.date()
        if key not in day_ranges:
            day_ranges[key] = [d, d]
        else:
            if d < day_ranges[key][0]:
                day_ranges[key][0] = d
            if d > day_ranges[key][1]:
                day_ranges[key][1] = d
    midpoints = [start + (end-start)/2 for start, end in day_ranges.values()]

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

    fig.savefig(filename, dpi=300, bbox_inches='tight',transparent=True)
    
    # Mostrar gráfica
    #plt.show()
    
    return fig

async def main():
    await chart_order(['V_all_1'],DATOS_PRUEBA)

if __name__ == "__main__":  
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.exception("KeyboardInterrupt: Shutting down service")