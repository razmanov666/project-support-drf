import json
import os
from datetime import datetime
from datetime import timezone
from pathlib import Path
from types import NoneType

import environ
from django.core.mail import send_mail
from django.db.models import Q
from django.http import Http404
from ticket.models import Ticket
from userauth.models import CustomUser

env = environ.Env(DEBUG=(bool, False))

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR.parent, ".env"))


def send_mail_update_comments(object):
    """
    TaskFunction for notify user about create a new comment by another user.
    """
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


def send_mail_tickets_without_assigned():
    """
    TaskFunction for sending notifications before the start of the work day, only for Managers.
    """
    count = Ticket.objects.filter(assigned__isnull=True).count()
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


def send_mail_change_status_of_ticket(object):
    """
    TaskFunction for sending notifications about changing the status (state) of ticket.
    """
    message_data = json.loads(object)
    title_message = f"Ticket status was changed '{message_data.get('old_status')}' >>> '{message_data.get('status')}'."
    text_message = "Your Ticket has a new state."
    send_mail(
        title_message,
        text_message,
        env("EMAIL_HOST_USER"),
        [message_data.get("email")],
        fail_silently=False,
    )


def updating_json_objects(self_obj, instance, validated_data):
    """
    Function for correctly working with data of JSONField for field comments of ticket.
    """
    comments_exists = type(instance.comments) is not NoneType
    id_comment = str(len(instance.comments) + 1) if comments_exists else "1"
    content = validated_data.get("comments", instance.comments)
    created_by = self_obj.context["request"].user.username
    comment_dict = {
        id_comment: {
            "content": content,
            "created_at": str(datetime.now()),
            "created_by": created_by,
        }
    }
    if comments_exists:
        instance.comments.update(comment_dict)
    else:
        instance.comments = comment_dict
        instance.save()

    notify_json_data = get_notify_json_data(created_by, instance)

    return {"instance": instance, "json_data": notify_json_data}


def get_notify_json_data(comment_created_by, instance):
    """
    Function for preparing data for notification.
    """
    if not instance.assigned:
        raise Http404
    ticket_assigned = instance.assigned.username
    if comment_created_by == ticket_assigned:
        target_user = instance.reporter
    else:
        target_user = instance.assigned
    notification_dict_data = {"email": target_user.email, "username": target_user.username, "ticket": instance.title}
    json_data = json.dumps((notification_dict_data), indent=4, sort_keys=True, default=str)
    return json_data


def autofrozen():
    """
    TaskFunction for checking tickets and automatically change status to OnHold.
    For tickets which have not been updated or have not been used more than 7 days.
    """
    tickets = Ticket.objects.filter(Q(status="OP") | Q(status="IP"))
    for ticket in tickets:
        if ticket.comments:
            datetime_last_comment = datetime.strptime(
                ticket.comments[list(ticket.comments.keys())[-1]].get("created_at"), "%Y-%m-%d %H:%M:%S.%f"
            )
            if (datetime.now() - datetime_last_comment).days >= 7:
                ticket.status = "OH"
                ticket.save()
        else:
            ticket_last_edit = max(ticket.created_at, ticket.updated_at)
            if (datetime.now(timezone.utc) - ticket_last_edit).days >= 7:
                ticket.status = "OH"
                ticket.save()
