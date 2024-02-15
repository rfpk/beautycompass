from datetime import date

from django.contrib import admin
from django.db.models import Max, F

from apps.manufacturers.models import Manufacturer, ManufacturerLinkShop, ManufacturerMailing, ManufacturerBanner, \
    ManufacturerServiceHistory, ManufacturerTariffHistory, ManufacturerQuestionAnswer, \
    ManufacturerSocialLink, AnswerReview
from apps.products.admin import TagsFilter


class ManufacturerServiceHistoryInline(admin.TabularInline):
    model = ManufacturerServiceHistory
    extra = 1
    readonly_fields = ['start_date']
    fields = ['service', 'start_date', 'end_date']

class ManufacturerTariffHistoryInline(admin.TabularInline):
    model = ManufacturerTariffHistory
    extra = 1
    readonly_fields = ['start_date']
    fields = ['tariff_plan', 'start_date', 'end_date']

class ManufacturerLinkShopInline(admin.TabularInline):
    model = ManufacturerLinkShop
    extra = 3

class ManufacturerSocialLinkInline(admin.TabularInline):
    model = ManufacturerSocialLink
    extra = 3


class ManufacturerBannerInline(admin.TabularInline):
    model = ManufacturerBanner
    extra = 5


class TariffFilter(admin.SimpleListFilter):
    title = 'Текущий тариф производителя'
    parameter_name = 'tariff_plan'

    def lookups(self, request, model_admin):
        return [
            ('Действующий стартовый тариф', 'Действующий стартовый тариф'),
            ('Действующий купленный тариф','Действующий купленный тариф'),
            ('Истекший тариф', 'Истекший тариф')
        ]

    def queryset(self, request, queryset):
        if self.value():
            if self.value() == 'Действующий стартовый тариф':
                return Manufacturer.objects.annotate(latest_tariff=Max('manufacturer_tariffs__start_date')).filter(
                    manufacturer_tariffs__tariff_plan__type__status_start_plan=True,
                    manufacturer_tariffs__start_date=F('latest_tariff'),
                    manufacturer_tariffs__end_date__gte=date.today())

            elif self.value() == 'Действующий купленный тариф':
                return Manufacturer.objects.annotate(latest_tariff=Max('manufacturer_tariffs__start_date')).filter(
                    manufacturer_tariffs__tariff_plan__type__status_start_plan=False,
                    manufacturer_tariffs__start_date=F('latest_tariff'))
            else:
                return Manufacturer.objects.annotate(latest_tariff=Max('manufacturer_tariffs__start_date')).filter(
                    manufacturer_tariffs__start_date=F('latest_tariff'),
                    manufacturer_tariffs__end_date__lt=date.today()
                )
        else:
            return queryset

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('profile', 'name', 'email', 'end_date_current_tariff')
    search_fields = ('name', 'email', 'phone', 'country', 'city',)
    list_filter = (TagsFilter, TariffFilter, )
    inlines = (ManufacturerSocialLinkInline, ManufacturerLinkShopInline, ManufacturerBannerInline,
               ManufacturerTariffHistoryInline, ManufacturerServiceHistoryInline)

    def end_date_current_tariff(self, obj):
        last_obj = obj.manufacturer_tariffs.last()
        if last_obj:
            return last_obj.end_date
        return f'Нет истории тарифов'

    end_date_current_tariff.short_description = 'Дата истечения текущего тарифа'


@admin.register(ManufacturerQuestionAnswer)
class ManufacturerQuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'manufacturer', 'date', 'updated_at')
    list_filter = ['manufacturer', ]
    search_fields = ('manufacturer', )


@admin.register(AnswerReview)
class ManufacturerReviewAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'review', 'manufacturer', 'created_at')
    list_filter = ['review', 'manufacturer']
    search_fields = ('review', 'manufacturer',)


@admin.register(ManufacturerMailing)
class ManufacturerMailingAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'company_name', 'created_at')
    search_fields = ('company_name', 'email', 'phone', )
    list_filter = ['manufacturer__name', ]

