import os

import smtplib
import mimetypes
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText


def send_email(subject, addr_from, addr_to, message, send_file=None):
    """Sending the email

    Args:
        subject (str): The email subject.
        addr_from (str): The email sender's address.
        addr_to (str): The email reciever's address.
        message (str): The message to send.
        send_file (str, optional): The sending file's path. Default set to `None`
    """

    for email in addr_to:
        body = MIMEMultipart()
        body['From'] = addr_from
        body['To'] = email
        body['Subject'] = subject
        body.attach(MIMEText(message, 'plain'))

        if send_file is not None:
            filename = os.path.basename(send_file)

            if os.path.isfile(send_file):
                ctype = mimetypes.guess_type(send_file)[0]
                maintype, subtype = ctype.split('/', 1)

                with open(send_file, 'rb') as fp:
                    file = MIMEBase(maintype, subtype)
                    file.set_payload(fp.read())
                    fp.close()

                encoders.encode_base64(file)
                file.add_header('Content-Disposition',
                                'attachment', filename=filename)

            body.attach(file)

        server = smtplib.SMTP('localhost')
        server.sendmail(body['From'], email, body.as_string())
        server.quit()
