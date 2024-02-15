from math import ceil
from django import forms

from apps.services.models import Tariff, Plan


class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = '__all__'


class TariffForm(forms.ModelForm):
    type = forms.IntegerField()
    price = forms.DecimalField(max_digits=5, decimal_places=3)

    class Meta:
        model = Tariff
        fields = ['price']

    def clean_lat(self):
        price = self.cleaned_data['price']
        if ceil(float(price)) <= 0:
            raise forms.ValidationError("Enter Valid Price")
        return self.cleaned_data['price']
