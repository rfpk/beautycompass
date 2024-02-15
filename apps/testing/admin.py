from django.contrib import admin

from apps.testing.models import Test, QuestionTest, Option, AnswerProfile, ImageOption, TestsResult

class QuestionTestInline(admin.TabularInline):
    model = QuestionTest
    extra = 1

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_filter = ['title', ]
    inlines = (QuestionTestInline,)

class ImageOptionInline(admin.TabularInline):
    model = ImageOption
    extra = 1

class OptionInline(admin.TabularInline):
    model = Option
    extra = 1
    inlines = (ImageOptionInline, )


@admin.register(Option)
class ChoiceAdmin(admin.ModelAdmin):
    inlines = (ImageOptionInline, )


@admin.register(QuestionTest)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('test', 'type', 'text', )
    search_fields = ('text',)
    list_filter = ['type', 'test__title']
    inlines = (OptionInline, )


@admin.register(AnswerProfile)
class AnswerProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'question')
    list_filter = ['profile__email', 'question__test__title']


@admin.register(TestsResult)
class TestResult(admin.ModelAdmin):
    list_display = ('name', 'profile', 'created_at', 'slug')
    list_filter = ('name', 'profile__email', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
