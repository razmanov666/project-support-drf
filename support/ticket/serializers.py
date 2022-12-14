import json

from common_modules.state_machine import ManagerOfState
from rest_framework import serializers
from ticket.service import updating_json_objects
from ticket.tasks import task_send_email_about_cnahge_status
from ticket.tasks import task_send_email_client

from .models import Ticket


# class TicketSerializerUpdate(serializers.ModelSerializer):
#     """
#     Serialiser for update tickets by user. If user want to edit description of ticket
#     """
#     class Meta:
#         model = Ticket
#         exclude = (
#             "reporter",
#             "title",
#             "status",
#             "assigned",
#             "comments",
#         )


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
    """
    Serializer for create a new ticket.
    """

    reporter = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Ticket
        exclude = (
            "assigned",
            "comments",
            "status",
        )


class TicketSerializerAddComment(serializers.ModelSerializer):
    """
    Serializer for create a new comment for ticket.
    """

    comments = serializers.CharField(label="Comment")

    class Meta:
        model = Ticket
        fields = ("comments",)
        read_only_fields = ("created_by", "assigned")

    def update(self, instance, validated_data):
        data = updating_json_objects(self, instance, validated_data)
        task_send_email_client.delay(data.get("json_data"))
        return data["instance"]


class TicketSerializerChangeState(serializers.ModelSerializer):
    """
    Serializer for changing status (state) of ticket. Only for Admins and Managers.
    """

    class Meta:
        model = Ticket
        fields = ("status",)

    def update(self, instance, validated_data):
        current_state = ManagerOfState(instance.status)
        data = {"old_status": current_state._state.full_name_status, "email": instance.reporter.email}
        changed_status = eval(f"current_state.{self.context.get('method')}")
        instance.status = current_state._state.name_status
        data.update({"status": current_state._state.full_name_status})
        data_json = json.dumps((data), indent=4, sort_keys=True, default=str)
        if changed_status:
            task_send_email_about_cnahge_status.delay(data_json)
        return super().update(instance, validated_data)


class TicketSerializerAssigned(serializers.ModelSerializer):
    """
    Serializer for assigning a ticket on a user. Only for Admins and Managers.
    """

    assigned = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Ticket
        fields = ("assigned",)
