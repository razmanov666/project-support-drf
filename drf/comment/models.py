from django.db import models
from ticket.models import Ticket
from userauth.models import CustomUser


class Comment(models.Model):
    text = models.TextField()
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text
