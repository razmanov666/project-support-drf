from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    CLIENT = "CL"
    SD_MANAGER = "MG"
    ADMIN = "AD"
    ROLE_CHOICES = [
        (CLIENT, "Client"),
        (SD_MANAGER, "SD manager"),
        (ADMIN, "Admin"),
    ]
    first_name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    role = models.CharField(max_length=2, choices=ROLE_CHOICES, default=CLIENT)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
