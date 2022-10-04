from rest_framework import serializers

from .models import Status
from .models import Ticket


class TicketSerializerUpdate(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = Status.objects.all()

    class Meta:
        model = Ticket
        fields = "__all__"


class SimpleUserSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Ticket
        fields = "__all__"
        read_only_fields = ("status",)


class AdminUserSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = Status.objects.all()

    class Meta:
        model = Ticket
        fields = "__all__"


class TicketSerializerCreate(TicketSerializerUpdate):
    status = serializers.HiddenField(
        default=Status.objects.filter(status="Unsolved")
    )
