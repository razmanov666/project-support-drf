from django.contrib import admin

from .models import Comment
from .models import Status
from .models import Ticket

admin.site.register(Ticket)
admin.site.register(Comment)
admin.site.register(Status)
