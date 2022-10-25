from django.urls import include
from django.urls import path

from .views import TicketAPIAddComment
from .views import TicketAPIDestroy
from .views import TicketAPIList
from .views import TicketAPIUpdate

urlpatterns = [
    path("api/tickets/", TicketAPIList.as_view()),
    path("api/tickets/<int:ticket_pk>/", TicketAPIUpdate.as_view()),
    path("api/tickets_destroy/<int:ticket_pk>/", TicketAPIDestroy.as_view()),
    path("api/tickets/<int:ticket_pk>/comments/", TicketAPIAddComment.as_view()),
    # path("api/tickets/opened", TicketFilterOpened.as_view()),
    # path("api/tickets/closed", TicketFilterClosed.as_view()),
    # path("api/tickets/on_hold", TicketFilterOnHold.as_view()),
]
