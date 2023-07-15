import smtplib
import configparser
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

CONF_FILE = 'config/settings.ini'
SETTINGS = "SETTINGS"
SMTP_SERVER_HOST = "SMTP_SERVER_HOST"
SMTP_SERVER_PORT = "SMTP_SERVER_PORT"
DEFAULT_FROM_ADDRESS = "DEFAULT_FROM_ADDRESS"
DEFAULT_TO_ADDRESS = "DEFAULT_TO_ADDRESS"

SUBJECT = "Test Email"
TEXT_BODY = "改行テスト\nテストメール\rテストメール\r\n"
HTML_BODY = """
<html>
    <head></head>
    <body>
        <p>改行テスト <br>テストメール</p>
    </body>
</html>"""


def createMsg(config, subject, text_message, html_message, from_address=None, to_address=None):
    """Create a MIME message."""
    # Get the default addresses from the config file.
    default_to_address = config[SETTINGS][DEFAULT_FROM_ADDRESS]
    default_from_address = config[SETTINGS][DEFAULT_TO_ADDRESS]
    msg = MIMEMultipart()
    msg["Subject"] = subject
    if from_address is None:
        msg["From"] = default_from_address
    else:
        msg["From"] = from_address
    if from_address is None:
        msg["To"] = default_to_address
    else:
        msg["To"] = to_address
    msg.attach(MIMEText(text_message, "plain"))
    msg.attach(MIMEText(html_message, "html"))
    return msg


def createSMTPSetting(config):
    # Get the SMTP server host and port number from the configuration file.
    smtp_host = config[SETTINGS][SMTP_SERVER_HOST]
    smtp_port = config[SETTINGS][SMTP_SERVER_PORT]
    # Create the SMTP setting.
    return smtplib.SMTP(smtp_host, smtp_port)


def sendMail(from_address=None, to_address=None):
    # Read the configuration file
    config = configparser.ConfigParser()
    config.read(CONF_FILE)

    # Create the SMTP object
    smtp = createSMTPSetting(config)

    # Create the message object
    msg = createMsg(config, SUBJECT, TEXT_BODY, HTML_BODY,
                    from_address=from_address, to_address=to_address)

    # Send the message
    smtp.send_message(msg)
    smtp.close()


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 3:
        sendMail(args[1], args[2])
    else:
        sendMail()
