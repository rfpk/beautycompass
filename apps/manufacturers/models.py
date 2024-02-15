from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from apps.products.mixins import ViewMixin
from apps.products.models import Tag, Brand
from tinymce import models as tinymce_models
from apps.products.models import Tag
from apps.profile.mixins import StatisticViewMixin
from apps.profile.models import Profile
from apps.services.models import Tariff
from apps.settings.models import Country
from apps.tools.database_operations import CleanImageField, Banner, CommentData, Link, SocialLink
from datetime import date


class Manufacturer(models.Model):
    """Class for manufacturer profile"""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Профиль', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, verbose_name='Название компании')
    logo = CleanImageField(upload_to='manufacturer/logos/', verbose_name='Логотип компании', blank=True, null=True)
    email = models.EmailField(unique=True, blank=True)
    phone = PhoneNumberField(blank=True, verbose_name='Телефон')
    description = tinymce_models.HTMLField(blank=True, verbose_name='Краткое описание компании')
    history = tinymce_models.HTMLField(blank=True, verbose_name='История компании')
    principle = tinymce_models.HTMLField(blank=True, verbose_name='Принципы компании')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='country_manufacturers',
                                verbose_name='Страна', blank=True, null=True)
    city = models.CharField(verbose_name='Город', max_length=255, blank=True)
    tag = models.ManyToManyField(Tag, verbose_name='Теги',
                                 blank=True, related_name='manufacturer_tags')

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return self.name

    @property
    def get_day_end_period(self):
        """
        get day value for end period current tariff plan
        """
        last_tariff = self.manufacturer_tariffs.last()
        if last_tariff:
            return abs((last_tariff.end_date - date.today()).days)

    def save(self, *args, **kwargs):
        new = False
        if not self.id:
            new = True
        super().save(*args, **kwargs)
        if new:
            starter_pack_tariff = Tariff.objects.filter(type__status_start_plan=True).first()
            if starter_pack_tariff:
                ManufacturerTariffHistory.objects.create(manufacturer=self,
                                                         tariff_plan=starter_pack_tariff)


class ManufacturerBanner(Banner, ViewMixin, StatisticViewMixin):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name='manufacturer_banners',
                                     verbose_name='Производитель')
    views = GenericRelation('profile.ViewAction')

    def set_action_banner(self, request):
        self.check_view_user(request, self)


class ManufacturerLinkShop(Link, ViewMixin):
    """Class for create link on other shops manufacturer"""
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name='manufacturer_links',
                                     verbose_name='Производитель')
    link_actions = GenericRelation('profile.ViewAction')

    def set_action_link(self, request):
        self.check_view_user(request, self)

    class Meta:
        verbose_name = 'Ссылка на магазины производителя'
        verbose_name_plural = 'Ссылки на магазины производителей'


class ManufacturerSocialLink(SocialLink):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE,
                                     related_name='manufacturer_social_links', verbose_name='Производитель')


class ManufacturerMailing(models.Model):
    """Class for creating manufacturer mailing"""
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE,
                                     related_name='manufacturer_mails', verbose_name='Производитель')
    company_name = models.CharField(max_length=255, verbose_name='Название компании')
    email = models.EmailField(verbose_name='E-mail')
    phone = PhoneNumberField(verbose_name='Телефон')
    text = tinymce_models.HTMLField(verbose_name='Текст рассылки')
    image = CleanImageField(upload_to='mailing/images/', verbose_name='Изображение', blank=True, null=True)
    banner = CleanImageField(upload_to='mailing/banners/', verbose_name='Баннер', blank=True, null=True)
    background_image = CleanImageField(upload_to='mailing/backgrounds/', verbose_name='Фон', blank=True, null=True)
    link_banner = models.URLField(verbose_name='Ссылка к баннеру', blank=True, null=True)
    receiver_profile = models.ManyToManyField(Profile, verbose_name='Получатели',
                                              related_name='profile_mails', blank=True)
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата рассылки')

    def __str__(self):
        return f'Рассылка от производителя {self.manufacturer}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

class AnswerReview(CommentData):
    review = models.ForeignKey('products.Review', on_delete=models.CASCADE,
                               related_name='review_answers', verbose_name='Отызыв')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE,
                                     related_name='manufacturer_reviews_answers', verbose_name='Производитель')
    is_publish = models.BooleanField(default=True, verbose_name='Опубликован')

    class Meta:
        verbose_name = 'Ответ производителя на отзыв'
        verbose_name_plural = 'Ответы производителей на отзывы'


class ManufacturerTariffHistory(models.Model):
    """
    Save information about tariff services profile
    """
    manufacturer = models.ForeignKey('manufacturers.Manufacturer', on_delete=models.CASCADE,
                                     related_name='manufacturer_tariffs',
                                     verbose_name='Производитель')
    tariff_plan = models.ForeignKey('services.Tariff', verbose_name='Тарифный план', on_delete=models.CASCADE,
                                    related_name='tariff_manufacturers')
    start_date = models.DateField(auto_now_add=True, verbose_name='Начало действия')
    end_date = models.DateField(verbose_name='Окончание действия', null=True, blank=True)

    class Meta:
        verbose_name = 'История тарифного плана'
        verbose_name_plural = 'История тарифных планов'


class ManufacturerServiceHistory(models.Model):
    """
    Save information about addition services profile
    """
    service = models.ForeignKey('services.AdditionalService', on_delete=models.CASCADE,
                                related_name='service_manufacturers', verbose_name='Дополнительная услуга')
    manufacturer = models.ForeignKey('manufacturers.Manufacturer', on_delete=models.CASCADE,
                                     related_name='manufacturer_services',
                                     verbose_name='Производитель')
    start_date = models.DateField(auto_now_add=True, verbose_name='Начало действия')
    end_date = models.DateField(verbose_name='Окончание действия', null=True, blank=True)

    class Meta:
        verbose_name = 'История дополнительной услуги'
        verbose_name_plural = 'История дополнительных услуг'


class ManufacturerQuestionAnswer(models.Model):
    """Model for answer manufacturer on user question"""
    manufacturer = models.ForeignKey('manufacturers.Manufacturer', related_name="manufacturer_answers",
                                     on_delete=models.CASCADE, verbose_name='Профиль отвечающего')
    question = models.ForeignKey('profile.Question', related_name="question_answers",
                                 on_delete=models.CASCADE, verbose_name='Вопрос')
    text = models.TextField(verbose_name='Текст ответа')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата ответа')
    updated_at = models.DateField(auto_now=True, verbose_name='Время последнего редактирования')

    class Meta:
        verbose_name = 'Ответ производителя на вопрос'
        verbose_name_plural = 'Ответы производителей на вопросы'

    def __str__(self):
        return str(self.pk)
