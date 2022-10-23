from django.db import models
from userauth.models import CustomUser


# class Status(models.Model):
#     opened = models.BooleanField(default=True)
#     in_progress = models.BooleanField()
#     done = models.BooleanField()
#     rejected = models.BooleanField()
#     on_hold = models.BooleanField()


class Ticket(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    OPENED = "OP"
    IN_PROGRESS = "IP"
    DONE = "DN"
    REJECTED = "RJ"
    ON_HOLD = "OH"
    STATUS_CHOICES = [
        (OPENED, "Opened"),
        (IN_PROGRESS, "In progress"),
        (DONE, "Done"),
        (REJECTED, "Rejected"),
        (ON_HOLD, "On hold"),
    ]
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=OPENED,
        editable=False,
    )
    reporter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="ticket_reporter")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="ticket_assigned",
        blank=True,
        null=True,
    )
    # comments = models.JSONField(null=True,)

    def __str__(self):
        return self.title
