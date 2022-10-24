from rest_framework import serializers

from .models import Ticket

# from .models import Status


class TicketSerializerUpdate(serializers.ModelSerializer):
    reporter = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.HiddenField(default="")

    class Meta:
        model = Ticket
        fields = "__all__"
        read_only_fields = ("status", "assigned")


class SimpleUserSerializer(serializers.ModelSerializer):
    reporter = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Ticket
        fields = "__all__"
        read_only_fields = ("status",)


class AdminUserSerializer(serializers.ModelSerializer):
    reporter = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # status = Status.objects.all()

    class Meta:
        model = Ticket
        fields = "__all__"


class TicketSerializerCreate(TicketSerializerUpdate):
    reporter = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.HiddenField(default=Ticket.STATUS_CHOICES[0][0])
