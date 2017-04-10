import smtplib
import os
from .env_vars import url, LEVEL
from logger import log_message
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_activate_email(to_address, activate):
    log_message(LEVEL.INFO,'Sending activation email for: ' + to_address)
    try:
        credentials = os.getenv('MAIL').rsplit(':', 1)

        from_address = credentials[0] + '@gmail.com'
        msg = MIMEMultipart()
        msg['From'] = from_address
        msg['To'] = to_address
        msg['Subject'] = "ACTIVATE"

        body = url + '/activate/' + activate
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_address, credentials[1])
        text = msg.as_string()
        server.sendmail(from_address, to_address, text)
        server.quit()
    except Exception as e:
        log_message(LEVEL.ERROR, 'Failed to send email for: ' + to_address + ' Exception: ' + str(e))


def reset_password_email(to_address, activate):
    log_message(LEVEL.INFO, 'Sending reset email for: ' + to_address)
    try:
        credentials = os.getenv('MAIL').rsplit(':', 1)

        from_address = credentials[0] + '@gmail.com'
        msg = MIMEMultipart()
        msg['From'] = from_address
        msg['To'] = to_address
        msg['Subject'] = "RESET"

        body = url + '/reset/' + activate
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_address, credentials[1])
        text = msg.as_string()
        server.sendmail(from_address, to_address, text)
        server.quit()
    except Exception as e:
        log_message(LEVEL.ERROR, 'Failed to send email for: ' + to_address + ' Exception: ' + str(e))
