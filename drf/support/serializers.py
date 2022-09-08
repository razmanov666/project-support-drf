from rest_framework import serializers

from .models import Comment
from .models import Status
from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.HiddenField(default=Status.objects.get(pk=3))
    comment = serializers.HiddenField(default=[])

    class Meta:
        model = Ticket
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # status = serializers.HiddenField(default=3)
    # comment = serializers.HiddenField(default=[])

    class Meta:
        model = Comment
        fields = "__all__"
