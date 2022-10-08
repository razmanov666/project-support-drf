# from django.core.mail import send_mail
from support.celery import app


@app.task
def say_work(arg):
    print("work " + arg)


# @app.task
# def send_email():
#     send_mail(
#                 "Dear, " + str(comment.ticket.user),
#                 "You are have update in your ticket.",
#                 "app_notification@mail.ru",
#                 [comment.ticket.user.email],
#                 fail_silently=False,
#             )
