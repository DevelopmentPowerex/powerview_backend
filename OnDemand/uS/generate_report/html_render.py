from jinja2 import Environment, FileSystemLoader
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('report_render') 

TEMPLATE_DIR = "uS/generate_report/static/templates/"
OUTPUT_HTML = "uS/generate_report/result/editable_report.html"

report_data = {'report_info': {'gen_date': '2025-09-18', 'date_range_start': '2025-08-17', 'date_range_end': '2025-08-25', 'csv_code': 'indu_1708_2508'}, 'project_info': {'client_name': 'INDURAMA ECUADOR S.A.', 'project_name': 'Laboratorios RI', 'fae': {'company_name': 'PREMIUMENERGIA SAS', 'engineer_name': 'Ing. Jeramhil Javier Solis Yari', 'email_addr': 'proyectos@premium-energia.com', 'phone': '0984373697'}, 'meters_list': ['PV-M3', 'PV-4M']}, 'circuits_list': [{'name': 'Alimentación Laboratorio 7', 'parameters_list': [{'name': 'Voltajes por línea [V]', 'param_values': [{'name': 'vA', 'max': 125.6, 'min': 112.9, 'prom': 120.82}, {'name': 'vB', 'max': 131.7, 'min': 113.5, 'prom': 121.87}, {'name': 'vC', 'max': 133.6, 'min': 118.7, 'prom': 128.39}]}, {'name': 'Voltajes por fase [V]', 'param_values': [{'name': 'vAB', 'max': 221, 'min': 202.2, 'prom': 210.13}, {'name': 'vBC', 'max': 226.5, 'min': 208.4, 'prom': 216.72}, {'name': 'vCA', 'max': 223.2, 'min': 208, 'prom': 215.81}]}, {'name': 'Corrientes por línea [A]', 'param_values': [{'name': 'iA', 'max': 5.79, 'min': 0, 'prom': 4.76}, {'name': 'iB', 'max': 27.43, 'min': 2.67, 'prom': 12.69}, {'name': 'iC', 'max': 14.72, 'min': 4.47, 'prom': 6.68}]}, {'name': 'Potencia Activa [W]', 'param_values': [{'name': 'P', 'max': 4.96, 'min': 0.72, 'prom': 1.99}, {'name': 'PA', 'max': 0.32, 'min': 0, 'prom': 0.22}, {'name': 'PB', 'max': 3.12, 'min': 0.28, 'prom': 1.34}, {'name': 'PC', 'max': 1.64, 'min': 0.2, 'prom': 0.41}]}, {'name': 'Potencia Reactiva [VAR]', 'param_values': [{'name': 'Q', 'max': 0.4, 'min': -1.76, 'prom': -1.43}, {'name': 'QA', 'max': 0, 'min': -0.52, 'prom': -0.42}, {'name': 'QB', 'max': 0.28, 'min': -0.68, 'prom': -0.51}, {'name': 'QC', 'max': 0.48, 'min': -0.64, 'prom': -0.48}]}, {'name': 'Potencia Aparente [VA]', 'param_values': [{'name': 'S', 'max': 4.96, 'min': 0.8, 'prom': 2.54}, {'name': 'SA', 'max': 0.6, 'min': 0, 'prom': 0.49}, {'name': 'SB', 'max': 3.12, 'min': 0.28, 'prom': 1.48}, {'name': 'SC', 'max': 1.72, 'min': 0.44, 'prom': 0.72}]}, {'name': 'Frecuencia[Hz]', 'param_values': [{'name': 'F', 'max': 60.05, 'min': 59.91, 'prom': 59.98}]}, {'name': 'Factor de Potencia General', 'param_values': [{'name': 'PF', 'max': 0.999, 'min': 0.449, 'prom': 0.78}]}], 'behaviour_images': [{'name': 'Voltajes por línea [V]', 'image': '/OD_service/uS/generate_report/temp/gen_graphs\\chart_voltage_PN.png'}, {'name': 'Voltajes por fase [V]', 'image': '/OD_service/uS/generate_report/temp/gen_graphs\\chart_voltage_PP.png'}, {'name': 'Corrientes por línea [A]', 'image': '/OD_service/uS/generate_report/temp/gen_graphs\\chart_current.png'}, {'name': 'Potencia Activa [W]', 'image': '/OD_service/uS/generate_report/temp/gen_graphs\\chart_active_power.png'}, {'name': 'Potencia Reactiva [VAR]', 'image': '/OD_service/uS/generate_report/temp/gen_graphs\\chart_reactive_power.png'}, {'name': 'Potencia Aparente [VA]', 'image': '/OD_service/uS/generate_report/temp/gen_graphs\\chart_aparent_power.png'}, {'name': 'Frecuencia[Hz]', 'image': '/OD_service/uS/generate_report/temp/gen_graphs\\chart_frequency.png'}, {'name': 'Factor de Potencia General', 'image': '/OD_service/uS/generate_report/temp/gen_graphs\\chart_power_factor.png'}]}], 'events': {'table_info': [], 'events_images': []}}

async def generate_html_report(template_path, output_path, data):
    try:
        env = Environment(loader=FileSystemLoader(template_path))
        
        template = env.get_template("report_template.html")
        
        html_output = template.render(**data)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_output)
        
        #logger.info(f"HTML report generated succesfully on: {html_output}")
        return html_output
        
    except Exception as e:
        logger.error(f"Error: {e}")
        return False

if __name__ == "__main__":

    # Generar el reporte HTML
    """
    
    success = await generate_html_report(TEMPLATE_DIR, OUTPUT_HTML, report_data)
    
    if success:
        print("Proceso completado exitosamente!")
    else:
        print("Error en la generación del reporte")
        
        """