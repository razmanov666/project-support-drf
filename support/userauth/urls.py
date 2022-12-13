from django.urls import path

from .views import UserToAdmin
from .views import UserToClient
from .views import UserToManager

urlpatterns = [
    # Urls for change role
    path("api/users/<int:user_pk>/to_admin", UserToAdmin.as_view()),
    path("api/users/<int:user_pk>/to_manager", UserToManager.as_view()),
    path("api/users/<int:user_pk>/to_client", UserToClient.as_view()),
]
