from django.db import models
from userauth.models import CustomUser

# from ticket.models import Ticket


class Comment(models.Model):
    content = models.TextField()
    # ticket = models.ForeignKey(
    #     Ticket,
    #     on_delete=models.CASCADE,
    # )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_bg = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.text
