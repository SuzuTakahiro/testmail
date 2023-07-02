import smtplib
import configparser
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

CONF_FILE='config/settings.ini'
SMTP_SERVER_HOST="SMTP_SERVER_HOST"
SMTP_SERVER_PORT="SMTP_SERVER_PORT"
DEFAULT_FROM_ADDRESS="DEFAULT_FROM_ADDRESS"
DEFAULT_TO_ADDRESS="DEFAULT_TO_ADDRESS"

subject = "Test Email"
text_body = "改行テスト\nテストメール\rテストメール\r\n"
html_body = """
<html>
    <head></head>
    <body>
        <p>改行テスト <br>テストメール</p>
    </body>
</html>"""


def createMsg(config,subject,text_message,html_message,from_address=None,to_address=None):
    default_to_address =config['SETTINGS'][DEFAULT_FROM_ADDRESS]
    default_from_address = config['SETTINGS'][DEFAULT_TO_ADDRESS]
    msg = MIMEMultipart()
    msg["Subject"] = subject
    if from_address is None :
        msg["From"] = default_from_address
    else:
        msg["From"] = from_address
    if from_address is None :
        msg["To"] = default_to_address
    else:
        msg["To"] = to_address
    msg.attach(MIMEText(text_message, "plain"))
    msg.attach(MIMEText(html_message, "html"))
    return msg
     

def createSMTPSetting(config):
    smtp_host =  config['SETTINGS'][SMTP_SERVER_HOST]
    smtp_port = config['SETTINGS'][SMTP_SERVER_PORT]
    return smtplib.SMTP(smtp_host, smtp_port)

def sendMail(from_address=None,to_address=None):
    config = configparser.ConfigParser()
    config.read(CONF_FILE)
    smtp = createSMTPSetting(config)
    msg = createMsg(config,subject,text_body,html_body,from_address=from_address,to_address=to_address)
    smtp.send_message(msg)
    smtp.close()

if __name__ == "__main__":
    args = sys.argv
    if len(args) == 3:
        sendMail(args[1],args[2])
    else:
        sendMail()