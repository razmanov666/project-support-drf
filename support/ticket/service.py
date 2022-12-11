import json
import os
from pathlib import Path

import environ
from django.core.mail import send_mail
from userauth.models import CustomUser

env = environ.Env(DEBUG=(bool, False))

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR.parent, ".env"))


def send_mail_update_comments(object):
    message_data = json.loads(object)
    title_message = 'Ticket "' + message_data.get("ticket") + '" has update.'
    text_message = "Dear, " + message_data.get("username") + " you are have a new message in your ticket"
    send_mail(
        title_message,
        text_message,
        env("EMAIL_HOST_USER"),
        [message_data.get("email")],
        fail_silently=False,
    )


def send_mail_tickets_without_assigned(count: int):
    manager_list_mail = [user.email for user in CustomUser.objects.filter(role="MG")]
    title_message = str(count) + " Tickets haven't assigned manager."
    text_message = "http://127.0.0.1:8000/api/tickets/opened/"
    send_mail(
        title_message,
        text_message,
        env("EMAIL_HOST_USER"),
        manager_list_mail,
        fail_silently=False,
    )


def send_mail_change_status_of_ticket():
    pass
