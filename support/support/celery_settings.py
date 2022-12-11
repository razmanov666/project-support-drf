import os
from pathlib import Path

import environ
from celery import Celery
from celery.schedules import crontab

env = environ.Env(DEBUG=(bool, False))

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR.parent, ".env"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "support.settings")

app = Celery()
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "auto-frozen": {
        "task": "ticket.tasks.autofrozen",
        "schedule": crontab(minute="*/30"),
        # 'schedule': 5.0,
    },
    "send-unassigned-ticket-for-managers": {
        "task": "ticket.tasks.send_email_manager",
        "schedule": crontab(minute=0, hour=9, day_of_week="mon,tue,wed,thu,fri"),
    },
}

app.conf.timezone = env("TIME_ZONE")
