from django.urls import path

from .views import TicketAPIAddComment
from .views import TicketAPIAssigned
from .views import TicketAPIDestroy
from .views import TicketAPIList
from .views import TicketAPIListInfo
from .views import TicketAPIToDone
from .views import TicketAPIToInProgress
from .views import TicketAPIToOnHold
from .views import TicketAPIToOpened
from .views import TicketAPIToRejected
from .views import TicketAPIUpdate
from .views import TicketFilterClosed
from .views import TicketFilterOnHold
from .views import TicketFilterOpened
from .views import UserToAdmin
from .views import UserToManager

urlpatterns = [
    # Urls for basically manage tickets
    path("api/tickets/", TicketAPIList.as_view()),
    path("api/tickets/<int:ticket_pk>/", TicketAPIUpdate.as_view()),
    path("api/tickets_list/<int:ticket_pk>/", TicketAPIListInfo.as_view()),
    path("api/tickets_destroy/<int:ticket_pk>/", TicketAPIDestroy.as_view()),
    path("api/tickets/<int:ticket_pk>/comments/", TicketAPIAddComment.as_view()),
    # Urls for manage a state of tickets
    path("api/tickets/<int:ticket_pk>/to_opened", TicketAPIToOpened.as_view()),
    path("api/tickets/<int:ticket_pk>/to_in_progress", TicketAPIToInProgress.as_view()),
    path("api/tickets/<int:ticket_pk>/to_done", TicketAPIToDone.as_view()),
    path("api/tickets/<int:ticket_pk>/to_on_hold", TicketAPIToOnHold.as_view()),
    path("api/tickets/<int:ticket_pk>/to_rejected", TicketAPIToRejected.as_view()),
    # Urls for filter tickets by state
    path("api/tickets/opened", TicketFilterOpened.as_view()),
    path("api/tickets/closed", TicketFilterClosed.as_view()),
    path("api/tickets/on_hold", TicketFilterOnHold.as_view()),
    # Url for assign the ticket
    path("api/tickets/<int:ticket_pk>/assigned", TicketAPIAssigned.as_view()),
    # Urls for creating new admin or SD_manager
    path("api/<int:user_pk>/to_admin", UserToAdmin.as_view()),
    path("api/<int:user_pk>/to_manager", UserToManager.as_view()),
]
