from datetime import datetime
from datetime import timezone

from ticket.models import Ticket
from ticket.service import send_mail_tickets_without_assigned
from ticket.service import send_mail_update_comments

from support.celery_settings import app


@app.task
def send_email_client(object):
    send_mail_update_comments(object)


@app.task
def autofrozen():
    tickets = Ticket.objects.all()
    for ticket in tickets:
        if ticket.status in ("OP", "IP") and (datetime.now(timezone.utc) - ticket.created_at).days >= 7:
            ticket.status = "OH"
            ticket.save()


@app.task
def send_email_manager():
    count = Ticket.objects.filter(assigned__isnull=True).count()
    print(count)
    send_mail_tickets_without_assigned(count)
