import datetime
import logging

from django.db import transaction
from django.urls import reverse
from django.http import JsonResponse
from apps.services.models import Tariff, Plan
from django.shortcuts import get_object_or_404, redirect
from dateutil.relativedelta import relativedelta
from apps.manufacturers.models import Manufacturer, ManufacturerTariffHistory
from apps.services.forms import TariffForm, PlanForm

logger = logging.getLogger("service")


def create_tariff_plan(request):
    if not request.user.is_superuser or request.method == 'GET':
        return JsonResponse({"redirect": reverse("profile:profile_detail")})
    else:
        if request.method == 'POST':
            form = PlanForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'status': 'success', 'message': 'Tariff Plan success Create'})
            else:
                return JsonResponse({'status': 'error', 'message': 'The data is incorrect'})
        else:
            return redirect("profile:profile_detail")


def create_tariff(request):
    if not request.user.is_superuser or request.method == 'GET':
        return JsonResponse({"redirect": reverse("profile:profile_detail")})
    else:
        if request.method == 'POST':
            form = TariffForm(request.POST)
            if form.is_valid():
                tariff = form.save(commit=False)
                tariff.price = form.cleaned_data.get('price')
                tariff.type = Plan.objects.filter(pk=form.cleaned_data.get('type')).first()
                tariff.save()
                return JsonResponse({'status': 'success', 'message': 'Tariff success Create'})
            else:
                return JsonResponse({'status': 'error', 'message': 'The data is incorrect'})


def change_tariff(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({"redirect": reverse("profile:panel")})
    else:
        new_tariff = get_object_or_404(Tariff, pk=pk)
        manufacturer = get_object_or_404(Manufacturer, profile__user=request.user)
        history_manufacturer = manufacturer.manufacturer_tariffs.last()
        try:
            with transaction.atomic():
                if not history_manufacturer:
                    history_manufacturer.end_date = datetime.datetime.now()
                    history_manufacturer.save()
                end_date_tariff = relativedelta(months=+new_tariff.type.period)
                ManufacturerTariffHistory.objects.create(manufacturer=manufacturer,
                                                         tariff_plan=new_tariff,
                                                         end_date=end_date_tariff
                                                         )
                logger.info(f"Profile({manufacturer.profile.email}) has change tariff on Tariff({new_tariff.pk})")
                return JsonResponse(
                    {
                        "message": "New tariff plan was set",
                        "status": "success"
                    }
                )
        except Exception as e:
            logger.exception(f"Profile({manufacturer.profile.email}) change error: {e}")
