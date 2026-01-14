import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage

import logging
from typing import Optional, Dict, Any

from AlwaysOn.uS.notifier.email.email_body import email_builder

SMTP_SERVER = "mail.premium-energia.com"
SMTP_PORT = 465
SENDER_USERNAME = "monitoreo@premium-energia.com" 
SENDER_PASSWORD = "m0n1t0r30."

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('send_email') 

async def send_email(email_data:Dict[str,Any],alarm_html:str):
    
    receiver_data=email_data['receiver_data']
    project_name=receiver_data['project_name']
    meter_nickname=receiver_data['meter_nickname']
    recipients=receiver_data['recipients_list']

    alarm_level=email_data['event_data']['level']
    
    alarm_selector=''

    match alarm_level:
        case 1:
            alarm_selector=r'AlwaysOn/uS/notifier/img/low_alarm.png'
        case 2:
            alarm_selector=r'AlwaysOn/uS/notifier/img/mid_alarm.png'
        case 3:
            alarm_selector=r'AlwaysOn/uS/notifier/img/high_alarm.png'
        case _:
            alarm_selector=r'AlwaysOn/uS/notifier/img/low_alarm.png'
            logger.info('No specified alarm level, taking 1 as default')

    msg=MIMEMultipart('related')
    msg['Subject'] = f"⚠POWERVIEW: {project_name} | {meter_nickname} "
    msg['From'] = SENDER_USERNAME

    # Aquí va la LISTA de destinatarios, unida en texto
    msg['To'] = ", ".join(recipients)

    #msg['To'] = receiver_username
    msg['Bcc'] = SENDER_USERNAME

    msg_alternative = MIMEMultipart('alternative')
    msg.attach(msg_alternative)
    msg_alternative.attach(MIMEText(alarm_html, 'html'))

    for img_file, cid in [(r'AlwaysOn/uS/notifier/img/alarm_header.png', 'Alarm_header'),
                         (r'AlwaysOn/uS/notifier/img/alarm_footer.png', 'Alarm_footer'),
                         (alarm_selector, 'Alarm_level')]:
        with open(img_file, "rb") as f:
            img = MIMEImage(f.read())
            img.add_header('Content-ID', f'<{cid}>')
            img.add_header('Content-Disposition', 'inline', filename=img_file)
            msg.attach(img)

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_USERNAME, SENDER_PASSWORD) 
            server.send_message(msg)
        logger.info("Email sent")
        return True
    
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return False

async def notify_by_email(email_data:Dict[str,Any],counter_notif:int)->bool:
    
    email_html=await email_builder(email_data,counter_notif)

    if not email_html:
        return None
    
    sent_email=await send_email(email_data,email_html)
    
    if not sent_email:
        return None
    
    return True