from django.db import models


class Plan(models.Model):
    """Class for plan tariff"""
    period = models.PositiveIntegerField(verbose_name='Период действия/месяц')
    quantity = models.PositiveIntegerField(verbose_name='Количество средств в каталоге')
    status_start_plan = models.BooleanField(verbose_name='План для стартового периода')

    def __str__(self):
        return f'Период: {self.period} месяца(-ев) | Лимит: {self.quantity} средств'

    class Meta:
        verbose_name = 'Тарифный план'
        verbose_name_plural = 'Тарифные планы'


class Tariff(models.Model):
    """Class tariff"""
    type = models.ForeignKey(Plan, on_delete=models.CASCADE, verbose_name='Тарифный план')
    price = models.DecimalField(decimal_places=3, max_digits=5,
                                verbose_name='Цена тарифа')

    def __str__(self):
        if self.type.status_start_plan:
            return f'Стартовый тариф: {self.type}  | Цена: {self.price} руб.'
        return f'Тариф: {self.type}  | Цена: {self.price} руб.'

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'

class AdditionalService(models.Model):
    title = models.CharField(max_length=300, verbose_name='Название услуги')
    description = models.TextField(verbose_name='Описание услуги')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Цена')
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Дополнительная услуга'
        verbose_name_plural = 'Дополнительные услуги'
