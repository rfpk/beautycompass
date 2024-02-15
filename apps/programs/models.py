from django.db import models
from django.urls import reverse

from apps.products.models import Product
from apps.profile.models import Profile


class Program(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название программы')
    is_publish = models.BooleanField(default=False, verbose_name='Опубликовать')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('programs:program_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Программа'
        verbose_name_plural = 'Программы'


class Complex(models.Model):
    """Class to create complex of products"""
    title = models.CharField(max_length=255, verbose_name='Название комплекса')
    recommendation = models.TextField(max_length=255, verbose_name='Описание рекомендаций', blank=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE,
                                related_name='program_complexes', verbose_name='Программа')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Комплекс'
        verbose_name_plural = 'Комплексы'


class ProgramResult(models.Model):
    description = models.CharField(max_length=255, null=True, verbose_name='Описание Программы')
    name = models.CharField(max_length=255, null=True, verbose_name='Название Программы')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                related_name='profile_program_result', verbose_name='Профиль')
    program = models.ForeignKey(Program, on_delete=models.CASCADE,
                                related_name='program_complexes_result', verbose_name='Программа')
    created_at = models.DateField(auto_now_add=True, blank=True, null=True, verbose_name='Время создания')

    class Meta:
        verbose_name = 'Результат Программы'
        verbose_name_plural = 'Результаты Программ'

    def __str__(self):
        return str(self.pk)


class ComplexResult(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название комплекса')
    recommendation = models.TextField(max_length=255, verbose_name='Описание рекомендаций', blank=True)
    program = models.ForeignKey(ProgramResult, on_delete=models.CASCADE,
                                related_name='program_complex_result', verbose_name='Программа')
    products = models.ManyToManyField(Product, related_name='complexes_result', verbose_name='Продукты')

    class Meta:
        verbose_name = 'Комплекс Результат Программы'
        verbose_name_plural = 'Комплексы Результатов Программ'

    def __str__(self):
        return self.title
