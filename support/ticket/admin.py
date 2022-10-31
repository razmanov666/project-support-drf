from django.contrib import admin

from .models import Ticket

# from .models import Status


class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "description",
        "status",
        "created_at",
        "updated_at",
        "reporter",
    )
    # list_display_links = ("id", "title")
    # search_fields = ("title", "content")
    # list_editable = ("is_published",)
    # list_filter = ("is_published", "category")


admin.site.register(Ticket, TicketAdmin)
# admin.site.register(Status)
