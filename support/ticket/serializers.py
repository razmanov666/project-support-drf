from rest_framework import serializers
from ticket.service import updating_json_objects
from ticket.state_machine import ManagerOfState
from ticket.tasks import send_email_client

from .models import Ticket


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
            "description",
            "reporter",
            "title",
            "comments",
        )


class TicketSerializerCreate(serializers.ModelSerializer):
    reporter = serializers.HiddenField(default=serializers.CurrentUserDefault())

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
        data = updating_json_objects(self, instance, validated_data)
        send_email_client.delay(data.get("json_data"))
        return data["instance"]


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


class TicketSerializerAssigned(serializers.ModelSerializer):
    assigned = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Ticket
        fields = ("assigned",)
