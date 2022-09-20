from rest_framework import serializers

from .models import Comment
from .models import Ticket


class CurrentTicketDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return Ticket.objects.get(
            pk=serializer_field.context["request"].parser_context["kwargs"][
                "ticket_pk"
            ]
        )

class CurrentTicketFilter:
    requires_context = True

    def __call__(self, serializer_field):
        return Ticket.objects.filter(serializer_field.context["request"].parser_context["kwargs"][
                "ticket_pk"
            ])

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    ticket = serializers.HiddenField(default=CurrentTicketDefault())
    reply_to = serializers.Field()

    class Meta:
        model = Comment
        fields = "__all__"

    def create(self, validated_data):
        comment = Comment(
            ticket=validated_data["ticket"],
            user=validated_data["user"],
            text=validated_data["text"]
        )
        comment.save()
        return comment
    
    # def get_queryset(self):
