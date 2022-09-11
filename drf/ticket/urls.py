from django.urls import include
from django.urls import path

from .views import TicketAPIDestroy
from .views import TicketAPIList
from .views import TicketAPIUpdate

urlpatterns = [
    path("api/tickets/", TicketAPIList.as_view()),
    path("api/tickets/<int:pk>/", TicketAPIUpdate.as_view()),
    path("api/tickets_destroy/<int:pk>/", TicketAPIDestroy.as_view()),
    path("api/tickets/<int:pk>/", include("comment.urls")),
]
