from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Max, F
from django.utils.translation import gettext_lazy as _
from .models import User, Profile, Question, Appeal, AppealImage, LikeAction, FavoriteAction, Author, \
    AuthorHistory, Overview, \
    OverviewPhoto, OverviewComment, ViewAction, Conversion, GratitudeAction, SubscribeAction
from ..manufacturers.models import ManufacturerQuestionAnswer


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "is_staff")
    search_fields = ("username", )
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('email', 'nickname', 'phone', 'is_active')
    list_filter = ['nickname', 'is_active', 'sex']
    search_fields = ('email', 'nickname', 'phone', 'first_name', 'last_name', )


class AnswerInline(admin.TabularInline):
    model = ManufacturerQuestionAnswer
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'product', 'get_manufacturer', 'date')
    list_filter = ['profile__nickname', 'product', 'product__series__brand__manufacturer']
    search_fields = ('product', 'profile', )
    inlines = (AnswerInline, )

    def get_manufacturer(self, obj):
        return obj.product.series.brand.manufacturer
    get_manufacturer.short_description = 'Производитель'



class AppealImageInline(admin.TabularInline):
    model = AppealImage
    extra = 5


@admin.register(Appeal)
class AppealAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'title', 'subject_appeal')
    search_fields = ('profile__nickname', )
    list_filter = ['subject_appeal', 'profile__nickname']
    inlines = (AppealImageInline, )


@admin.register(LikeAction)
class ProfileActionAdmin(admin.ModelAdmin):
    list_display = ('profile', 'type_action', 'created_at', 'content_object')
    search_fields = ('profile__email',)
    list_filter = ['profile__email', 'type_action']

@admin.register(GratitudeAction)
class GratitudeActionAdmin(admin.ModelAdmin):
    list_display = ('author', 'author_action', 'type_action', 'created_at')

@admin.register(SubscribeAction)
class SubscribeActionAdmin(admin.ModelAdmin):
    list_display = ('author', 'author_action', 'type_action', 'created_at')

@admin.register(FavoriteAction)
class ProfileActionAdmin(admin.ModelAdmin):
    list_display = ('profile', 'type_action', 'created_at', 'content_object')
    search_fields = ('profile__email',)
    list_filter = ['profile__email', 'type_action']

@admin.register(ViewAction)
class ViewActionAdmin(admin.ModelAdmin):
    list_display = ('profile', 'type_action', 'created_at', 'content_object')

@admin.register(Conversion)
class ConversionAdmin(admin.ModelAdmin):
    list_display = ('profile', 'type_action', 'created_at', 'content_object')



class AuthorHistorySatus(admin.TabularInline):
    model = AuthorHistory
    extra = 1

class StatusFilter(admin.SimpleListFilter):
    title = 'Текущий статус пользователя'
    parameter_name = 'current_status'

    def lookups(self, request, model_admin):
        author_histories = AuthorHistory.AuthorStatus.choices
        return [obj for obj in author_histories]

    def queryset(self, request, queryset):
        if self.value():
            return Author.objects.annotate(latest_history=Max('history__created_at')).filter(
                history__current_status=self.value(), history__created_at=F('latest_history'))
        else:
            return queryset


@admin.register(Author)
class AppealAdmin(admin.ModelAdmin):
    list_display = ('profile', 'type', 'rating', 'get_current_status')
    list_filter = ['profile__nickname', 'type', StatusFilter]
    inlines = (AuthorHistorySatus,)

    def get_current_status(self, obj):
        status = obj.history.last()
        if status:
            return status.get_current_status_display()
        return None
    get_current_status.short_description = 'Текущий статус'


class OverviewPhotosInLine(admin.TabularInline):
    model = OverviewPhoto
    extra = 1

@admin.register(OverviewComment)
class OverviewCommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Overview)
class OverviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'is_publish')
    search_fields = ('author__profile__nickname', 'title')
    list_filter = ['author__profile__nickname', 'is_publish']
    inlines = (OverviewPhotosInLine,)
    prepopulated_fields = {'slug': ('title',)}

