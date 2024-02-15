import logging

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.shortcuts import redirect
from django.urls import reverse

from apps.products.mixins import ViewMixin
from tinymce import models as tinymce_models

from apps.profile.mixins import StatisticMixin, StatisticViewMixin
from apps.settings.models import Country
from apps.tools.database_operations import CleanImageFieldModel, CleanImageField, CommonFields, Banner, Action, \
    CommentData, Link, SocialLink, AuthorAction
from apps.catalog.models import Category

logger = logging.getLogger("profile")


class Tag(CommonFields):
    """Class for create tags"""

    def get_absolute_url(self):
        return reverse('products:tag_products', kwargs={'tag_slug': self.slug})

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Brand(CleanImageFieldModel):
    name = models.CharField(max_length=100, verbose_name='Название бренда')
    image = CleanImageField(upload_to='brands/images/', verbose_name='Картинка', blank=True, null=True)
    description = tinymce_models.HTMLField(verbose_name='Описание бренда', blank=True, null=True)
    short_description = tinymce_models.HTMLField(verbose_name='Короткое писание бренда', blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='brands', verbose_name='Страна',
                                blank=True, null=True)
    favorite_action = GenericRelation('profile.FavoriteAction')
    conversion = GenericRelation('profile.Conversion')
    views = GenericRelation('profile.ViewAction')
    manufacturer = models.ForeignKey('manufacturers.Manufacturer', on_delete=models.SET_NULL,
                                     related_name='manufacturer_brands', verbose_name='Производитель',
                                     blank=True, null=True)

    tag = models.ManyToManyField(Tag, verbose_name='Теги',
                                 blank=True, related_name='brand_tags')

    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:brand_detail', kwargs={'slug': self.slug})

    def get_brand_article(self):
        return reverse('products:brand_articles', kwargs={'slug': self.slug})

    def check_conversion(self, request, following_model, following_slug):
        from apps.tools.utils import conversion_checking
        conversion_checking(self, request, following_model, following_slug)

class BrandSubscriber(AuthorAction):
    brand = models.ForeignKey('products.Brand', on_delete=models.CASCADE, related_name='brand_subscribers',
                              verbose_name='Бренд')
    profile = models.ForeignKey('profile.Profile', on_delete=models.CASCADE, related_name='subscribe_brands',
                                verbose_name='Профиль')

    class Meta:
        verbose_name = 'История подписки на бренд'
        verbose_name_plural = 'История подписок на бренд'


class BrandBanner(Banner, ViewMixin, StatisticViewMixin):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand_banners',
                              verbose_name='Бренд')
    views = GenericRelation('profile.ViewAction')

    def set_action_banner(self, request):
        self.check_view_user(request, self)


class BrandLink(Link, ViewMixin):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE,
                              related_name='brand_links', verbose_name='Бренд')
    link_conversion = GenericRelation('profile.ViewAction')

    def set_action_link(self, request):
        self.check_view_user(request, self)

    class Meta:
        verbose_name = 'Ссылка магазины бренда'
        verbose_name_plural = 'Ссылки на магазины брендов'


class BrandSocialLink(SocialLink):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE,
                              related_name='brand_social_links', verbose_name='Бренд')


class Series(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='series', verbose_name='Бренд')
    logo = CleanImageField(upload_to='series/images/', verbose_name='Картинка', blank=True, null=True)
    name = models.CharField(max_length=100, verbose_name='Название cерии')
    description = models.TextField(blank=True, null=True, verbose_name='Краткое описание')
    favorite_action = GenericRelation('profile.FavoriteAction')
    conversion = GenericRelation('profile.Conversion')

    tag = models.ManyToManyField(Tag, verbose_name='Теги',
                                 blank=True, related_name='series_tags')

    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Серия'
        verbose_name_plural = 'Серии'

    def get_absolute_url(self):
        return redirect('products:series_detail', self.slug)

    def check_conversion(self, request, following_model, following_slug):
        from apps.tools.utils import conversion_checking
        conversion_checking(self, request, following_model, following_slug)


class SeriesBanner(Banner, ViewMixin, StatisticViewMixin):
    series = models.ForeignKey(Series, on_delete=models.CASCADE, related_name='series_banners',
                               verbose_name='Cерия')
    views = GenericRelation('profile.ViewAction')

    def set_action_banner(self, request):
        self.check_view_user(request, self)


class SeriesImage(CleanImageFieldModel):
    series = models.ForeignKey(Series, on_delete=models.CASCADE, related_name='seria_images', verbose_name='Серия')
    image = CleanImageField(upload_to='products/images/', verbose_name='Картинка')

    class Meta:
        verbose_name = 'Картинка серии'
        verbose_name_plural = 'Картинки серий'

    def __str__(self):
        return str(self.id)


class PriceCategory(CommonFields):
    """Class for create price categories"""

    class Meta:
        verbose_name = 'Ценовая категория'
        verbose_name_plural = 'Ценовые категории'


class Prescription(CommonFields):
    """Class for create prescriptions of products"""

    class Meta:
        verbose_name = 'Назначение средства'
        verbose_name_plural = 'Назначения средств'


class KeyAction(CommonFields):
    """Class for create key actions of products"""

    class Meta:
        verbose_name = 'Ключевое действие'
        verbose_name_plural = 'Ключевые действия'


class KeyAsset(CommonFields):
    """Class for create key assets of products"""

    class Meta:
        verbose_name = 'Ключевый актив'
        verbose_name_plural = 'Ключевые активы'


class Sex(CommonFields):
    """Class for create sex categories of products"""

    class Meta:
        verbose_name = 'Пол'
        verbose_name_plural = 'Пол'


class AgeRecommendation(CommonFields):
    """Class for create age recommendations of products"""

    class Meta:
        verbose_name = 'Возрастная рекомендация'
        verbose_name_plural = 'Возрастные рекомендации'

class Format(CommonFields):
    """Class for create formats of products"""

    class Meta:
        verbose_name = 'Формат'
        verbose_name_plural = 'Форматы'

class Product(CleanImageFieldModel, Action, StatisticMixin):
    name = models.CharField(max_length=100, verbose_name='Название продукта')
    series = models.ForeignKey(Series, on_delete=models.CASCADE, blank=True, null=True,
                               related_name='products', verbose_name='Серия')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand_products', verbose_name='Бренд')
    price_category = models.ForeignKey(PriceCategory, on_delete=models.CASCADE, related_name='price_category_products',
                                       verbose_name='Ценовая категория', blank=True, null=True)
    thumbnail = CleanImageField(upload_to='products/thumbnails', verbose_name='Картинка', blank=True, null=True)
    description = tinymce_models.HTMLField('Описание', blank=True, null=True)
    prescription = models.ManyToManyField(Prescription, blank=True, related_name='prescription_products',
                                          verbose_name='Назначение средства')
    use_description = tinymce_models.HTMLField('Применение', blank=True, null=True)
    key_action = models.ManyToManyField(KeyAction, blank=True, related_name='key_action_products',
                                        verbose_name='Ключевое действие')
    composition = tinymce_models.HTMLField(blank=True, null=True, verbose_name='Состав')
    key_asset = models.ManyToManyField(KeyAsset, blank=True, related_name='key_asset_products',
                                       verbose_name='Ключевой актив')
    sex = models.ManyToManyField(Sex, blank=True, related_name='sex_products',
                                 verbose_name='Пол')
    age_recommendation = models.ForeignKey(AgeRecommendation, on_delete=models.CASCADE, blank=True, null=True,
                                           related_name='age_recommendation_products',
                                           verbose_name='Возрастные рекоммендации')
    format = models.ForeignKey(Format, on_delete=models.CASCADE, blank=True, null=True,
                                       related_name='format_products',
                                       verbose_name='Формат')
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    rating = models.FloatField(verbose_name='Рейтинг продукта', null=True, blank=True)
    category = models.ManyToManyField(Category, verbose_name='Категория',
                                      blank=True, related_name='category_products')
    conversion = GenericRelation('profile.Conversion')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    new_status = models.BooleanField(default=True, verbose_name='Новое средство')
    tag = models.ManyToManyField(Tag, verbose_name='Теги', related_name='product_tags', blank=True)

    def __str__(self):
        return self.name

    @property
    def get_rating(self):
        return self.rating

    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'slug': self.slug})

    def check_conversion(self, request, following_model, following_slug):
        from apps.tools.utils import conversion_checking
        conversion_checking(self, request, following_model, following_slug)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class ProductBanner(Banner, ViewMixin, StatisticViewMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_banners',
                                verbose_name='Продукт')
    views = GenericRelation('profile.ViewAction')

    def set_action_banner(self, request):
        self.check_view_user(request, self)


class ProductImage(CleanImageFieldModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='Продукт')
    image = CleanImageField(upload_to='products/images/', verbose_name='Картинка')
    status_watermark = models.BooleanField(default=False, verbose_name='Необходим копирайт')

    class Meta:
        verbose_name = 'Картинка продукта'
        verbose_name_plural = 'Картинки продукта'

    def __str__(self):
        return str(self.id)


class ProductLink(Link, ViewMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='product_links', verbose_name='Продукт')
    link_conversion = GenericRelation('profile.ViewAction')

    def set_action_link(self, request):
        self.check_view_user(request, self)

    class Meta:
        verbose_name = 'Ссылка на магазины продукта'
        verbose_name_plural = 'Ссылки на магазины продуктов'


class Review(CommentData):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name='Продукт')
    profile = models.ForeignKey('profile.Profile', on_delete=models.CASCADE, related_name='profile_reviews',
                                verbose_name='Отзыв пользователя', blank=True, null=True)
    rating = models.FloatField(default=0, verbose_name='Рейтинг', blank=True, null=True)
    is_publish = models.BooleanField(default=False, verbose_name='Опубликован')

    @property
    def get_normalizated_rating(self):
        return int(self.rating / 5 * 100)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class ReviewImage(CleanImageFieldModel):
    review = models.ForeignKey('products.Review', on_delete=models.CASCADE, related_name='images', verbose_name='Отзыв')
    image = CleanImageField(upload_to='reviews/images/', verbose_name='Картинка')
    status_watermark = models.BooleanField(default=False, verbose_name='Необходим копирайт')

    class Meta:
        verbose_name = 'Картинка отзыва'
        verbose_name_plural = 'Картинки отзывов'

    def __str__(self):
        return str(self.id)
