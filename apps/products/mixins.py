from datetime import date

from django.http import JsonResponse

from apps.profile.models import ViewAction, Profile, Ip

class ManufacturerStatus:
    @staticmethod
    def check_manufacturer_status(manufacturer):
        manufacturer_current_tariff = manufacturer.manufacturer_tariffs
        manufacturer_current_tariff_last = manufacturer_current_tariff.last()
        if not manufacturer_current_tariff_last:
            return JsonResponse(
                {
                    "message": "Manufacturer has not current tariff!",
                    "status": "error"
                }
            )
        today = date.today()
        if manufacturer_current_tariff_last.end_date < today:
            return JsonResponse(
                {
                    "message": "The current tariff has expired!",
                    "status": "error"
                }
            )
        return True


class BrandMixin(ManufacturerStatus):
    template_name = 'products/create_brand.html'

    @staticmethod
    def get_model():
        from django.apps import apps
        return apps.get_model('products', 'Brand')

    @staticmethod
    def get_form_class():
        from apps.products.forms import BrandForm
        return BrandForm


class SeriesMixin(ManufacturerStatus):
    def get_model(self):
        from django.apps import apps
        return apps.get_model('products', 'Series')

    def get_form_class(self):
        from apps.products.forms import SeriesForm
        return SeriesForm
    template_name = 'series/series_form.html'


class ProductMixin(ManufacturerStatus):
    def get_model(self):
        from django.apps import apps
        return apps.get_model('products', 'Product')

    def get_form_class(self):
        from apps.products.forms import ProductForm
        return ProductForm
    template_name = 'product/product_form.html'


class ViewMixin:

    @staticmethod
    def check_view_user(request, obj):
        from apps.tools.utils import get_client_ip
        ip = get_client_ip(request)
        model_name = obj.__class__.__name__.lower()
        if request.user.is_authenticated:
            profile = Profile.objects.filter(user=request.user).first()
            view = ViewAction.objects.filter(profile=profile,
                                             content_type__model=model_name,
                                             object_id=obj.id)
        else:
            profile = None
            view = ViewAction.objects.filter(ip__ip=ip,
                                             content_type__model=model_name,
                                             object_id=obj.id)
        if not view.exists():
            ip, _ = Ip.objects.get_or_create(ip=ip)
            session_id = request.session.session_key
            ViewAction.objects.create(profile=profile, ip=ip, session_id=session_id, content_object=obj)
            if model_name == 'overview':
                obj.author.rating += 1
                obj.author.save(update_fields=['rating'], )
