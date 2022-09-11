from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from support.models import Comment
from support.models import Ticket
from support.serializers import CommentSerializer
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


class AllCommentAPIList(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = TicketAPIListPagination


class TicketAPIUpdate(RetrieveUpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    lookup_url_kwarg = "pk"
    # permission_classes = (IsAuthenticated,)


class TicketAPIDestroy(RetrieveDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = (IsAuthenticated,)


class CommentAPIUpdate(RetrieveUpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)


# class UnsolvedTicketAPIList(AllTicketAPIList):
#     queryset = Ticket.objects.filter(is_solved=False)


# class SolvedTicketAPIList(AllTicketAPIList):
#     queryset = Ticket.objects.filter(is_solved=True)
