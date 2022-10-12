# Generated by Django 4.1 on 2022-10-11 23:22
import django.db.models.deletion
from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("ticket", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="ticket",
            name="assigned",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="ticket",
            name="reporter",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="customuser_id",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="ticket",
            name="status",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="ticket.status"
            ),
        ),
    ]
