from django.db import models
from django.urls import reverse
from tinymce import models as tinymce_models

from apps.profile.mixins import StatisticMixin
from apps.profile.models import Profile, Author

from apps.tools.database_operations import CleanImageField, CommentData, Action


class Chat(models.Model):
    """Class for create chat room"""
    participants = models.ManyToManyField(Profile, related_name='profile_chats', verbose_name='Участники чата')
    title = models.CharField(max_length=255, blank=True, verbose_name='Название чата')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'

class Message(models.Model):
    """Class for create message user"""
    title = models.CharField(max_length=300, blank=True, verbose_name='Тема сообщения')
    text = models.TextField(verbose_name='Текст')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправления')
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender_messages',
                               blank=True, null=True, verbose_name='Отправитель')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver_messages',
                                 blank=True, null=True, verbose_name='Получатель')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat_messages', verbose_name='Чат')

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class ConversationPost(Action, StatisticMixin):
    title = models.CharField(max_length=300, blank=True, verbose_name='Заголовок поста')
    profile = models.ForeignKey('profile.Profile', on_delete=models.CASCADE, related_name='profile_conversation_posts',
                                verbose_name='Профиль')
    text = tinymce_models.HTMLField(blank=True, verbose_name='Текст')
    tag = models.ManyToManyField('products.Tag', verbose_name='Теги',
                                 blank=True, related_name='conversation_tags')
    created_at = models.DateField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateField(auto_now=True, verbose_name='Время последнего редактирования')
    is_publish = models.BooleanField(default=True, verbose_name='Опубликован')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Пост беседки'
        verbose_name_plural = 'Посты беседки'
        ordering = ('-created_at', )

    def get_absolute_url(self):
        return reverse('chats:detail_conversation', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class ImagePost(models.Model):
    comment = models.ForeignKey(ConversationPost, on_delete=models.CASCADE,
                                related_name='post_conversation_images', verbose_name='Пост')
    image = CleanImageField(upload_to='conversation/photos/', verbose_name='Фотография')
    status_watermark = models.BooleanField(default=False, verbose_name='Необходим копирайт')


class CommentConversation(CommentData):
    post = models.ForeignKey(ConversationPost, on_delete=models.CASCADE, related_name='comments',
                             verbose_name='Пост')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE,
                               related_name='answers', verbose_name='Корневой комментарий')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, related_name='author_conversations_comments',
                               verbose_name='Автор комментария')
    is_publish = models.BooleanField(default=True, verbose_name='Опубликован')

    class Meta:
        verbose_name = 'Комметарий'
        verbose_name_plural = 'Комметарии'
        ordering = ('-created_at', )


class ImageComment(models.Model):
    comment = models.ForeignKey(CommentConversation, on_delete=models.CASCADE,
                                related_name='comment_conversation_images', verbose_name='Комметрарий')
    image = CleanImageField(upload_to='conversation/photos/', verbose_name='Фотография')
