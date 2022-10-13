from django.core.mail import send_mail
from rest_framework import serializers
from ticket.models import Ticket

from .models import Comment


class CurrentTicketDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return Ticket.objects.get(pk=serializer_field.context["request"].parser_context["kwargs"].get("ticket_pk"))


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    ticket = serializers.HiddenField(default=CurrentTicketDefault())

    class Meta:
        model = Comment
        fields = "__all__"

    def create(self, validated_data):
        comment = Comment(
            ticket=validated_data["ticket"],
            user=validated_data["user"],
            text=validated_data["text"],
        )
        comment.save()
        if comment.ticket.user != comment.user:
            send_mail(
                "Dear, " + str(comment.ticket.user),
                "You are have update in your ticket.",
                "app_notification@mail.ru",
                [comment.ticket.user.email],
                fail_silently=False,
            )
        return comment
