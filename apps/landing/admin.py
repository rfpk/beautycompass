from django.contrib import admin

from apps.landing.models import MainPage, MainBanner


@admin.register(MainPage)
class ContactPageAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(MainBanner)
class MainBannerAdmin(admin.ModelAdmin):
    pass
