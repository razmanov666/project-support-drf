from rest_framework import serializers

from .models import Status
from .models import Ticket


class TicketSerializerUpdate(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = Status.objects.get(pk=1)

    class Meta:
        model = Ticket
        fields = "__all__"


class TicketSerializerCreate(TicketSerializerUpdate):
    status = serializers.HiddenField(default=Status.objects.get(pk=1))
