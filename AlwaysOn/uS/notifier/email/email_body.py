from email.mime.image import MIMEImage

import logging
from typing import Dict,Any

PARAMETER_TRANSLATION={

    "vA":('V','Voltaje entre Fase A  y Neutro [vA]'),
    "vB":('V','Voltaje entre Fase B  y Neutro [vB]'),
    "vC":('V','Voltaje entre Fase C  y Neutro [vC]'),
    "vAB":('V','Voltaje entre Fases  A y B [vAB]'),
    "vBC":('V','Voltaje entre Fases  B y C [vBC]'),
    "vCA":('V','Voltaje entre Fases  C y A [vCA]'),
    "iA":('A','Corriente en Fase A [iA]'),
    "iB":('A','Corriente en Fase B [iB]'),
    "iC":('A','Corriente en Fase C [iC]'), 
    "PA":('W','Potencia Activa en Fase A [PA]'),
    "PB":('W','Potencia Activa en Fase B [PB]'), 
    "PC":('W','Potencia Activa en Fase C [PC]'),
    "P":('W','Potencia Activa Total [P]'),
    "QA":('VAR','Potencia Reactiva en Fase A [QA]'), 
    "QB":('VAR','Potencia Reactiva en Fase B [QB]'),
    "QC":('VAR','Potencia Reactiva en Fase C [QC]'),
    "Q":('VAR','Potencia Reactiva Total [Q]'),
    "SA":('VA','Potencia Aparente en Fase A [SA]'),
    "SB":('VA','Potencia Aparente en Fase B [SB]'), 
    "SC":('VA','Potencia Aparente en Fase C [SC]'), 
    "S" :('VA','Potencia Aparente Total [S]'),
    "PFA":('','Factor de Potencia en Fase A [PFA]'),
    "PFB":('','Factor de Potencia en Fase B [PFB]'),
    "PFC":('','Factor de Potencia en Fase C [PFC]'),
    "PF":('','Factor de Potencia General [PF]'),
    "F":('Hz','Frecuencia [F]'), 
    "TA":('°C','Temperatura en Fase A [TA]'),
    "TB":('°C','Temperatura en Fase B [TB]'), 
    "TC":('°C','Temperatura en Fase C [TC]'), 
    "TN":('°C','Temperatura en Neutro [N]'),
    "iF":('A','Corriente de Fuga [iF]'),
    "V_unb":('%','Porcentaje de Desbalance de Voltaje'),
    "I_unb":('%','Porcentaje de Desbalance de Corriente'),
    "P_kWh_T":('kWh','Energía Activa Positiva Total') ,
    "R_kWh_T":('kWh','Energía Activa Inversa Total'),
    "P_kvarh_T":('kVarh','Energía Reactiva Positiva Total'),
    "R_kvarh_T":('kVarh','Energía Reactiva Inversa Total'),
    "DI_status":('bit','Estado de las entradas digitales'), #(bit0:DI1,bit1:DI2,bit2:DI3,bit3:DI4)
    "P_kWh_A":('kWh','Energía activa en A: Positiva'),
    "R_kWh_A":('kWh','Energía activa en A: Inversa'),
    "P_kvarh_A":('kVarh','Energía reactiva en A: Positiva'),
    "R_kvarh_A":('kVarh','Energía reactiva en A: Inversa'),
    "P_kWh_B":('kWh','Energía activa en B: Positiva'),
    "R_kWh_B":('kWh','Energía activa en B: Inversa'),
    "P_kvarh_B":('kVarh','Energía reactiva en B: Positiva'),
    "R_kvarh_B":('kVarh','Energía reactiva en B: Inversa'),
    "P_kWh_C":('kWh','Energía activa en C: Positiva'),
    "R_kWh_C":('kWh','Energía activa en C: Inversa'),
    "P_kvarh_C":('kVarh','Energía reactiva en C: Positiva'),
    "R_kvarh_C":('kVarh','Energía reactiva en A: Inversa'),
    "THD_A":('%','Rate de armónicos en A'),
    "THD_B":('%','Rate de armónicos en B'),
    "THD_C":('%','Rate de armónicos en C'),
    "THDC_A":('%','Rate de armónicos de corriente en A'), 
    "THDC_B":('%','Rate de armónicos de corriente en B'), 
    "THDC_C":('%','Rate de armónicos de corriente en C')
}


M3_MAPPING={ # Mapeo de constantes de mensaje PV-M3
    0:"serial_number",
    1: "vA", 2: "vB", 3: "vC", #Voltajes de cada línea
    4: "vAB", 5: "vBC", 6: "vCA", #Voltajes de cada fase
    7: "iA", 8: "iB", 9: "iC", #Corrientes de cada línea
    10: "PA", 11: "PB", 12: "PC", 13: "P", #Potencia Activa por línea y total
    14: "QA", 15: "QB", 16: "QC", 17: "Q", #Potencia Reactiva por línea y total
    18: "SA", 19: "SB", 20: "SC", 21: "S" , #Potencia Aparente por línea y total
    22: "PFA",23: "PFB",24: "PFC",25: "PF", #Factor de Potencia por línea y total
    26: "F", 27:"Signal_strength", #Frecuencia e intensidad de señal de transmisión
    28: "P_kWh_T", #Indication value of total positive active energy
    29: "R_kWh_T", #Indication value of total reverse active energy
    30: "P_kvarh_T", #Indication value of total positive reactive energy
    31: "R_kvarh_T", #Indication value of total reverse reactive energy
    32: "P_Active_demand", ##Demanda de potencia activa positiva actual
    33: "ICCID", #identificador único de placa
    34: "PT", #Valor de transformador de potencia del medidor
    35: "CT", #Valor de transformador de corriente del medidor (relación de transformación)
    ##A partir de aquí son las direcciones del segundo mensaje
    36: "TA", 37: "TB", 38: "TC", 39: "TN", #Temperaturas en líneas y neutro
    40: "iF", #Corriente de fuga
    41: "DI_status", #Estado de las entradas digitales (bit0:DI1,bit1:DI2,bit2:DI3,bit3:DI4)
    42: "P_kWh_A", 43: "R_kWh_A", #Energía activa en A: Positiva e Inversa/Reversa
    44: "P_kvarh_A", 45: "R_kvarh_A", #Energía reactiva en A: Positiva e Inversa/Reversa
    46: "P_kWh_B", 47: "R_kWh_B", #Energía activa en B: Positiva e Inversa/Reversa
    48: "P_kvarh_B", 49: "R_kvarh_B", #Energía reactiva en B: Positiva e Inversa/Reversa
    50: "P_kWh_C", 51: "R_kWh_C", #Energía activa en C: Positiva e Inversa/Reversa
    52: "P_kvarh_C", 53: "R_kvarh_C", #Energía reactiva en C: Positiva e Inversa/Reversa
    54: "THD_A", 55: "THD_B", 56: "THD_C" , #Rate de harmonicos de voltaje por línea
    57: "THDC_A",58: "THDC_B",59: "THDC_C", #Rate de harmonicos de corriente por línea
    60: "R_Active_demand", #Demanda de potencia activa inversa actual
    61: "P_Reactive_demand", #Demanda de potencia reactiva positiva actual
    62: "R_Reactive_demand", #Demanda de potencia reactiva inversa actual
    63: "V_unb", #Desbalance de voltaje en %
    64: "I_unb", #Desbalance de corriente en %
    65: "kWh_spike", #Energía total activa en "periodo spike"
    66: "kWh_peak", #Energía total activa en "periodo peak"
    67: "kWh_flat", #Energía total activa en "periodo flat"
    68: "kWh_valley", #Energía total activa en "periodo valley"
    69: "C1_kvarh", #Energía reactiva en 1er cuadrante
    70: "C2_kvarh", #Energía reactiva en 2do cuadrante
    71: "C3_kvarh", #Energía reactiva en 3er cuadrante
    72: "C4_kvarh"  #Energía reactiva en 4to cuadrante 
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('build_email') #Logger específico para Notificaciones

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
    




