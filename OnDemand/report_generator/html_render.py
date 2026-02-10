from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import logging

logger = logging.getLogger(__name__)

templates_path = r"OnDemand\report_generator\static\templates"
STATIC_ROOT = Path(r"OnDemand\report_generator\static").resolve()

templates = {
    "cover": "cover_template.html",
    "format": "format_template.html",
    "content": "content_template.html",
}

results = {
    "cover": r"OnDemand\report_generator\result\cover_result.html",
    "format": r"OnDemand\report_generator\result\format_result.html",
    "content": r"OnDemand\report_generator\result\content_result.html",
}

def file_uri(rel_path: str) -> str:
    return (STATIC_ROOT / rel_path).resolve().as_uri()

def inject_graph_uris_inplace(report_data: dict) -> dict:

    for circuit in report_data.get("circuits_list", []):
        for graph in circuit.get("behaviour_images", []):
            img = graph.get("image")
            if img:  # evita None o ""
                graph["image_uri"] = Path(img).resolve().as_uri()
    return report_data

async def generate_html_report(report_data: dict):
    try:
        env = Environment(loader=FileSystemLoader(templates_path))

        inject_graph_uris_inplace(report_data)

        report_data.setdefault("assets", {})
        report_data["assets"].update({
            "logo_powerview": file_uri("img/logo_powerview.png"),
            "loguito": file_uri("img/loguito.png"),
        })

        for part_key, template_name in templates.items():
            template = env.get_template(template_name)
            html_output = template.render(**report_data)

            output_path = results[part_key]
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_output)

        return results

    except Exception:
        logger.exception("Error rendering the report html")
        return None
