try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    __path__ = __import__('pkgutil').extend_path(__path__, __name__)


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 


class Sender():

    def sendmail(self, toaddr, subject, body):
        try:
            self.msg = MIMEMultipart()
            self.msg['From'] = self.fromaddr
            self.msg['To'] = toaddr
            self.msg['Subject'] = subject
            self.msg.attach(MIMEText(body, 'html'))
            self.send()
        except Exception as e:
            raise e

    def send(self):
        try:
            self.server.starttls()
            self.server.login(self.fromaddr, self.passwrd)
            text = self.msg.as_string()
            self.server.sendmail(self.fromaddr, self.msg['To'], text)
            self.server.quit()
        except Exception as e:
            self.server.quit()
            raise e

    def __init__(self, myConfig):
        try:
            self.config = myConfig
            self.fromaddr = self.config.core.getVariable("MAIL_USER")
            self.passwrd = self.config.core.getVariable("MAIL_PASS")
            self.mailserver = self.config.core.getVariable("MAIL_SERVER")
            self.port = self.config.core.getVariable("MAIL_SERVER_PORT")
            self.server = smtplib.SMTP(self.mailserver, self.port)
            self.server.connect(self.mailserver, self.port)
        except Exception as e:
            raise e