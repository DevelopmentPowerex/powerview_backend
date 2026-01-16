from email.mime.image import MIMEImage
from typing import Dict,Any

from ..protocols.pvm3 import M3_MAPPING, PARAMETER_TRANSLATION

import logging
from ..config import settings

logger = logging.getLogger(__name__)

async def attach_image_to_email(email_message, filename, content_id)->MIMEImage:

    with open(filename, "rb") as f:
        img = MIMEImage(f.read())
        img.add_header('Content-ID', f'<{content_id}>')
        img.add_header('Content-Disposition', 'inline', filename=filename)

    return img

async def email_builder(email_data:Dict[str,Any],counter_notif:int)->str:
    try:
        case_inf=email_data['event_data']

        alarm_ts=(case_inf['ts']).replace('T',' ')
        alarm_param=M3_MAPPING[case_inf['parameter']]
        alarm_comparator=case_inf['comparator']
        alarm_threshold=case_inf['threshold']
        alarm_read=case_inf['reading']
        alarm_comment=case_inf['comment']
        
        alarm_html = f"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>POWERVIEW ALARM NOTIFICATION (PV_m3 type)</title>
            <style type="text/css">
                body, table, td {{-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%;}}
            </style>
            <!--[if gte mso 9]>
            <style type="text/css">
                .outlook-fix {{width: 600px;}}
            </style>
            <xml>
                <o:OfficeDocumentSettings>
                    <o:AllowPNG/>
                    <o:PixelsPerInch>96</o:PixelsPerInch>
                </o:OfficeDocumentSettings>
            </xml>
            <![endif]-->
        </head>
        <body style="margin:0;padding:0;background-color:#1e1e1e;" bgcolor="#1e1e1e">
        
        <!--[if (gte mso 9)|(IE)]>
        <table width="600" align="center" cellpadding="0" cellspacing="0" border="0" bgcolor="#1e1e1e">
        <tr>
        <td>
        <![endif]-->
        
        <table class="outlook-fix" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" style="max-width:600px;background-color:#1e1e1e;" bgcolor="#1e1e1e">
            <!-- Header -->
            <tr>
                <td align="center" valign="top">
                    <!--[if (gte mso 9)|(IE)]>
                    <img src="cid:Alarm_header" alt="" width="600" style="width:600px;">
                    <![endif]-->
                    <!--[if !(gte mso 9)|!(IE)]><!-->
                    <img src="cid:Alarm_header" alt="" width="600" style="width:100%;max-width:600px;height:auto;display:block;">
                    <!--<![endif]-->
                </td>
            </tr>
            
            <!-- Contenido -->
            <tr>
                <td align="center" valign="top" style="padding:20px;color:#ffffff;font-family:Arial,sans-serif;font-size:14px;line-height:1.4;" bgcolor="#1e1e1e">
                    <table width="100%" border="0" cellpadding="0" cellspacing="0">
                        <tr>
                            <td align="center" style="padding-bottom:20px;">
                                <img src="cid:Alarm_level" alt="Alarm_level" width="200" style="max-width:200px;width:100%;height:auto;display:block;margin:0 auto;">
                            </td>
                        </tr>
                        <tr>
                            <td align="left" style="padding-bottom:10px;color:#ffffff;">
                                <strong>{alarm_comment}</strong>
                            </td>
                        </tr>
                        <tr>
                            <td align="left" style="padding-bottom:10px;color:#ffffff;">
                                <strong>Parámetro:</strong> {PARAMETER_TRANSLATION[alarm_param][1]}
                            </td>
                        </tr>
                        <tr>
                            <td align="left" style="padding-bottom:10px;color:#ffffff;">
                                <strong>Valor leído:</strong> {alarm_read} {PARAMETER_TRANSLATION[alarm_param][0]}
                            </td>
                        </tr>
                        <tr>
                            <td align="left" style="padding-bottom:10px;color:#ffffff;">
                                <strong>Alarmar cuando:</strong> {alarm_param} {alarm_comparator} {alarm_threshold} {PARAMETER_TRANSLATION[alarm_param][0]}
                            </td>
                        </tr>
                        <tr>
                            <td align="left" style="padding-bottom:10px;color:#ffffff;">
                                <strong>Fecha y hora:</strong> {alarm_ts}
                            </td>
                        </tr>
                        <tr>
                            <td align="left" style="padding-bottom:0;color:#ffffff;">
                                <strong>Cantidad de incidencias:</strong> {counter_notif}
                            </td>
                        </tr>

                    </table>
                </td>
            </tr>
            
            <!-- Footer -->
            <tr>
                <td align="center" valign="top">
                    <!--[if (gte mso 9)|(IE)]>
                    <img src="cid:Alarm_footer" alt="" width="600" style="width:600px;">
                    <![endif]-->
                    <!--[if !(gte mso 9)|!(IE)]><!-->
                    <img src="cid:Alarm_footer" alt="" width="600" style="width:100%;max-width:600px;height:auto;display:block;">
                    <!--<![endif]-->
                </td>
            </tr>
        </table>
        
        <!--[if (gte mso 9)|(IE)]>
        </td>
        </tr>
        </table>
        <![endif]-->
        
        </body>
        </html>"""
        
        return alarm_html
    
    except Exception as e:
        logger.error(f'Something went wrong while building the html:{e}')
        return None
    




