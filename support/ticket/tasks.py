from support.celery import app
from ticket.service import send_mail_update_comments

@app.task
def send_email(object):
    send_mail_update_comments(object)
