from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Model for create category of catalog"""
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True,
                               related_name='children', verbose_name='Корневая категория')
    name = models.CharField(max_length=50, verbose_name='Категория')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория каталога'
        verbose_name_plural = 'Категории каталога'
