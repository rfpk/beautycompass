from django.contrib import admin

from apps.programs.models import Program, Complex, ProgramResult, ComplexResult


class ComplexInline(admin.TabularInline):
    model = Complex
    extra = 3


@admin.register(Program)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_publish')
    list_filter = ['title', ]
    inlines = (ComplexInline, )


class ComplexResultInline(admin.TabularInline):
    model = ComplexResult
    extra = 3


@admin.register(ProgramResult)
class ProgramResult(admin.ModelAdmin):
    list_display = ('id', 'profile', 'program')
    list_filter = ('profile', 'program')
    inlines = (ComplexResultInline, )
