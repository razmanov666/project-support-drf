from common_permissions.permissions import IsAdminOrSupport
from common_permissions.permissions import IsOwnerOrAdminOrSupport
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
from ticket.serializers import TicketSerializerChangeStateGoDone
from ticket.serializers import TicketSerializerChangeStateGoInProgress
from ticket.serializers import TicketSerializerChangeStateGoOnHold
from ticket.serializers import TicketSerializerChangeStateGoOpened
from ticket.serializers import TicketSerializerChangeStateGoRejected
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
    def get_queryset(self, *args, **kwargs):
        if self.request.user.role in CustomUser.MANAGERS:
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


class TicketAPIToOpened(TicketAPIChangeStateBase):
    serializer_class = TicketSerializerChangeStateGoOpened


class TicketAPIToInProgress(TicketAPIChangeStateBase):
    serializer_class = TicketSerializerChangeStateGoInProgress


class TicketAPIToDone(TicketAPIChangeStateBase):
    serializer_class = TicketSerializerChangeStateGoDone


class TicketAPIToOnHold(TicketAPIChangeStateBase):
    serializer_class = TicketSerializerChangeStateGoOnHold


class TicketAPIToRejected(TicketAPIChangeStateBase):
    serializer_class = TicketSerializerChangeStateGoRejected


class TicketFilter(TicketAPIBase, ListAPIView):
    serializer_class = TicketSerializerCreate
    permission_classes = (IsOwnerOrAdminOrSupport,)


class TicketFilterOpened(TicketFilter):
    queryset = Ticket.objects.filter(status="OP")


class TicketFilterOnHold(TicketFilter):
    queryset = Ticket.objects.filter(status="OH")


class TicketFilterClosed(TicketFilter):
    queryset = Ticket.objects.filter(Q(status="RJ") | Q(status="DN"))


class TicketAPIAssigned(TicketAPIBase, UpdateAPIView):
    queryset = Ticket.objects.filter(assigned__isnull=True)
    serializer_class = TicketSerializerAssigned
    permission_classes = (IsAdminOrSupport,)
    lookup_url_kwarg = "ticket_pk"


class UserToAdmin(UpdateAPIView):
    queryset = CustomUser.objects.filter(~Q(role="AD"))


class UserToManager(UpdateAPIView):
    queryset = CustomUser.objects.filter(~Q(role="MG"))


class TicketAPIListInfo(ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializerListForManagers
    permission_classes = (IsAdminOrSupport,)
    lookup_url_kwarg = "ticket_pk"
