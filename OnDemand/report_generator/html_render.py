from jinja2 import Environment, FileSystemLoader

import logging
logger = logging.getLogger(__name__)

TEMPLATE_DIR = "uS/generate_report/static/templates/"
OUTPUT_HTML = "uS/generate_report/result/editable_report.html"

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