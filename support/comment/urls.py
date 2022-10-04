from django.urls import path

from .views import CommentAPIList
from .views import CommentAPIUpdate

urlpatterns = [
    path("comments/", CommentAPIList.as_view()),
    path("comments/<int:pk>/", CommentAPIUpdate.as_view()),
]
