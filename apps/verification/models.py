from django.db import models
from django.db.models import Max
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from apps.profile.models import Profile


class Link(models.Model):
    url = models.CharField(max_length=500)
    count = models.PositiveIntegerField(default=0)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=False, default=timezone.now)

    class Meta:
        abstract = True

    def __str__(self):
        return self.url

    @classmethod
    def max_count(cls, lid):
        return (
            cls.objects.filter(profile=lid, is_used=True).aggregate(Max("count"))[
                "count__max"
            ]
            or 0
        )


class RegistrationLink(Link):
    email = models.EmailField("email")
    password = models.CharField("password", max_length=128)
    phone = PhoneNumberField(blank=True, null=True)
    nickname = models.CharField(max_length=15, blank=True)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    profile = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        related_name="profile_registration_links",
        blank=True,
        null=True,
    )

    @classmethod
    def max_count(cls, lid):
        return (
            cls.objects.filter(email=lid, is_used=True).aggregate(Max("count"))[
                "count__max"
            ]
            or 0
        )


class PasswordResetLink(Link):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="profile_password_reset_links"
    )
