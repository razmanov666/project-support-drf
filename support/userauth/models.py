from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    CLIENT = "CL"
    SD_MANAGER = "MG"
    ADMIN = "AD"
    ROLE_CHOICES = [
        (CLIENT, "CLient"),
        (SD_MANAGER, "Sd_manager"),
        (ADMIN, "Admin"),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    role = models.CharField(
        max_length=2, choices=ROLE_CHOICES, default=CLIENT, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
