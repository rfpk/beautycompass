from django.contrib import admin

from apps.chats.models import Chat, Message, ConversationPost, CommentConversation, ImageComment, ImagePost
from apps.profile.models import Profile


class ChatParticipantsFilter(admin.SimpleListFilter):
    title = 'Участники чата'
    parameter_name = 'participants'

    def lookups(self, request, model_admin):
        profiles = Profile.objects.all()
        return [(profile.id, profile.nickname) for profile in profiles]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(participants__id=self.value())
        else:
            return queryset


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_participants', 'title', 'created', )
    list_filter = (ChatParticipantsFilter,)

    def get_participants(self, obj):
        return "\n".join([profile.nickname for profile in obj.participants.all()])

    get_participants.short_description = "Участники чата"


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('chat', 'sender', 'receiver', 'date')
    list_filter = ('chat__title', 'sender', 'receiver')

class ImagePostInline(admin.TabularInline):
    model = ImagePost
    extra = 1

@admin.register(ConversationPost)
class ConversationPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'profile', 'created_at', 'updated_at', 'is_publish')
    list_filter = ['profile__nickname', 'is_publish', ]
    prepopulated_fields = {"slug": ("title",)}
    inlines = (ImagePostInline, )

class ImageCommentInline(admin.TabularInline):
    model = ImageComment
    extra = 1

@admin.register(CommentConversation)
class CommentConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'created_at', 'updated_at', 'is_publish')
    list_filter = ['post__title', 'author__profile__nickname', ]
    inlines = (ImageCommentInline, )
