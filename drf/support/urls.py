from django.urls import path
from support.views import AllCommentAPIList
from support.views import AllTicketAPIList
from support.views import TicketAPIUpdate

# from support.views import CommentAPIUpdate

# from support.views import SolvedTicketAPIList
# from support.views import UnsolvedTicketAPIList

urlpatterns = [
    path("api/tickets/", AllTicketAPIList.as_view(), name="all_tickets"),
    # path(
    #     "api/tickets/unsolved/",
    #     UnsolvedTicketAPIList.as_view(),
    #     name="unsolved_tickets",
    # ),
    # path(
    #     "api/tickets/solved/",
    #     SolvedTicketAPIList.as_view(),
    #     name="solved_tickets",
    # ),
    path("api/tickets/<int:pk>/", TicketAPIUpdate.as_view()),
    path("api/tickets/<int:pk>/comments/", AllCommentAPIList.as_view()),
    # path("api/tickets/<int:pk>/comments/", CommentAPIUpdate.as_view()),
]
