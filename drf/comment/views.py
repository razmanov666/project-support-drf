from comment.serializers import CommentSerializer
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ticket.permissions import IsOwnerOrAdminOrSupport, IsOwner

from .models import Comment

# from rest_framework.response import Response

from rest_framework.generics import RetrieveDestroyAPIView


class CommentAPIBase():
    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(ticket_id=self.kwargs["ticket_pk"])
        )
        

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

