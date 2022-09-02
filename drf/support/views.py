from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from support.models import Ticket
from support.serializers import TicketSerializer


class TicketAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 10000


class AllTicketAPIList(ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = TicketAPIListPagination


class UnsolvedTicketAPIList(AllTicketAPIList):
    queryset = Ticket.objects.filter(is_solved=False)


class SolvedTicketAPIList(AllTicketAPIList):
    queryset = Ticket.objects.filter(is_solved=True)


class TicketAPIUpdate(RetrieveUpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = (IsAuthenticated,)
