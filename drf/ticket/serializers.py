from rest_framework import serializers

from .models import Ticket

# from .models import Status


class TicketSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # status = Status.objects.get(pk=3)

    class Meta:
        model = Ticket
        fields = "__all__"
