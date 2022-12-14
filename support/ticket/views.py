from common_modules.permissions import IsAdminOrSupport
from common_modules.permissions import IsOwnerOrAdminOrSupport
from django.db.models import Q
from django.http import Http404
from rest_framework.generics import ListAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from ticket.serializers import TicketSerializerAddComment
from ticket.serializers import TicketSerializerAssigned
from ticket.serializers import TicketSerializerChangeState
from ticket.serializers import TicketSerializerCreate
from ticket.serializers import TicketSerializerListForManagers
from ticket.serializers import TicketSerializerListForUser
from userauth.models import CustomUser

from .models import Ticket


class TicketAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 10000


class TicketAPIBase:
    """
    Abstract class with get_queryset for owners of tickets or for Managers and Admins.
    """

    def get_queryset(self, *args, **kwargs):
        if not self.request.user.is_anonymous and self.request.user.role in CustomUser.MANAGERS:
            return super().get_queryset(*args, **kwargs)
        elif not self.request.user.is_anonymous:
            return super().get_queryset(*args, **kwargs).filter(reporter=self.request.user)
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
    serializer_class = TicketSerializerListForUser


class TicketAPIDestroy(TicketAPIBase, RetrieveDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializerCreate
    permission_classes = (IsOwnerOrAdminOrSupport,)
    lookup_url_kwarg = "ticket_pk"


class TicketAPIAddComment(TicketAPIBase, RetrieveUpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializerAddComment
    permission_classes = (IsOwnerOrAdminOrSupport,)
    lookup_url_kwarg = "ticket_pk"


class TicketAPIChangeStateBase(TicketAPIBase, UpdateAPIView):
    queryset = Ticket.objects.all()
    permission_classes = (IsAdminOrSupport,)
    lookup_url_kwarg = "ticket_pk"
    serializer_class = TicketSerializerChangeState


class TicketAPIToOpened(TicketAPIChangeStateBase):
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["method"] = "go_opened()"
        return context


class TicketAPIToInProgress(TicketAPIChangeStateBase):
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["method"] = "go_in_progress()"
        return context


class TicketAPIToDone(TicketAPIChangeStateBase):
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["method"] = "go_done()"
        return context


class TicketAPIToOnHold(TicketAPIChangeStateBase):
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["method"] = "go_on_hold()"
        return context


class TicketAPIToRejected(TicketAPIChangeStateBase):
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["method"] = "go_rejected()"
        return context


class TicketAPIAssigned(TicketAPIBase, UpdateAPIView):
    queryset = Ticket.objects.filter(assigned__isnull=True)
    serializer_class = TicketSerializerAssigned
    permission_classes = (IsAdminOrSupport,)
    lookup_url_kwarg = "ticket_pk"


class TicketAPIInfo(ListAPIView):
    """
    Class for get full info about tickets.
    """

    queryset = Ticket.objects.all()
    permission_classes = (IsAdminOrSupport,)
    serializer_class = TicketSerializerListForManagers
    pagination_class = TicketAPIListPagination


# Classes for filtering tickets
class TicketFilter(TicketAPIBase, ListAPIView):
    pagination_class = TicketAPIListPagination
    serializer_class = TicketSerializerCreate
    permission_classes = (IsOwnerOrAdminOrSupport,)


class TicketFilterOpened(TicketFilter):
    queryset = Ticket.objects.filter(status="OP")


class TicketFilterOnHold(TicketFilter):
    queryset = Ticket.objects.filter(status="OH")


class TicketFilterClosed(TicketFilter):
    queryset = Ticket.objects.filter(Q(status="RJ") | Q(status="DN"))
