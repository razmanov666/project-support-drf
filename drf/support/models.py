from django.db import models


class Ticket(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    is_solved = models.BooleanField(default=False)
    # user_id = models.ForeignKey()

    def __str__(self):
        return self.title
