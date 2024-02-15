from django.contrib import admin


from .models import ArticlePhoto, Article, ArticleComment, ArticleCommentPhoto, ArticleLink, Complaint


class ArticlePhotoInline(admin.TabularInline):
    model = ArticlePhoto
    extra = 0


class ArticleLinkInline(admin.TabularInline):
    model = ArticleLink
    extra = 5


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('manufacturer', 'title', 'date', 'is_publish')
    list_filter = ('manufacturer', 'tag__name', 'is_publish')
    inlines = [ArticlePhotoInline, ArticleLinkInline, ]
    prepopulated_fields = {'slug': ('title',)}


class ArticleCommentPhotoInline(admin.TabularInline):
    model = ArticleCommentPhoto
    extra = 0


@admin.register(ArticleComment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text',)
    inlines = [ArticleCommentPhotoInline, ]



@admin.register(Complaint)
class ComplaintActionAdmin(admin.ModelAdmin):
    list_display = ('profile', 'content_object', 'title')
    search_fields = ('title',)
    list_filter = ['profile__nickname',]
