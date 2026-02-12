from pathlib import Path
from pypdf import PdfReader, PdfWriter
from playwright.async_api import async_playwright
import copy
from typing import Optional,Dict,Any

from OnDemand.report_generator.protocols.auxiliar_info import PDF_RESULT_PATHS

import logging
logger = logging.getLogger(__name__)

async def merge_cover_with_content(cover_pdf:str,content_pdf:str,final_pdf_path: str)->str:
    
    cover_reader = PdfReader(cover_pdf)
    body_reader = PdfReader(content_pdf)
    writer = PdfWriter()

    for page in cover_reader.pages:
        writer.add_page(page)

    for page in body_reader.pages:
        writer.add_page(page)

    with open(final_pdf_path, "wb") as f:
        writer.write(f)

    return final_pdf_path


async def merge_format_with_content(format_pdf_path: str,content_pdf_path: str,output_pdf_path: str)->str:
    
    format_reader = PdfReader(format_pdf_path)
    content_reader = PdfReader(content_pdf_path)


    format_page = format_reader.pages[0]
    
    writer = PdfWriter()

    for content_page in content_reader.pages:

        page = copy.deepcopy(content_page)
        page.merge_page(format_page,over=False)

        writer.add_page(page)

    with open(output_pdf_path, "wb") as f:
        writer.write(f)

    return output_pdf_path

async def first_render(html_path: str, pdf_path: str):
    html_path = Path(html_path).resolve()
    pdf_path = Path(pdf_path).resolve()

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Carga el HTML renderizado (Jinja ya aplicado)
        await page.goto(html_path.as_uri(), wait_until="networkidle")

        # Fuerza estilos @media print (tu CSS de print)
        await page.emulate_media(media="print")

        # Espera extra corta por si Tailwind termina de inyectar CSS
        await page.wait_for_timeout(200)  # ms

        await page.pdf(
            path=str(pdf_path),
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )

        await browser.close()

async def render_to_pdf(html_dict:Dict[str,Any])->Optional[str]:

    try:
        for part in html_dict.keys():
            await first_render(html_dict.get(part),PDF_RESULT_PATHS.get(part))

        full_content_pdf=await merge_format_with_content(PDF_RESULT_PATHS.get('format'),
                                                         PDF_RESULT_PATHS.get('content'),
                                                         PDF_RESULT_PATHS.get('full_content'))
        
        if not full_content_pdf:
            return None
        
        final_pdf=await merge_cover_with_content(PDF_RESULT_PATHS.get('cover'),
                                                 full_content_pdf,
                                                 PDF_RESULT_PATHS.get('final'))

        return final_pdf if final_pdf else None

    except Exception:
        logger.exception("Error creating the final pdf report")
        return None
    

        

    
        


