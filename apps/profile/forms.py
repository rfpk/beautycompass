from django import forms

from apps.products.models import Brand, Tag
from apps.profile.models import Question, Overview, OverviewPhoto, OverviewComment
from apps.profile.models import Profile, Appeal


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', ]

class ProfileForm(forms.ModelForm):
    avatar = forms.FileField(required=False, widget=forms.FileInput(attrs={
        'class': 'file-input',
        'id': 'form__pic',
        'name': 'form__pic',
    }))
    sex = forms.ChoiceField(
        choices=Profile.SexChoices.choices,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control passw__inp',
    }), required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control passw__inp__rep',
    }), required=False)
    accept_news = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'check check__wrap',
            'name': 'skinProp',
            'value': 'dehydration',
            'form': 'profile__confidInf',
            'id': 'dehydration',
        })
    )
    
    class Meta:
        model = Profile
        fields = ["nickname", "first_name", "last_name", "avatar",
                  "sex", "date_of_birth", "phone", "contact_email",
                  "description", "country", "city", "public_email",
                  "hair_type", "skin_type", "accept_news", "email"]
        widgets = {
            'nickname': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'phone': forms.TextInput(attrs={
                'data-mask': "+7(900)000-00-00",
                'class': 'form-control'
            }),
            'date_of_birth': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                },
                format='%Y-%m-%d'
            ),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control'
            }),
            'country': forms.Select(attrs={
                'class': 'form-select'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'public_email': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
            'hair_type': forms.Select(attrs={
                'class': 'form-select',
            }),
            'skin_type': forms.Select(attrs={
                'class': 'form-select',
            })
        }
        labels = {
            'email': 'Логин',
            'nickname': 'Ник',
            'first_name': 'Имя',
            'last_name': 'Фамилия (скрыто)',
            'sex': 'Пол',
            'avatar': 'Аватар',
            'date_of_birth': 'Дата рождения',
            'phone': 'Телефон',
            'contact_email': 'Email для связи с администрацией',
            'description': 'Описание профиля',
            'country': 'Страна',
            'city': 'Город',
            'public_email': 'E-mail (виден на странице профиля)',
            'hair_type': 'Тип волос',
            'skin_type': 'Тип кожи'
        }

    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )
        return cleaned_data
    
    def save_password(self, user, commit=True):
        password = self.cleaned_data["password"]
        user.set_password(password)
        if commit:
            user.save()
        return user


class AppealForm(forms.ModelForm):
    images = forms.FileField(label='Фотографии обращения', required=False,
                             widget=forms.ClearableFileInput(attrs={"allow_multiple_selected": True}))
    subject_appeal = forms.ChoiceField(
        choices=Appeal.AppealType.choices,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True,
    )

    class Meta:
        model = Appeal
        fields = ['title', 'text', 'subject_appeal']

        labels = {
            'title': 'Логин',
            'text': 'Текст обращения',
            'subject_appeal': 'Тема обращения'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        appeal = super().save(commit=commit)
        if commit:
            appeal.save()
        return appeal


class CreateUpdateOverviewForm(forms.ModelForm):
    images = forms.FileField(label='Фотографии обзора', required=False,
                             widget=forms.ClearableFileInput(attrs={"allow_multiple_selected": True}))
    thumbnail = forms.FileField(required=False, widget=forms.FileInput(attrs={}))

    class Meta:
        model = Overview
        fields = ["title", "description", "thumbnail"]
        brand = forms.ModelChoiceField(queryset=Brand.objects.all(), required=False)
        tag = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)

        labels = {
            'title': 'Заголовок обзора',
            'description': 'Текст обзора',
            'tag': 'Теги',
            'brand': 'Бренд',
            'thumbnail': 'Главное фото',
        }

    def save(self, commit=True):
        overview = super().save(commit=commit)
        images = self.cleaned_data.get('images')
        if images:
            for image in images:
                OverviewPhoto.objects.create(overview=overview, image=image)
        return overview


class CreateCommentForm(forms.ModelForm):
    images = forms.FileField(label='Изображения комментария', required=False,
                             widget=forms.ClearableFileInput(attrs={"allow_multiple_selected": True}))
    overview = forms.IntegerField(widget=forms.HiddenInput)
    parent = forms.IntegerField(widget=forms.HiddenInput, required=False)
    
    def save(self, commit=True):
        comment = super().save(commit=commit)
        return comment
    
    def check_exist(self, user):
        parent = self.cleaned_data.get('parent', None)
        if parent:
            commentExist = OverviewComment.objects.filter(
                author__profile__user=user,
                pk=int(parent),
            ).first()
            return commentExist

    class Meta:
        model = OverviewComment
        fields = ['text', ]
        labels = {
            'text': 'Текст',
        }


class OverviewPublish(forms.ModelForm):
    class Meta:
        model = Overview
        fields = ['is_publish', 'is_draft']
    
    def save(self, commit=True):
        overview = super().save(commit=commit)
        return overview