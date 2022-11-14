from support.celery import app
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

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'))

@app.task
def test(arg):
    print(arg)