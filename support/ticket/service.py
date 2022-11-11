from django.core.mail import send_mail
import json

def send_mail_update_comments(object):
    message_data = json.loads(object)
    print("\n\n")
    print(message_data[0], message_data[1])
    print("\n\n")
    send_mail(
                "Dear, " + str(message_data[0]),
                "You are have update in your ticket.",
                "app_notification@mail.ru",
                [message_data[1]],
                # fail_silently=False,
            )
