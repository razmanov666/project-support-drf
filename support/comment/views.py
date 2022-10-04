from comment.serializers import CommentSerializer
from common_permissions.permissions import IsOwner
from common_permissions.permissions import IsOwnerOrAdminOrSupport
from django.db.models import Q
from django.http import Http404
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Comment

# from rest_framework.response import Response


class CommentAPIBase:
    def get_queryset(self, *args, **kwargs):
        ticket_query = Q(ticket_id=self.kwargs["ticket_pk"])
        comment_by_ticket_query = Q(ticket__user=self.request.user)
        if self.request.user.is_staff or self.request.user.is_superuser:
            return super().get_queryset(*args, **kwargs).filter(ticket_query)
        elif not self.request.user.is_anonymous:
            return (
                super()
                .get_queryset(*args, **kwargs)
                .filter(ticket_query & comment_by_ticket_query)
            )
        else:
            raise Http404


class CommentAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 10000


class CommentAPIList(CommentAPIBase, ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = CommentAPIListPagination


class CommentAPIUpdate(CommentAPIBase, RetrieveUpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsOwner,)


class CommentAPIDestroy(CommentAPIBase, RetrieveDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrAdminOrSupport,)
