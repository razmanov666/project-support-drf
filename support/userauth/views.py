from common_modules.permissions import IsAdmin
from common_modules.permissions import IsAdminOrSupport
from common_modules.permissions import IsNotAuthenticated
from django.db.models import Q
from rest_framework import generics
from rest_framework.generics import UpdateAPIView

from .models import CustomUser
from .serializers import RegisterSerializer
from .serializers import UserSerializerUserToAdmin
from .serializers import UserSerializerUserToClient
from .serializers import UserSerializerUserToManager


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (IsNotAuthenticated,)
    serializer_class = RegisterSerializer


class UserToAdmin(UpdateAPIView):
    queryset = CustomUser.objects.filter(~Q(role="AD"))
    permission_classes = (IsAdmin,)
    serializer_class = UserSerializerUserToAdmin
    lookup_url_kwarg = "user_pk"


class UserToManager(UpdateAPIView):
    queryset = CustomUser.objects.filter(~Q(role="MG"))
    permission_classes = (IsAdminOrSupport,)
    serializer_class = UserSerializerUserToManager
    lookup_url_kwarg = "user_pk"


class UserToClient(UpdateAPIView):
    queryset = CustomUser.objects.filter(~Q(role="CL") & ~Q(role="AD"))
    permission_classes = (IsAdminOrSupport,)
    serializer_class = UserSerializerUserToClient
    lookup_url_kwarg = "user_pk"
