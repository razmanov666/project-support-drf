from common_permissions.permissions import IsNotAuthenticated
from rest_framework import generics

from .models import CustomUser
from .serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (IsNotAuthenticated,)
    serializer_class = RegisterSerializer
