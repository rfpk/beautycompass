from django.contrib import admin

from apps.settings.models import BlockComment, SocialWeb, HairType, SkinType


@admin.register(BlockComment)
class BlockCommentAdmin(admin.ModelAdmin):
    pass

@admin.register(SocialWeb)
class SocialWebAdmin(admin.ModelAdmin):
    pass

@admin.register(HairType)
class HairTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(SkinType)
class HairTypeAdmin(admin.ModelAdmin):
    pass