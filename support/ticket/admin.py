from django.contrib import admin

from .models import Ticket


class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "description",
        "status",
        "created_at",
        "updated_at",
        "reporter",
    )


admin.site.register(Ticket, TicketAdmin)
