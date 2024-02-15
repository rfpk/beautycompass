from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class HiddenPasswordForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label="Password",
    )
