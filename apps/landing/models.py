from django.db import models
from tinymce import models as tinymce_models

from apps.tools.database_operations import CleanImageField, Banner


class MainPage(models.Model):
    """Class for save information about main pages"""
    title = models.CharField(max_length=255, blank=True, verbose_name='Заголовок страницы')
    content = tinymce_models.HTMLField(blank=True, verbose_name='Содержимое страницы')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Основная страница'
        verbose_name_plural = 'Основные страницы'


class MainBanner(models.Model):
    banner = CleanImageField(upload_to='landing/banners/', verbose_name='Баннер')
    banner_selection = models.BooleanField(default=False, verbose_name='Баннер для блока подбора косметики')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры на главной странице'
