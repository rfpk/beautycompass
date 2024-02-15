from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.files.utils import validate_file_name
from django.db import models
from django.utils.translation import gettext_lazy as _
from .image_operations import create_unique_name, remove_exif_data
from tinymce import models as tinymce_models

ADD = 1
REMOVE = 0
TYPE = [
    (REMOVE, 'Удаление'),
    (ADD, 'Добавление'),
]

# todo optimize
class CleanImageField(models.ImageField):

    def __init__(
        self,
        upload_to='',
        **kwargs,
    ):
        self.upload_folder = upload_to
        super(CleanImageField, self).__init__(upload_to=self.get_image_path, **kwargs)

    @staticmethod
    def get_image_path(_, filename, folder):
        return create_unique_name(filename, folder)

    def generate_filename(self, instance, filename):
        filename = self.upload_to(instance, filename, self.upload_folder)
        filename = validate_file_name(filename, allow_relative_path=True)
        return self.storage.generate_filename(filename)


class CleanImageFieldModel(models.Model):
    original_values = None

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = self._meta.get_fields()
        self.original_values = {}
        for field in fields:
            if field.__class__ == CleanImageField:
                self.original_values[field.name] = getattr(self, field.name)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        fields = self._meta.get_fields()
        for field in fields:
            if field.__class__ == CleanImageField:
                if not update_fields or field.name in update_fields:
                    file = getattr(self, field.name)
                    if self.original_values.get(field.name) != file:
                        setattr(self, field.name, remove_exif_data(file.file))

        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)



class CommonFields(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название', null=True, blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class ProfileAction(models.Model):
    """Class for save activity profile: set/reset likes, add in favorite"""
    type_action = models.PositiveIntegerField(choices=TYPE, verbose_name='Тип действия',
                                              default=1, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return str(self.pk)

    class Meta:
        abstract = True
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]


class TestData(models.Model):
    """Model for create test data"""
    title = models.CharField(max_length=255, blank=True, verbose_name='Название')
    is_publish = models.BooleanField(default=False, verbose_name='Опубликовать')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания',
                                      blank=True, null=True)
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return self.title

    class Meta:
        abstract = True

class QuestionData(models.Model):
    """Model for create question data"""
    class QuestionTypeChoices(models.TextChoices):
        ONE = 'ONE', _('Один подходящий ответ')
        MANY = 'MANY', _('Множественный выбор')
        BOOL = 'BOOL', _('Булевый тип ответа (да/нет)')
        TEXT = 'TEXT', _('Свободная форма ответа')

    type = models.CharField(choices=QuestionTypeChoices.choices, verbose_name='Тип ответа', max_length=15)
    text = models.TextField(verbose_name='Текст вопроса')
    description = models.TextField(verbose_name='Описание вопроса', blank=True, null=True)

    def __str__(self):
        return self.text

    class Meta:
        abstract = True
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

class OptionData(models.Model):
    """Model for create option data"""
    text = models.TextField(verbose_name='Вариант ответа', blank=True, null=True)
    description = models.TextField(verbose_name='Описание ответа', blank=True, null=True)

    def __str__(self):
        return self.text

    class Meta:
        abstract = True
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'

class AnswerData(models.Model):
    text_answer = models.TextField(verbose_name='Ответ', blank=True, null=True)

    class Meta:
        abstract = True
        verbose_name = 'Ответ пользователя'
        verbose_name_plural = 'Ответы пользователей'


class CommentData(models.Model):
    text = tinymce_models.HTMLField(blank=True, verbose_name='Текст')
    created_at = models.DateField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateField(auto_now=True, verbose_name='Время последнего редактирования')
    reaction = GenericRelation('profile.LikeAction')
    block_type = models.ForeignKey('settings.BlockComment', on_delete=models.SET_NULL,
                                   blank=True, null=True, verbose_name='Причина блокировки')

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.pk)

class Banner(models.Model):
    banner = CleanImageField(upload_to='products/banners/', verbose_name='Баннер')
    url = models.URLField(max_length=500, verbose_name='Ccылка на баннер')

    def __str__(self):
        return str(self.id)

    class Meta:
        abstract = True
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'


class AuthorAction(models.Model):
    type_action = models.PositiveIntegerField(choices=TYPE, verbose_name='Тип действия',
                                              default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        abstract = True


class Action(models.Model):
    like_action = GenericRelation('profile.LikeAction')
    favorite_action = GenericRelation('profile.FavoriteAction')
    views = GenericRelation('profile.ViewAction')

    class Meta:
        abstract = True

class Link(models.Model):
    name = models.CharField(verbose_name='Название источника', max_length=255)
    url = models.URLField(max_length=500, verbose_name='Ccылка на источник')

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class SocialLink(models.Model):
    social_web = models.ForeignKey('settings.SocialWeb', on_delete=models.CASCADE, verbose_name='Социальная сеть')
    url = models.URLField(max_length=500, verbose_name='Ccылка на социальную сеть')

    class Meta:
        abstract = True
        verbose_name = 'Ссылка на социальную сеть'
        verbose_name_plural = 'Ссылки на социальные сети'

    def __str__(self):
        return str(self.pk)


class ComplaintAction(models.Model):
    title = models.CharField(max_length=255, blank=True, verbose_name='Тема жалобы')
    text = models.TextField(verbose_name='Описание причины')
    content_type = models.ForeignKey(ContentType, null=True, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    def __str__(self):
        return self.title

    class Meta:
        abstract = True
        ordering = ['id']
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]