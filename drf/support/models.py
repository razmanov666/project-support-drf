from django.conf import settings
from django.db import models


class Status(models.Model):
    status = models.CharField(max_length=150)
    desc_status = models.TextField()

    def __str__(self):
        return self.status


class Ticket(models.Model):
    title = models.CharField(max_length=150)
    text = models.TextField()
    status = models.ForeignKey(Status, on_delete=models.PROTECT, default=2)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    # comment_arr = models.ManyToManyField("Comment", blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField()
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE
    )
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True
