import datetime
from types import NoneType

from rest_framework import serializers
from .tasks import send_email_client
from .models import Ticket
import json
from ticket.state_machine import ManagerOfState


class TicketSerializerUpdate(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        exclude = (
            "reporter",
            "title",
            "status",
            "assigned",
            "comments",
        )


class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        exclude = (
            "reporter",
            "title",
            "status",
            "assigned",
            "comments",
        )


class AdminUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        exclude = (
            "reporter",
            "title",
            "comments",
        )


class TicketSerializerCreate(serializers.ModelSerializer):
    reporter = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Ticket
        exclude = (
            "assigned",
            "comments",
            "status",
        )


class TicketSerializerAddComment(serializers.ModelSerializer):
    comments = serializers.CharField(label="Comment")

    class Meta:
        model = Ticket
        fields = ("comments",)
        read_only_fields = ("created_by", "assigned")

    def update(self, instance, validated_data):
        comments_exists = (type(instance.comments) is not NoneType)
        id_comment = str(len(instance.comments) +
                         1) if comments_exists else "1"
        content = validated_data.get("comments", instance.comments)
        created_by = self.context["request"].user.username
        comment_dict = {
            id_comment: {
                "content": content,
                "created_at": str(datetime.datetime.now()),
                "created_by": created_by,
            }
        }
        if comments_exists:
            instance.comments.update(comment_dict)
        else:
            instance.comments = comment_dict
        instance.save()

        notify_json_data = get_notify_json_data(created_by, instance)
        send_email_client.delay(notify_json_data)

        return instance


class TicketSerializerChangeStateBase(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("status",)


class TicketSerializerChangeStateGoOpened(TicketSerializerChangeStateBase):
    def update(self, instance, validated_data):
        current_state = ManagerOfState(instance.status)
        current_state.go_opened()
        instance.status = current_state._state.name_status
        return super().update(instance, validated_data)


class TicketSerializerChangeStateGoInProgress(TicketSerializerChangeStateBase):
    def update(self, instance, validated_data):
        current_state = ManagerOfState(instance.status)
        current_state.go_in_progress()
        instance.status = current_state._state.name_status
        return super().update(instance, validated_data)


class TicketSerializerChangeStateGoDone(TicketSerializerChangeStateBase):
    def update(self, instance, validated_data):
        current_state = ManagerOfState(instance.status)
        current_state.go_done()
        instance.status = current_state._state.name_status
        return super().update(instance, validated_data)


class TicketSerializerChangeStateGoRejected(TicketSerializerChangeStateBase):
    def update(self, instance, validated_data):
        current_state = ManagerOfState(instance.status)
        current_state.go_rejected()
        instance.status = current_state._state.name_status
        return super().update(instance, validated_data)


class TicketSerializerChangeStateGoOnHold(TicketSerializerChangeStateBase):
    def update(self, instance, validated_data):
        current_state = ManagerOfState(instance.status)
        current_state.go_on_hold()
        instance.status = current_state._state.name_status
        return super().update(instance, validated_data)


def get_notify_json_data(comment_created_by, instance):
    ticket_assigned = instance.assigned.username
    if comment_created_by == ticket_assigned:
        target_user = instance.reporter
    else:
        target_user = instance.assigned
    notification_dict_data = {"email": target_user.email,
                              "username": target_user.username,
                              "ticket": instance.title}
    json_data = json.dumps((notification_dict_data),
                           indent=4, sort_keys=True, default=str)
    return json_data
