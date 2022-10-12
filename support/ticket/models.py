from django.db import models
from userauth.models import CustomUser


class Status(models.Model):
    opened = models.BooleanField(default=True)
    in_progress = models.BooleanField()
    in_review = models.BooleanField()
    closed = models.BooleanField()
    rejected = models.BooleanField()
    on_hold = models.BooleanField()


class Ticket(models.Model):
    title = models.CharField(max_length=150, editable=False)
    description = models.TextField()
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    reporter = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        editable=False,
        related_name="customuser_id",
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    assigned = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, editable=False
    )
    comments = models.JSONField(null=True)

    def __str__(self):
        return self.title
