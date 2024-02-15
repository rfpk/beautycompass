from django import forms
from django.forms import inlineformset_factory

from apps.products.models import Review, Brand, Series, Product, SeriesImage, Tag, BrandLink, BrandBanner, \
    SeriesBanner, ProductImage, ProductLink, AgeRecommendation, PriceCategory, Sex, Prescription, Format, KeyAsset, \
    KeyAction


class CommentForm(forms.ModelForm):
    images = forms.FileField(label='Фотографии отзыва', required=False,
                             widget=forms.ClearableFileInput(attrs={"allow_multiple_selected": True}))
    class Meta:
        model = Review
        fields = ['text', 'rating']
        labels = {
            'text': 'Текст отзыва',
            'rating': 'Рейтинг'
        }

    def save(self, commit=True):
        review = super().save(commit=commit)
        return review


BrandBannerFormSet = inlineformset_factory(
    Brand,
    BrandBanner,
    fields=['banner', 'url'],
    extra=1,
)
BrandLinkFormSet = inlineformset_factory(Brand, BrandLink, fields=['name', 'url'], extra=1)


class BrandForm(forms.ModelForm):
    tag = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)
    brand_banners = BrandBannerFormSet()
    brand_links = BrandLinkFormSet()

    class Meta:
        model = Brand
        fields = ['name', 'image', 'short_description', 'tag']
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'short_description': 'Краткое Описание',
            'image': 'Изображение',
            'tag': 'Теги',
            'country': 'Регион'
        }

    def save(self, commit=True):
        brand = super().save(commit=False)
        if commit:
            brand.save()
        return brand

SeriesBannerFormSet = inlineformset_factory(
    Series,
    SeriesBanner,
    fields=['banner', 'url'],
    extra=1,
)

class SeriesBannerForm(forms.ModelForm):
    banner = forms.FileField(required=False,
                             widget=forms.ClearableFileInput(attrs={
                                 'class': 'file-input',
                                 'onchange': 'handleFileSelected(event)',
                             }))
    class Meta:
        model = SeriesBanner
        fields = ['banner', 'url']


class SeriesForm(forms.ModelForm):
    name = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={
        'class': 'brand__input input--regular'
    }))
    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.SelectMultiple,
    )
    logo = forms.FileField(
        label='Изображения серии',
        required=False,
        widget=forms.ClearableFileInput(
        attrs={
            'class': 'file-input profile__file-input brand__file-input',
            'onchange': 'handleFileSelected(event)'
        })
    )
    series_banners = SeriesBannerFormSet()
    brand = forms.ModelChoiceField(queryset=Brand.objects.filter(manufacturer__profile__user=1))

    class Meta:
        model = Series
        fields = ['name', 'brand', 'description', 'tag', 'logo']
        labels = {
            'name': 'Название',
            'tag': 'Теги',
            'description': 'Краткое описание',
        }
        widgets = {
            'series_banners__banner': forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'file-input'}))
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(SeriesForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['brand'].queryset = Brand.objects.filter(manufacturer__profile__user=user)

    def save(self, commit=True):
        series = super().save(commit=False)
        image = self.cleaned_data.get('logo', None)
        if commit:
            series.save()
        if image:
            SeriesImage.objects.create(series=series, image=image)
        return series


ProductImageFormSet = inlineformset_factory(Product, ProductImage, fields=['image', 'status_watermark'], extra=1)
ProductLinkFormSet = inlineformset_factory(Product, ProductLink, fields=['name', 'url'], extra=1)


class ProductForm(forms.ModelForm):
    tag = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)
    product_images = ProductImageFormSet()
    product_links = ProductLinkFormSet()

    prescription = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Prescription.objects.all(),
    )

    format = forms.ModelChoiceField(
        required=False,
        queryset=Format.objects.all(),
    )

    sex = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Sex.objects.all(),
    )

    key_asset = forms.ModelMultipleChoiceField(
        required=False,
        queryset=KeyAsset.objects.all(),
    )

    key_action = forms.ModelMultipleChoiceField(
        required=False,
        queryset=KeyAction.objects.all(),
    )

    age_recommendation = forms.ModelChoiceField(
        required=False,
        queryset=AgeRecommendation.objects.all(),
        widget=forms.Select(attrs={'class': 'input--arrow'}),
    )
    price_category = forms.ModelChoiceField(
        required=False,
        queryset=PriceCategory.objects.all(),
        widget=forms.Select(attrs={'class': 'input--arrow'}),
    )

    class Meta:
        model = Product
        fields = ['series', 'price_category', 'thumbnail', 'name', 'description', 'prescription',
                  'use_description', 'key_action', 'composition', 'key_asset', 'sex',
                  'age_recommendation', 'category', 'tag']
        labels = {
            'series': 'Серия',
            'price_category': 'Ценовая категория',
            'name': 'Название продукта',
            'description': 'Описание',
            'prescription': 'Назначение средства',
            'use_description': 'Применение',
            'key_action': 'Ключевое действие',
            'composition': 'Состав',
            'key_asset': 'Ключевой актив',
            'sex': 'Пол',
            'age_recommendation': 'Возрастные рекоммендации',
            'category': 'Категория',
            'tag': 'Тег'
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['thumbnail'].required = False

    def save(self, commit=True):
        product = super().save(commit=False)
        if commit:
            product.save()
        return product
