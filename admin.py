from django.contrib import admin
from .models import Websites

# Register your models here.
@admin.register(Websites)
class WebsitesAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "route_name",
        "url",
        "is_active",
        "show_in_random",
        "search_enabled",
        "search_order",
        "created_at",
    )

    list_filter = (
        "is_active",
        "show_in_random",
        "search_enabled",
        "created_at",
    )

    search_fields = (
        "name",
        "url",
        "route_name",
    )

    ordering = ["-created_at"]