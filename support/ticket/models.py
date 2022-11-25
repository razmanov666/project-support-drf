from django.db import models
from userauth.models import CustomUser


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
    reporter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="ticket_reporter", editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    assigned = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="ticket_assigned",
        blank=True,
        null=True,
    )
    comments = models.JSONField(
        null=True,
        blank=True,
    )

    # def __str__(self):
    #     return self.title
