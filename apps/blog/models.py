from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils import timezone

from apps.profile.mixins import StatisticMixin
from apps.tools.database_operations import CleanImageFieldModel, CleanImageField, Action, CommentData, ComplaintAction


class Article(CleanImageFieldModel, Action, StatisticMixin):
    manufacturer = models.ForeignKey('manufacturers.Manufacturer', on_delete=models.CASCADE,
                                     related_name='manufacturer_articles', verbose_name='Производитель')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField('Текст')
    thumbnail = CleanImageField(upload_to='articles/thumbnails/', verbose_name='Главная фотография',
                                blank=True, null=True)
    brand = models.ForeignKey('products.Brand', on_delete=models.CASCADE, related_name='brand_articles',
                              verbose_name='Бренд',
                              blank=True, null=True)
    date = models.DateTimeField(auto_now=True, verbose_name='Дата')
    is_publish = models.BooleanField(default=False, verbose_name='Опубликована')
    is_draft = models.BooleanField(default=False, verbose_name='Черновик')
    is_active = models.BooleanField(default=False, verbose_name='Активна')
    created_at = models.DateTimeField(editable=False, default=timezone.now)
    slug = models.SlugField(unique=True)
    conversion = GenericRelation('profile.Conversion')
    tag = models.ManyToManyField('products.Tag', verbose_name='Теги', blank=True, related_name='articles_tags')
    total_rating = models.PositiveIntegerField(default=0, verbose_name='Общий рейтинг')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ('date', )
        
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:article_detail', kwargs={'slug': self.slug})

    def check_conversion(self, request, following_model, following_slug):
        from apps.tools.utils import conversion_checking
        conversion_checking(self, request, following_model, following_slug)

class ArticleLink(models.Model):
    """Model for storing links to tool pages"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE,
                                related_name='article_links', verbose_name='Ссылка на продукт')
    url = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = 'Ссылка на продукт'
        verbose_name_plural = 'Ссылки на продукты'

    def __str__(self):
        return str(self.pk)

class ArticlePhoto(CleanImageFieldModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='photos', verbose_name='Статья')
    photo = CleanImageField(upload_to='articles/photos/', verbose_name='Фотография')
    status_watermark = models.BooleanField(default=False, verbose_name='Необходим копирайт')

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'

    def __str__(self):
        return str(self.id)


class ArticleComment(CommentData):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', verbose_name='Статья')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE,
                               related_name='answers', verbose_name='Корневой комментарий')
    author = models.ForeignKey('profile.Author', on_delete=models.CASCADE, null=True, related_name='author_articles_comments',
                               verbose_name='Автор комментария')
    is_publish = models.BooleanField(default=True, verbose_name='Опубликован')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-created_at', )

    def get_absolute_url(self):
        return reverse('blog:article_detail', kwargs={'slug': self.article.slug})


class ArticleCommentPhoto(CleanImageFieldModel):
    comment = models.ForeignKey(ArticleComment, on_delete=models.CASCADE, related_name='photos', verbose_name='Комментарий')
    photo = CleanImageField(upload_to='comments/photos/', verbose_name='Фотография')

    class Meta:
        verbose_name = 'Фотография комментария'
        verbose_name_plural = 'Фотографии комментария'

    def __str__(self):
        return str(self.id)

    @property
    def comment_text(self):
        return self.comment.text


class Complaint(ComplaintAction):
    """Class for create complaints on articles"""
    profile = models.ForeignKey('profile.Profile', on_delete=models.CASCADE,
                                related_name='profile_complaints_actions', verbose_name='Профиль')

    class Meta:
        verbose_name = 'Жалоба'
        verbose_name_plural = 'Жалобы'
