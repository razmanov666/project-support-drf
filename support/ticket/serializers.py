import datetime
from types import NoneType

from rest_framework import serializers

from .models import Ticket


class TicketSerializerUpdate(serializers.ModelSerializer):
    reporter = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Ticket
        # fields = "__all__"
        # read_only_fields = ("status", "assigned", "comments")
        exclude = (
            "title",
            "status",
            "assigned",
            "comments",
        )


class SimpleUserSerializer(serializers.ModelSerializer):
    reporter = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Ticket
        # fields = "__all__"
        exclude = (
            "title",
            "status",
            "assigned",
            "comments",
        )


class AdminUserSerializer(serializers.ModelSerializer):
    reporter = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Ticket
        exclude = (
            "title",
            "comments",
        )


class TicketSerializerCreate(serializers.ModelSerializer):
    reporter = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.HiddenField(default=Ticket.STATUS_CHOICES[0][0])

    class Meta:
        model = Ticket
        exclude = (
            "assigned",
            "comments",
        )


class TicketSerializerAddComment(serializers.ModelSerializer):
    comments = serializers.CharField(label="Comment")

    class Meta:
        model = Ticket
        fields = ("comments",)

    def update(self, instance, validated_data):
        comments_exists = type(instance.comments) is not NoneType
        id_comment = str(len(instance.comments) + 1) if comments_exists else "1"
        content = validated_data.get("comments", instance.comments)
        created_by = self.context["request"].user.username
        comment_dict = {
            id_comment: {
                "content": content,
                "created_at": str(datetime.datetime.now()),
                "updated_at": str(datetime.datetime.now()),
                "created_by": created_by,
            }
        }
        if comments_exists:
            instance.comments.update(comment_dict)
        else:
            instance.comments = comment_dict
        instance.save()
        return instance
