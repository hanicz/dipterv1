import smtplib
import os
from .env_vars import url, LEVEL
from logger import log_message


def send_activate_email(to_address, activate):
    log_message(LEVEL.INFO,'Sending activation email for: ' + to_address)
    try:
        credentials = os.getenv('MAIL').rsplit(':', 1)
        message = url + '/activate/' + activate
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(credentials[0], credentials[1])
        server.sendmail(credentials[0], to_address, message)
        server.quit()
    except Exception as e:
        log_message(LEVEL.ERROR, 'Failed to send email for: ' + to_address + ' Exception: ' + str(e))


def reset_password_email(to_address, activate):
    log_message(LEVEL.INFO, 'Sending reset email for: ' + to_address)
    try:
        credentials = os.getenv('MAIL').rsplit(':', 1)
        message = url + '/reset/' + activate
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(credentials[0], credentials[1])
        server.sendmail(credentials[0], to_address, message)
        server.quit()
    except Exception as e:
        log_message(LEVEL.ERROR, 'Failed to send email for: ' + to_address + ' Exception: ' + str(e))
