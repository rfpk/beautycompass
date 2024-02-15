from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify as django_slugify
from apps.blog.models import Article
from apps.manufacturers.models import ManufacturerBanner
from apps.products.models import Brand, Product, Series, ProductBanner, BrandBanner, SeriesBanner
from apps.profile.models import Profile, Conversion, Ip

alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'sh', 'ы': 'y', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}

def slugify(s):
    return django_slugify(''.join(alphabet.get(w, w) for w in s.lower()))

filter_data = {
        'brand': {'model': Brand, 'filter_args': 'manufacturer'},
        'product': {'model': Product, 'filter_args': 'series__brand__manufacturer'},
        'article': {'model': Article, 'filter_args': 'manufacturer'},
        'banner': {
                    'product': {'model': ProductBanner, 'filter_args': 'product__series__brand__manufacturer'},
                    'manufacturer': {'model': ManufacturerBanner, 'filter_args': 'manufacturer'},
                    'brand': {'model': BrandBanner, 'filter_args': 'brand__manufacturer'},
                    'series': {'model': SeriesBanner, 'filter_args': 'series__brand__manufacturer'}
                   }
    }


def get_client_ip(request):
    """
    Ip taken
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def conversion_checking(current_obj, request, following_model, following_slug):
    model_map = {
        'brand': Brand,
        'product': Product,
        'article': Article,
        'series': Series

    }
    if following_model not in model_map:
        return JsonResponse(
            {
             "message": "Such model not exists!",
             "status": "error"
             }
        )
    ip = get_client_ip(request)
    following_obj = get_object_or_404(model_map[following_model], slug=following_slug)
    profile = Profile.objects.filter(user=request.user).first()
    if profile:
        conversion = Conversion.objects.filter(profile=profile, conversions_content_type__model=following_model,
                                               object_id=current_obj.id, conversions_object_id=following_obj.id)
    else:
        conversion = Conversion.objects.filter(ip__ip=ip, conversions_content_type__model=following_model,
                                               object_id=current_obj.id, conversions_object_id=following_obj.id)
    if not conversion.exists():
        ip, _ = Ip.objects.get_or_create(ip=ip)
        Conversion.objects.create(
            profile=profile, ip=ip, content_object=current_obj, conversions_object=following_obj
        )
