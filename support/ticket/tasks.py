from support.celery_settings import app
from ticket.service import send_mail_update_comments, send_mail_tickets_without_assigned
from ticket.models import Ticket

@app.task
def send_email_client(object):
    send_mail_update_comments(object)

@app.task
def autofrozen():
    pass

@app.task
def send_email_manager():
    count = Ticket.objects.filter(assigned__isnull=True).count()
    print(count)
    send_mail_tickets_without_assigned(count)
