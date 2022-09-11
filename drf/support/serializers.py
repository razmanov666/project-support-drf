# from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Comment
from .models import Status
from .models import Ticket


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    ticket = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    # print(serializers.PrimaryKeyRelatedField(many=False, read_only = True))

    class Meta:
        model = Comment
        fields = "__all__"
        # extra_kwargs = {"pk": {""}}


class TicketSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = Status.objects.get(pk=3)

    class Meta:
        model = Ticket
        fields = "__all__"
