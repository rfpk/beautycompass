from django.contrib import admin

from apps.catalog.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('parent', 'name',)
    list_filter = ('parent', )
    prepopulated_fields = {'slug': ('name',)}
