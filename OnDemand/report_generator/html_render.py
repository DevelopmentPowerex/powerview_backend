from jinja2 import Environment, FileSystemLoader
import asyncio
import logging
logger = logging.getLogger(__name__)


TEMPLATE_DIR = "OnDemand/report_generator/static/templates/"

OUTPUT_HTML = "OnDemand/report_generator/result/editable_report.html"

PRUEBA={
    'report_info': {
        'gen_date': '2026-02-04', 
         'date_range_start': '2026-01-19', 
         'date_range_end': '2026-01-20', 
         'csv': 'electroprotecciones_sas_proyecto_a_1901_2001'
    }, 
    'project_info': {
        'client_name': 'ELECTROPROTECCIONES SAS', 
        'project_name': 'Proyecto A', 
        'fae': {
            'company_name': 'PREMIUMENERGIA SAS', 
            'engineer_name': 'Ing. Jeramhil Javier Solis Yari', 
            'email_addr': 'proyectos@premium-energia.com', 
            'phone': '0984373697'
            }, 
        'meters_list': ['pv-m3']
    }, 
    'circuits_list': [{
        'name': 'Medidor A', 
        'parameters_list': {
            'V_all_1': [{'name': 'vA', 'max': 126.7, 'min': 120.5, 'prom': 124.15}], 
            'V_all_2': [{'name': 'vAB', 'max': 126.7, 'min': 120.5, 'prom': 124.15}, 
                         {'name': 'vCA', 'max': 126.7, 'min': 120.5, 'prom': 124.15}], 
            'Wh_all_p': [{'name': 'P_kWh_A', 'max': 79.6, 'min': 79.6, 'prom': 79.6}, 
                         {'name': 'P_kWh_B', 'max': 825.2, 'min': 825.2, 'prom': 825.2}, 
                         {'name': 'P_kWh_C', 'max': 568.8, 'min': 568.8, 'prom': 568.8}, 
                         {'name': 'P_kWh_T', 'max': 2160.4, 'min': 2160.4, 'prom': 2160.4}], 
            'varh_all_p': [{'name': 'P_kvarh_A', 'max': 4.4, 'min': 4.4, 'prom': 4.4}, 
                           {'name': 'P_kvarh_B', 'max': 2, 'min': 2, 'prom': 2}, 
                           {'name': 'P_kvarh_C', 'max': 2.8, 'min': 2.8, 'prom': 2.8}, 
                           {'name': 'P_kvarh_T', 'max': 27.6, 'min': 27.6, 'prom': 27.6}], 
            'varh_all_r': [{'name': 'R_kvarh_A', 'max': 410.8, 'min': 410.8, 'prom': 410.8}, 
                           {'name': 'R_kvarh_B', 'max': 565.2, 'min': 565.2, 'prom': 565.2}, 
                           {'name': 'R_kvarh_C', 'max': 538.4, 'min': 538.4, 'prom': 538.4}, 
                           {'name': 'R_kvarh_T', 'max': 2012, 'min': 2012, 'prom': 2012}], 
            'F': [{'name': 'F', 'max': 60.01, 'min': 59.93, 'prom': 59.98}], 
            'PF': [{'name': 'PF', 'max': 1, 'min': 1, 'prom': 1}]
            }, 
        'behaviour_images': ['C:\\Users\\jeras\\Documents\\PowerView\\backend_pv\\OnDemand\\report_generator\\temp\\gen_graphs\\meter1_chart_voltage_PN', 
                                 'C:\\Users\\jeras\\Documents\\PowerView\\backend_pv\\OnDemand\\report_generator\\temp\\gen_graphs\\meter1_chart_voltage_PP', 
                                 'C:\\Users\\jeras\\Documents\\PowerView\\backend_pv\\OnDemand\\report_generator\\temp\\gen_graphs\\meter1_chart_current', 
                                 'C:\\Users\\jeras\\Documents\\PowerView\\backend_pv\\OnDemand\\report_generator\\temp\\gen_graphs\\meter1_chart_active_power', 
                                 'C:\\Users\\jeras\\Documents\\PowerView\\backend_pv\\OnDemand\\report_generator\\temp\\gen_graphs\\meter1_chart_reactive_power', 
                                 'C:\\Users\\jeras\\Documents\\PowerView\\backend_pv\\OnDemand\\report_generator\\temp\\gen_graphs\\meter1_chart_aparent_power', 
                                 'C:\\Users\\jeras\\Documents\\PowerView\\backend_pv\\OnDemand\\report_generator\\temp\\gen_graphs\\meter1_chart_active_positive_energy', 
                                 'C:\\Users\\jeras\\Documents\\PowerView\\backend_pv\\OnDemand\\report_generator\\temp\\gen_graphs\\meter1_chart_active_reverse_energy', 
                                 'C:\\Users\\jeras\\Documents\\PowerView\\backend_pv\\OnDemand\\report_generator\\temp\\gen_graphs\\meter1_chart_reactive_positive_energy', 
                                 'C:\\Users\\jeras\\Documents\\PowerView\\backend_pv\\OnDemand\\report_generator\\temp\\gen_graphs\\meter1_chart_reactive_reverse_energy', 
                                 'C:\\Users\\jeras\\Documents\\PowerView\\backend_pv\\OnDemand\\report_generator\\temp\\gen_graphs\\meter1_chart_frequency', 
                                 'C:\\Users\\jeras\\Documents\\PowerView\\backend_pv\\OnDemand\\report_generator\\temp\\gen_graphs\\meter1_chart_power_factor'
                                ]
        }, 
        {
        'name': 'Medidor B', 
        'parameters_list': {
            'V_all_1': [{'name': 'vB', 'max': 123.5, 'min': 0, 'prom': 114.44}], 
            'V_all_2': [{'name': 'vAB', 'max': 123.5, 'min': 0, 'prom': 114.44}, 
                        {'name': 'vBC', 'max': 123.5, 'min': 0, 'prom': 114.44}], 
                        'F': [{'name': 'F', 'max': 60.03, 'min': 0, 'prom': 57.13}], 
                        'PF': [{'name': 'PF', 'max': 1, 'min': 1, 'prom': 1}]}, 
        'behaviour_images': ['\\OnDemand\\report_generator\\temp\\gen_graphs\\meter2_chart_voltage_PN.png', 
                             '\\OnDemand\\report_generator\\temp\\gen_graphs\\meter2_chart_voltage_PP.png', 
                             '\\OnDemand\\report_generator\\temp\\gen_graphs\\meter2_chart_current.png', 
                             '\\OnDemand\\report_generator\\temp\\gen_graphs\\meter2_chart_active_power.png', 
                             '\\OnDemand\\report_generator\\temp\\gen_graphs\\meter2_chart_reactive_power.png', 
                             '\\OnDemand\\report_generator\\temp\\gen_graphs\\meter2_chart_aparent_power.png', 
                             '\\OnDemand\\report_generator\\temp\\gen_graphs\\meter2_chart_active_positive_energy.png', 
                             '\\OnDemand\\report_generator\\temp\\gen_graphs\\meter2_chart_active_reverse_energy.png', 
                             '\\OnDemand\\report_generator\\temp\\gen_graphs\\meter2_chart_reactive_positive_energy.png', 
                             '\\OnDemand\\report_generator\\temp\\gen_graphs\\meter2_chart_reactive_reverse_energy.png', 
                             '\\OnDemand\\report_generator\\temp\\gen_graphs\\meter2_chart_frequency.png', 
                             '\\OnDemand\\report_generator\\temp\\gen_graphs\\meter2_chart_power_factor.png']
    }], 
    'events': [{
        'circuit': 'Medidor B', 'context': 'Salida de UPS en cero', 'rule': 'vB=0.0', 'level': 'MID', 'first_event': '2026-01-19T23:16:36', 'last_event': '2026-01-19T23:16:36', 'event_counter': 1
    }]
}
async def generate_html_report(template_path, output_path, data):
    try:
        env = Environment(loader=FileSystemLoader(template_path))
        
        template = env.get_template("report_template.html")
        
        html_output = template.render(**data)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_output)
        
        return html_output
        
    except Exception:
        logger.exception(f"Error rendering the report html")
        return False

async def main():
    await generate_html_report(TEMPLATE_DIR, OUTPUT_HTML,PRUEBA)

if __name__=="__main__":
    asyncio.run(main())
