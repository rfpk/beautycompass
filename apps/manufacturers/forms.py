from django import forms
from django.forms import inlineformset_factory
from phonenumber_field.formfields import PhoneNumberField

from apps.manufacturers.models import Manufacturer, ManufacturerMailing, ManufacturerLinkShop, \
    ManufacturerQuestionAnswer, ManufacturerBanner, AnswerReview


class ManufacturerLinkShopForm(forms.ModelForm):
    class Meta:
        model = ManufacturerLinkShop
        fields = ['name', 'url']
        labels = {
            'name': 'Название магазина',
            'url': 'Ссылка на магазин'
        }


ManufacturerBannerFormSet = inlineformset_factory(
    Manufacturer,
    ManufacturerBanner,
    fields=['banner', 'url'],
    extra=1,
)
ManufacturerLinkFormSet = inlineformset_factory(Manufacturer, ManufacturerLinkShop, fields=['name', 'url'], extra=1)


class ManufacturerForm(forms.ModelForm):
    manufacturer_banners = ManufacturerBannerFormSet()
    manufacturer_links = ManufacturerLinkFormSet()
    logo = forms.FileField(required=False, widget=forms.FileInput(attrs={
        'class': 'file-input',
        'name': 'logo',
        'id': 'manufacturer-info-image',
    }))


    class Meta:
        model = Manufacturer
        fields = '__all__'

        labels = {
            'name': 'Название компании',
            'email': 'E-mail',
            'logo': 'Логотип компании',
            'phone': 'Телефон',
            'description': 'Краткое описание компании',
            'history': 'История компании',
            'principle': 'Принципы компании',
            'country': 'Страна',
            'city': 'Город (необязательно)',
            'banner': 'Баннер производителя (1080х277 рх)',
            'link_banner': 'Ссылка к баннеру'
        }
        widgets = {
            'country': forms.Select(attrs={
                'class': 'select__header input--select',
            }),
            'city': forms.TextInput(attrs={
                'class': '',
            }),
        }
    
    def save(self, commit=True):
        manufacturer = super().save(commit=commit)
        return manufacturer
    
    def __init__(self,*args, **kwargs):
        super(ManufacturerForm,self).__init__(*args,**kwargs)
        banners = ManufacturerBanner.objects.filter(manufacturer=self.instance)
        self.manufacturer_banners = ManufacturerBannerFormSet(
            queryset=banners,
        )


class ManufacturerUpdateForm(forms.ModelForm):
    logo = forms.FileField(required=False, widget=forms.FileInput(attrs={
        'class': 'file-input',
        'name': 'logo',
        'id': 'manufacturer-info-image',
    }))

    class Meta:
        model = Manufacturer
        fields = ['name', 'logo', 'phone', 'email']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'data-mask': "+7(900)000-00-00",
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
        }

    def save(self, commit=True):
        manufacturer = super().save(commit=commit)
        return manufacturer


class MailingEmailFormSet(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input--regular'}))


class MailingPhoneFormSet(forms.Form):
    phone = PhoneNumberField()


class ManufacturerMailForm(forms.ModelForm):
    image = forms.FileField(required=False, widget=forms.FileInput(attrs={
        'class': 'file-input',
        'id': 'mailing-form__pic',
        'onchange': 'handleFileSelected(this)'
    }))
    banner = forms.FileField(required=False, widget=forms.FileInput(attrs={
        'class': 'file-input',
        'id': 'mailing-form__banner',
        'onchange': 'handleFileSelected(this)'
    }))
    background_image = forms.FileField(required=False, widget=forms.FileInput(attrs={
        'class': 'file-input',
        'id': 'mailing-form__background',
        'onchange': 'handleFileSelected(this)'
    }))
    class Meta:
        model = ManufacturerMailing
        fields = '__all__'
        exclude = ['email', 'phone', 'manufacturer']

        labels = {
            'company_name': 'Название компании',
            'email': 'E-mail',
            'phone': 'Телефон',
            'image': 'Изображение',
            'text': 'Текст рассылки',
            'banner': 'Баннер',
            'link_banner': 'Ссылка к баннеру',
            'background_image': 'Фон'
        }


class ReviewAnswerForm(forms.ModelForm):
    class Meta:
        model = AnswerReview
        fields = '__all__'