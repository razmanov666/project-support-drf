from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.pagination import PageNumberPagination
from ticket.permissions import IsOwnerOrAdminOrSupport
from ticket.serializers import TicketSerializerCreate
from ticket.serializers import TicketSerializerUpdate

from .models import Ticket

# from rest_framework.permissions import IsAuthenticatedOrReadOnly


class TicketAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 10000


class TicketAPIList(ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializerCreate
    permission_classes = (IsOwnerOrAdminOrSupport,)
    pagination_class = TicketAPIListPagination
    lookup_url_kwarg = "ticket_pk"


class TicketAPIUpdate(RetrieveUpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializerUpdate
    lookup_url_kwarg = "ticket_pk"
    # permission_classes = (IsAuthenticated,)


class TicketAPIDestroy(RetrieveDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializerCreate
    permission_classes = (IsOwnerOrAdminOrSupport,)
    lookup_url_kwarg = "ticket_pk"
