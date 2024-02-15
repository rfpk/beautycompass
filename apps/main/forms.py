from django import forms
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from apps.profile.models import Profile, User
from django.contrib.auth import password_validation
from django.forms import EmailInput


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={
                "class": "col-3 my-0 p-0 auth__label",
                "id": "registerInputPassword1",
                "minlength": "8",
            }
        ),
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput(
            attrs={
                "class": "col-3 my-0 p-0 auth__label",
                "id": "registerInputPassword2",
                "minlength": "8",
            }
        ),
    )
    phone = PhoneNumberField(widget=forms.TextInput(attrs={'type': 'tel', }))
    nickname = forms.CharField(widget=forms.TextInput(attrs={
        "for": "headerReisterFirstName",
    }), max_length=15)
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "for": "headerReisterFirstName",
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "for": "headerReisterLastName",
    }))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields

        widgets = {
            "username": forms.EmailInput(
                attrs={"for": "headerRegisterEmail",
                       "class": "col-3 my-0 p-0 auth__label",
                       "id": "userSignupEmail"},
            ),
        }

    def clean_password(self):
        password = self.cleaned_data["password1"]
        if password:
            password_validation.validate_password(password)
        return password

    def clean_nickname(self):
        return self.cleaned_data['nickname'].lower()

    def clean_username(self):
        email = User.objects.normalize_email(self.cleaned_data['username'])
        email = email.lower()
        self.cleaned_data['username'] = email
        return super().clean_username()


class LoginUserForm(forms.Form):
    email = forms.CharField(
        label="Е-mail",
        widget=forms.EmailInput(
            attrs={"class": "form-control order-2", "id": "headerAuthEmail"}
        ),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control shadow-none",
                "id": "authInputPassword",
                "minlength": "8",
            }
        ),
    )

    def clean_email(self):
        email = User.objects.normalize_email(self.cleaned_data['email'])
        return email.lower()


class PasswordReset(forms.Form):

    email = forms.EmailField(
        required=True,
        widget=EmailInput(
            attrs={"class": "form-control shadow-none", "id": "userForgotEmail"}
        ),
    )

    def clean_email(self):
        email = User.objects.normalize_email(self.cleaned_data['username'])
        return email.lower()


class ChangePasswordForm(forms.Form):
    password = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control shadow-none",
                "id": "userSignUpPassword",
                "minlength": "8",
            }
        ),
    )

