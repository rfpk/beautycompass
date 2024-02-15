from django.contrib import admin

from apps.services.models import Tariff, Plan, AdditionalService


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'period', 'quantity', 'status_start_plan')



@admin.register(Tariff)
class AppealAdmin(admin.ModelAdmin):
    list_display = ('id', 'price', 'type',)
    list_filter = ['price', 'type']

@admin.register(AdditionalService)
class AdditionalServiceAdmin(admin.ModelAdmin):
    pass

