from django.http import Http404
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from ticket.permissions import IsOwnerOrAdminOrSupport
from ticket.serializers import AdminUserSerializer
from ticket.serializers import SimpleUserSerializer
from ticket.serializers import TicketSerializerCreate

from .models import Ticket


class TicketAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 10000


class TicketAPIBase:
    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return super().get_queryset(*args, **kwargs)
        elif not self.request.user.is_anonymous:
            return (
                super()
                .get_queryset(*args, **kwargs)
                .filter(user=self.request.user)
            )
        else:
            raise Http404


class TicketAPIList(TicketAPIBase, ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializerCreate
    permission_classes = (IsAuthenticated,)
    pagination_class = TicketAPIListPagination
    lookup_url_kwarg = "ticket_pk"


class TicketAPIUpdate(TicketAPIBase, RetrieveUpdateAPIView):
    queryset = Ticket.objects.all()
    permission_classes = (IsOwnerOrAdminOrSupport,)
    lookup_url_kwarg = "ticket_pk"

    def get_serializer_class(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return AdminUserSerializer
        elif not self.request.user.is_anonymous:
            return SimpleUserSerializer
        else:
            raise Http404


class TicketAPIDestroy(TicketAPIBase, RetrieveDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializerCreate
    permission_classes = (IsOwnerOrAdminOrSupport,)
    lookup_url_kwarg = "ticket_pk"
