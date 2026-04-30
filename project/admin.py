from django.contrib import admin
from .models import Artist, Client, CommissionPackage, CommissionRequest


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ("display_name", "email", "is_open_for_commissions", "created_at")
    search_fields = ("display_name", "email")
    list_filter = ("is_open_for_commissions",)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "created_at")
    search_fields = ("first_name", "last_name", "email")


@admin.register(CommissionPackage)
class CommissionPackageAdmin(admin.ModelAdmin):
    list_display = ("title", "artist", "base_price", "turnaround_days", "is_active")
    search_fields = ("title", "artist__display_name")
    list_filter = ("is_active",)


@admin.register(CommissionRequest)
class CommissionRequestAdmin(admin.ModelAdmin):
    list_display = ("request_title", "client", "package", "status", "deadline", "created_at")
    search_fields = ("request_title", "client__first_name", "client__last_name")
    list_filter = ("status",)