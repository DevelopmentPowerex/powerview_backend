from typing import Optional,Dict,Any

from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from OnDemand.report_generator.protocols.auxiliar_info import STATIC_FOLDER,HTML_TEMPLATES_PATH,HTML_REPORT_PARTS_TEMPLATES,HTML_REPORT_PARTS_RESULT

import logging
logger = logging.getLogger(__name__)

STATIC_ROOT = Path(STATIC_FOLDER).resolve()

async def file_uri(rel_path: str) -> str:
    return (STATIC_ROOT / rel_path).resolve().as_uri()

async def inject_graph_uris_inplace(report_data: Dict[str,Any]) -> Dict[str,Any]:

    for circuit in report_data.get("circuits_list", []):
        for graph in circuit.get("behaviour_images", []):
            img = graph.get("image")
            graph["image_uri"] = Path(img).resolve().as_uri()
            
    return report_data

async def generate_html_report(report_data: Dict[str,Any])->Optional[Dict[str,Any]]:
    try:
        env = Environment(loader=FileSystemLoader(HTML_TEMPLATES_PATH))

        await inject_graph_uris_inplace(report_data)

        report_data.setdefault("assets", {})
        report_data["assets"].update({
            "logo_powerview": await file_uri("img/logo_powerview.png"),
            "loguito": await file_uri("img/loguito.png"),
        })

        for part_key, template_name in HTML_REPORT_PARTS_TEMPLATES.items():
            template = env.get_template(template_name)
            html_output = template.render(**report_data)

            output_path = HTML_REPORT_PARTS_RESULT[part_key]
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_output)

        return HTML_REPORT_PARTS_RESULT

    except Exception:
        logger.exception("Error rendering the report html")
        return None
