import logging
import smtplib
import ssl
from email.message import EmailMessage

from celery import Celery
from celery import shared_task

app = Celery('root')


@shared_task
def send_email_async(email, random_code):
    logging.warning(email + str(random_code))
    email_sender = 'boronovshahriyor2004@gmail.com'  # noqa
    email_password = 'sqip huze ceri llpz'  # noqa
    subject = "salom"
    body = f"Tasdiqlash kodi: {random_code}"  # noqa

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email, em.as_string())
