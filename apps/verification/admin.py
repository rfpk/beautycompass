from django.contrib import admin
from .models import RegistrationLink
from apps.tools.forms import HiddenPasswordForm


@admin.register(RegistrationLink)
class RegistrationLinkAdmin(admin.ModelAdmin):
    form = HiddenPasswordForm
    list_display = (
        "id",
        "email",
        "nickname",
        "profile",
        "url",
        "is_used",
        "created_at",
    )
    list_filter = ("is_used",)
    raw_id_fields = ("profile",)
    search_fields = (
        "profile__id",
        "profile__email",
        "profile__user__username",
    )
