import logging
from datetime import datetime

from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, AbstractUser as DefaultUser, \
    UserManager as DefaultUserManager
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction, IntegrityError
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _

from apps.blog.models import Article
from apps.profile.mixins import StatisticMixin
from apps.settings.models import Country, HairType, SkinType
from apps.tools.database_operations import CleanImageFieldModel, CleanImageField, ProfileAction, AuthorAction, \
    Action, CommentData


logger = logging.getLogger("profile")


# class UserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#
#         return self.create_user(email, password, **extra_fields)


# class User(AbstractBaseUser):
#     full_name = models.CharField(max_length=150)
#     phone = PhoneNumberField()
#     email = models.EmailField(unique=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['full_name', 'phone']
#
#     objects = UserManager()
#
#     def __str__(self):
#         return self.email
#
#     def has_perm(self, perm, obj=None):
#         return self.is_superuser
#
#     def has_module_perms(self, app_label):
#         return self.is_superuser


class UserManager(DefaultUserManager):

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username and password.
        """
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        with transaction.atomic():
            GlobalUserModel = apps.get_model(
                self.model._meta.app_label, self.model._meta.object_name
            )

            username = GlobalUserModel.normalize_username(username)
            email = self.normalize_email(username)
            email = email.lower()
            user = self.model(username=email, **extra_fields)
            user.password = make_password(password)
            user.save(using=self._db)

        return user


class User(DefaultUser):
    first_name = None
    last_name = None
    email = None

    objects = UserManager()

    EMAIL_FIELD = ""
    REQUIRED_FIELDS = []

    def clean(self):
        super(AbstractBaseUser, self).clean()

    def profile(self):
        try:
            return self.user_profile
        except Exception:
            return None

    def save(self, *args, **kwargs):
        new = False
        if not self.id:
            new = True
        super().save(*args, **kwargs)
        if new:
            profile = Profile.objects.create(user=self, email=self.username, contact_email=self.username)
            author = Author.objects.create(profile=profile)
            AuthorHistory.objects.create(author=author, created_at=datetime.now())


class Profile(CleanImageFieldModel):
    class SexChoices(models.TextChoices):
        MALE = 'M', 'Мужчина'
        FEMALE = 'F', 'Женщина'

    user = models.OneToOneField(
        User, related_name="user_profile", on_delete=models.CASCADE
    )
    email = models.EmailField(_("email address"), null=True, unique=True)
    nickname = models.CharField(max_length=15, blank=True, verbose_name='Ник')
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    avatar = CleanImageField(upload_to='profiles/avatars/', verbose_name='Картинка', blank=True, null=True)

    sex = models.CharField(blank=True, null=True, max_length=1, choices=SexChoices.choices, verbose_name='Пол')

    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    phone = PhoneNumberField(blank=True, null=True, verbose_name='Телефон')
    contact_email = models.EmailField(blank=True, null=True, verbose_name='Контактный email')
    description = models.TextField(blank=True, verbose_name='Описание профиля')

    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='profiles', verbose_name='Страна',
                                blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, verbose_name='Город')

    public_email = models.EmailField(blank=True, null=True, verbose_name='Публичный email')
    hair_type = models.ForeignKey(HairType, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Тип волос')
    skin_type = models.ForeignKey(SkinType, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Тип кожи')
    accept_news = models.BooleanField(default=False, verbose_name='Принимать новости')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    like_action = GenericRelation('LikeAction')
    favorite_action = GenericRelation('FavoriteAction')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    __original_email = None

    def __str__(self):
        return str(self.email)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    @property
    def identificator(self):
        return self.user.username

    @property
    def last_name_slice(self):
        return self.last_name[0:1]

    def is_admin(self):
        return self.user.groups.filter(name='admin').exists()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None, delete=False):

        if delete:
            self.email = None
            self.public_email = None
            self.contact_email = None
            self.is_active = False

            self.user.username = str(self.user.pk)
            self.user.is_active = False

            if update_fields is None:
                update_fields = ['email', 'public_email', 'contact_email', 'is_active', ]
            else:
                update_fields.extend(['email', 'public_email', 'contact_email', 'is_active', ])

            try:
                with transaction.atomic():
                    self.user.save(update_fields=['username', 'is_active'])
                    super().save(force_insert, force_update, using, update_fields)
            except IntegrityError as e:
                logger.exception(f"Profile({self.id}) change error: {e}")
            return

        self.assign_old_values()

        try:
            with transaction.atomic():
                if self.email != self.__original_email:
                    self.user.username = self.email
                    self.user.save(update_fields=['username'])
                super().save(force_insert, force_update, using, update_fields)
        except IntegrityError as e:
            logger.exception(f"Profile({self.id}) change error: {e}")

    def assign_old_values(self):
        self_dict = self.__class__.objects.filter(pk=self.pk).values('email').first()

        if self_dict:
            self.__original_email = self_dict.get('email')


class LikeAction(ProfileAction):
    profile = models.ForeignKey('profile.Profile', on_delete=models.CASCADE, related_name='profile_likes_actions',
                                verbose_name='Профиль')

    class Meta:
        verbose_name = 'История лайков'
        verbose_name_plural = 'История лайков'


class FavoriteAction(ProfileAction):
    profile = models.ForeignKey('profile.Profile', on_delete=models.CASCADE, related_name='profile_favorites_actions',
                                verbose_name='Профиль')

    class Meta:
        verbose_name = 'История добавления в избранное'
        verbose_name_plural = 'История добавлений в избранное'


class Ip(models.Model):
    ip = models.GenericIPAddressField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.ip)

    class Meta:
        verbose_name = 'IP-aдрес'
        verbose_name_plural = 'IP-aдреса'


class ViewAction(ProfileAction):
    profile = models.ForeignKey('profile.Profile', on_delete=models.CASCADE, blank=True, null=True,
                                related_name='profile_views_actions', verbose_name='Профиль')
    ip = models.ForeignKey('profile.Ip', on_delete=models.CASCADE, related_name='ip_views',
                           verbose_name='IP-aдрес')
    session_id = models.CharField(max_length=150, blank=True, null=True, verbose_name='Сессия пользователя')

    class Meta:
        verbose_name = 'История просмотров'
        verbose_name_plural = 'История просмотров'


class Conversion(ProfileAction):
    profile = models.ForeignKey('profile.Profile', on_delete=models.CASCADE, blank=True, null=True,
                                related_name='profile_conversions', verbose_name='Профиль')
    ip = models.ForeignKey('profile.Ip', on_delete=models.CASCADE, related_name='ip_conversions',
                           verbose_name='IP-aдрес')
    conversions_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                                 related_name='content_type_conversions')
    conversions_object_id = models.PositiveIntegerField(blank=True, null=True)
    conversions_object = GenericForeignKey("conversions_content_type", "conversions_object_id")

    class Meta:
        verbose_name = 'История переходов на страницу продукта/статьи/бренда/'
        verbose_name_plural = 'История переходов на страницы продуктов/статей/брендов/'


class Appeal(models.Model):
    """Class to create appeal for technical support"""
    class AppealType(models.TextChoices):
        TECH_SUPPORT = 'TS', _('Техническая поддержка')
        QUESTION_SUGGEST = 'QS', _('Общие вопросы и предложения')
        LEGAL_FINANCE = 'LF', _('Юридические и финансовые вопросы')

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_appeals',
                                verbose_name='Профиль')
    title = models.CharField(max_length=300, blank=True, verbose_name='Заголовок обращения')
    text = models.TextField(verbose_name='Текст обращения')
    date = models.DateTimeField(auto_now=True, verbose_name='Дата обращения')
    subject_appeal = models.CharField(max_length=25, choices=AppealType.choices,
                                      default=AppealType.TECH_SUPPORT, verbose_name='Тема обращения')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'


class Author(models.Model):
    class AuthorType(models.TextChoices):
        READER = 'R', _('Читатель')
        AUTHOR = 'A', _('Автор')
        MANUFACTURER = 'M', _('Производитель')

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                related_name='profile_author', verbose_name='Профиль')
    type = models.CharField(max_length=25, choices=AuthorType.choices,
                            default=AuthorType.READER, verbose_name='Тип пользователя')
    rating = models.PositiveIntegerField(default=0, verbose_name='Рейтинг')

    def __str__(self):
        return f'{self.get_type_display()} {self.profile}'

    @property
    def years_old(self):
        return datetime.now().year - self.profile.date_of_birth.year

    def get_rating_value(self, period) -> int:
        from apps.profile.services.author_rating_statistics import calculate_author_rating_period
        period_rating = sum(calculate_author_rating_period(self, period).values())
        return period_rating

    def get_rating_place(self) -> int:
        return list(Author.objects.order_by("-rating")).index(self) + 1

    def get_current_status_obj(self):
        history_status = self.history.last()
        if history_status:
            return history_status

    def get_author_url(self):
        reverse('profile:author_reviews_articles', kwargs={'nickname': self.profile.nickname})

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class AuthorHistory(models.Model):
    """Class for save history activity of author"""
    class AuthorStatus(models.TextChoices):
        ACTIVE = 'AT', _('Активен')
        BLOCKED_UNTIL = 'BU', _('Заблокирован на время')
        BLOCKED_FOREVER = 'BF', _('Заблокирован навсегда')

    author = models.ForeignKey(Author, on_delete=models.CASCADE,
                               related_name='history', verbose_name='Автор')
    current_status = models.CharField(max_length=25, default=AuthorStatus.ACTIVE,
                                      choices=AuthorStatus.choices,
                                      verbose_name='Текущий статус активности')
    created_at = models.DateField(verbose_name='Дата начала действия статуса')
    close_at = models.DateField(verbose_name='Дата окончания действия статуса',
                                null=True, blank=True)
    description = models.TextField(blank=True, verbose_name='Описание статуса')

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Журнал изменения статуса'
        verbose_name_plural = 'Журнал изменений статусов'


class SubscribeAction(AuthorAction):
    author = models.ForeignKey('profile.Author', on_delete=models.CASCADE, related_name='author_subscribers',
                                verbose_name='Профиль автора')
    author_action = models.ForeignKey('profile.Author', on_delete=models.CASCADE,
                                          related_name='authors_signed',
                                          verbose_name='Профиль подписчика')

    class Meta:
        verbose_name = 'История подписки'
        verbose_name_plural = 'История подписок'


class GratitudeAction(AuthorAction):
    author = models.ForeignKey('profile.Author', on_delete=models.CASCADE, related_name='author_gratitudes',
                                verbose_name='Профиль автора')
    author_action = models.ForeignKey('profile.Author', on_delete=models.CASCADE,
                                          related_name='authors_gratitudes',
                                          verbose_name='Профиль благодаришего')

    class Meta:
        verbose_name = 'История благодарности'
        verbose_name_plural = 'История благодарностей'


class Overview(Action, StatisticMixin):
    """Model for create overviews authors"""
    author = models.ForeignKey(Author, on_delete=models.CASCADE,
                               related_name='overviews', verbose_name='Автор')
    title = models.CharField(max_length=255, verbose_name='Заголовок обзора')
    slug = models.SlugField(unique=True)
    description = models.TextField(verbose_name='Текст статьи')
    thumbnail = CleanImageField(upload_to='overviews/thumbnails/', verbose_name='Главная фотография',
                                blank=True, null=True)
    brand = models.ForeignKey('products.Brand', on_delete=models.CASCADE, related_name='brand_overviews',
                              verbose_name='Бренд',
                              blank=True, null=True)
    tag = models.ManyToManyField('products.Tag', verbose_name='Теги', blank=True, related_name='overview_tags')
    is_draft = models.BooleanField(default=False, verbose_name='Черновик')
    is_publish = models.BooleanField(default=False, verbose_name='Опубликован')
    is_active = models.BooleanField(default=False, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    total_rating = models.PositiveIntegerField(default=0, verbose_name='Общий рейтинг')

    class Meta:
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзоры'

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if self.author.type == Author.AuthorType.READER:
            if self.is_publish:
                self.author.type = Author.AuthorType.AUTHOR
                logger.info(f'New type for profile {self.author.profile.email}: "AUTHOR"')
                self.author.save()
        else:
            if Overview.objects.filter(author=self.author, is_publish=True).count() >= 10:
                self.is_publish = True
                self.save()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        reverse('profile:detail_overview', kwargs={'slug': self.slug})

class OverviewComment(CommentData):
    overview = models.ForeignKey(Overview, on_delete=models.CASCADE, related_name='comments',
                                 verbose_name='Обзор')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE,
                               related_name='answers', verbose_name='Корневой комментарий')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='author_comments',
                               verbose_name='Автор комментария')
    is_publish = models.BooleanField(default=True, verbose_name='Опубликован')

    class Meta:
        verbose_name = 'Комментарий обзора'
        verbose_name_plural = 'Комментарии обзоров'

class OverviewPhoto(CleanImageFieldModel):
    overview = models.ForeignKey(Overview, on_delete=models.CASCADE, related_name='photos_overview',
                                 verbose_name='Обзор')
    image = CleanImageField(upload_to='overviews/thumbnails/', verbose_name='Главная фотография',
                            blank=True, null=True)
    status_watermark = models.BooleanField(default=False, verbose_name='Необходим копирайт')

    class Meta:
        verbose_name = 'Фотография обзора'
        verbose_name_plural = 'Фотографии обзоров'

    def __str__(self):
        return str(self.id)


class AppealImage(models.Model):
    appeal = models.ForeignKey(Appeal, on_delete=models.CASCADE, related_name='images', verbose_name='Обращение')
    image = CleanImageField(upload_to='profile/images/', verbose_name='Картинка')

    class Meta:
        verbose_name = 'Фото обращения'
        verbose_name_plural = 'Фото обращения'


class Question(models.Model):
    """Model for question user profile"""
    profile = models.ForeignKey(Profile, related_name="profile_questions",
                                on_delete=models.CASCADE, verbose_name='Профиль')
    product = models.ForeignKey('products.Product', related_name="product_questions",
                                on_delete=models.CASCADE, verbose_name='Продукт')
    text = models.TextField(verbose_name='Текст вопроса')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата вопроса')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.text

