from django.conf import settings
from django.db import models


class Ticket(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    is_solved = models.BooleanField(default=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title
