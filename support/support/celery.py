import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "support.settings")

app = Celery("tasks123")
app.config_from_object("django.conf:settings", namespace="CELERY")


app.conf.beat_shedule = {
    "check-ticket-for-autofrozen": {
        "task": "ticket.tasks.autofrozen",
        "schedule": crontab(minute="*/5"),
    },
    "unassigned-tickets-at-the-start-of-work-day":{
        "task": "ticket.tasks.send_email_manager",
        # "schedule": crontab(hour=17, minute=23 ,day_of_week='mon,tue,wed,thu,fri'),
        "schedule": 30.0
    }
}
app.autodiscover_tasks()
# app.conf.timezone = 'GMT+3'