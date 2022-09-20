from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.pagination import PageNumberPagination
from ticket.permissions import IsOwnerOrAdminOrSupport
from ticket.serializers import TicketSerializerCreate
from ticket.serializers import TicketSerializerUpdate

from .models import Ticket

from rest_framework.permissions import IsAuthenticated


class TicketAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 10000


class TicketAPIList(ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializerCreate
    permission_classes = (IsAuthenticated,)
    pagination_class = TicketAPIListPagination
    lookup_url_kwarg = "ticket_pk"

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return super().get_queryset(*args, **kwargs)
        else:
            return (
                super()
                .get_queryset(*args, **kwargs)
                .filter(user=self.request.user)
        )


class TicketAPIUpdate(RetrieveUpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializerUpdate
    lookup_url_kwarg = "ticket_pk"
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return super().get_queryset(*args, **kwargs)
        else:
            return (
                super()
                .get_queryset(*args, **kwargs)
                .filter(user=self.request.user)
        )


class TicketAPIDestroy(RetrieveDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializerCreate
    permission_classes = (IsOwnerOrAdminOrSupport,)
    lookup_url_kwarg = "ticket_pk"


    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return super().get_queryset(*args, **kwargs)
        else:
            return (
                super()
                .get_queryset(*args, **kwargs)
                .filter(user=self.request.user)
        )
