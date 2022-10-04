from django.contrib import admin

from .models import Status
from .models import Ticket


class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "text",
        "status",
        "time_create",
        "time_update",
        "user",
    )
    # list_display_links = ("id", "title")
    # search_fields = ("title", "content")
    # list_editable = ("is_published",)
    # list_filter = ("is_published", "category")


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Status)
