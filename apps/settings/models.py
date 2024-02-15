from django.db import models
from django_countries.fields import CountryField

from apps.tools.database_operations import CleanImageField


class Country(models.Model):
    country = CountryField('Country')
    label = models.CharField('label', max_length=255, blank=True, null=True)
    order = models.IntegerField('Order', default=0)
    enabled = models.BooleanField(default=False)

    class Meta:
        ordering = ('order', 'label', )

    def __str__(self):
        return self.label


class HairType(models.Model):
    label = models.CharField(max_length=255, unique=True)
    
    class Meta:
        verbose_name = 'Тип волос'
        verbose_name_plural = 'Типы волос'
    
    def __str__(self):
        return self.label


class SkinType(models.Model):
    label = models.CharField(max_length=255, unique=True)
    
    class Meta:
        verbose_name = 'Тип кожи'
        verbose_name_plural = 'Типы кожи'
    
    def __str__(self):
        return self.label


class BlockComment(models.Model):
    reasons = models.CharField(max_length=300, verbose_name='Причина блокировки')

    class Meta:
        verbose_name = 'Тип блокировки комментария'
        verbose_name_plural = 'Типы блокировок комментариев'

    def __str__(self):
        return self.reasons


class SocialWeb(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    logo = models.FileField(upload_to='social/logo/', verbose_name='Лого')

    class Meta:
        verbose_name = 'Социальная сеть'
        verbose_name_plural = 'Социальные сети'

    def __str__(self):
        return self.name
