import os

from celery import Celery


from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "support.settings")

app = Celery("support")
# ticket_app = Celery('ticket')
# userauth_app = Celery('userath')

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_shedule = {
    "check-ticket-for-autofrozen": {
        "task": "comment.tasks.autofrozen",
        "schedule": crontab(minute="*/5"),
    }
}
