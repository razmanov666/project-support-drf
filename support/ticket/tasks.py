from ticket.service import autofrozen
from ticket.service import send_mail_tickets_without_assigned
from ticket.service import send_mail_update_comments

from support.celery_settings import app


@app.task
def task_send_email_client(object):
    send_mail_update_comments(object)


@app.task
def task_autofrozen():
    autofrozen()


@app.task
def task_send_email_manager():
    send_mail_tickets_without_assigned()
