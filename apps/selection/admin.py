from django.contrib import admin

from apps.selection.models import QuestionSelection, Selection, OptionSelection, AnswerSelectionProfile


class QuestionSelectionInline(admin.TabularInline):
    model = QuestionSelection
    extra = 1

@admin.register(Selection)
class TestAdmin(admin.ModelAdmin):
    list_filter = ['title', ]
    inlines = (QuestionSelectionInline,)

class OptionSelectionInline(admin.TabularInline):
    model = OptionSelection
    extra = 1



@admin.register(QuestionSelection)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('selection', 'type', 'text', )
    search_fields = ('text',)
    list_filter = ['type', 'selection__title']
    inlines = (OptionSelectionInline, )


@admin.register(AnswerSelectionProfile)
class AnswerSelectionProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'question')
    list_filter = ['profile__email', 'question__selection__title']
