from rest_framework import serializers
from ticket.service import updating_json_objects
from ticket.tasks import task_send_email_client

from .models import Ticket
from support.common_modules.state_machine import ManagerOfState


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


class TicketSerializerListForUser(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        exclude = (
            "reporter",
            "title",
            "status",
            "assigned",
            "comments",
        )


class TicketSerializerListForManagers(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"


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
        task_send_email_client.delay(data.get("json_data"))
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


class TicketSerializerUserToAdmin(serializers.ModelSerializer):
    role = serializers.HiddenField(default="AD")

    class Meta:
        model = Ticket
        fields = ("role",)


class TicketSerializerUserToManager(serializers.ModelSerializer):
    role = serializers.HiddenField(default="MG")

    class Meta:
        model = Ticket
        fields = ("role",)
