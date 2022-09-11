# from django.urls import include
from django.urls import path
from support.views import AllCommentAPIList
from support.views import AllTicketAPIList
from support.views import TicketAPIDestroy
from support.views import TicketAPIUpdate

# from support.views import CommentAPIUpdate

# from support.views import SolvedTicketAPIList
# from support.views import UnsolvedTicketAPIList
# def view():
#     pass

# p = path('project/<int:project_id>/user/<int:user_id>/project-detail', view)


urlpatterns = [
    # path("api/tickets/", AllTicketAPIList.as_view(), name="all_tickets"),
    # path("api/tickets/<int:ticket_id>/", TicketAPIUpdate.as_view()),
    # path("api/tickets/<int:ticket_id>/comments/",
    # AllCommentAPIList.as_view()),
    # path("api/tickets_destroy/<int:ticket_id>/", TicketAPIDestroy.as_view()),
    path("api/tickets/", AllTicketAPIList.as_view(), name="all_tickets"),
    path("api/tickets/<int:pk>/", TicketAPIUpdate.as_view()),
    path("api/tickets/<int:pk>/comments/", AllCommentAPIList.as_view()),
    path("api/tickets_destroy/<int:pk>/", TicketAPIDestroy.as_view()),
    # path("api/tickets/<int:ticket_id>/comments/<int:comment_id>/",
    #      CommentAPIUpdate.as_view()),
]
