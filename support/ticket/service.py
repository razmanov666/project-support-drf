from django.core.mail import send_mail
import json
from userauth.models import CustomUser

def send_mail_update_comments(object):
    message_data = json.loads(object)
    title_message = 'Ticket "' + message_data.get('ticket') + '" has update.'
    text_message = "Dear, " + message_data.get("username") + " you are have a new message in your ticket"
    send_mail(
                title_message,
                text_message,
                "app_notification@mail.ru",
                [message_data.get("email")],
                fail_silently=False,
            )


def send_mail_tickets_without_assigned(count: int):
    # message_data = json.loads(object)
    manager_list = CustomUser.objects.filter("MG")
    manager_list_mail = [user.mail for user in manager_list]
    title_message = str(count) + " Tickets haven't assigned manager."
    text_message = "http://127.0.0.1:8000/api/tickets/opened/"
    send_mail(
                title_message,
                text_message,
                "app_notification@mail.ru",
                manager_list_mail,
                fail_silently=False,
            )