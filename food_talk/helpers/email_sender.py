import smtplib, ssl
import imghdr
from email.message import EmailMessage
import datetime
from dotenv import dotenv_values

config = dotenv_values()
context = ssl.create_default_context()

def send_email(attachment_path=''):
    msg = EmailMessage()
    curr_time = datetime.datetime.now()
    msg['Subject'] = f'The Tale of Food login authorization request at {curr_time}.'
    msg['from'] = config['SENDER_ADDR']
    msg['to'] = config['RECIPIENT_ADDR']

    if attachment_path:
        with open(attachment_path, 'rb') as fp:
            img_data = fp.read()
        msg.add_attachment(img_data, maintype='image',
                            subtype=imghdr.what(None, img_data))
    else:
        print('Sending the email without an image attachment.')
    with smtplib.SMTP_SSL('smtp.126.com', 465, context=context) as s:
        s.login(config['SENDER_ADDR'], config['SENDER_PASSWD'])
        try:
            s.send_message(msg)
        finally:
            s.quit()
