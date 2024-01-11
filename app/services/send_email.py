import smtplib
import os
from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv()

MAIL_SERVER = os.environ.get("MAIL_SERVER")
MAIL_PORT = os.environ.get("MAIL_PORT")
MAIL_FROM = os.environ.get("MAIL_FROM")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

def send_mail(mailTo: str, mail_data: dict):
    msg = EmailMessage()
    msg['From'] = MAIL_FROM
    msg['To'] = mailTo
    msg['Subject'] = mail_data['subject']
    msg.set_content(
        f"""\
           {mail_data['body']}   
        """,
         
    )
    with smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT) as smtp:
        smtp.login(MAIL_FROM, MAIL_PASSWORD)
        smtp.send_message(msg)
