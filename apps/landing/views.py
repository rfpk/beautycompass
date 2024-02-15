from django.shortcuts import render
from django.views.generic import DetailView

from apps.blog.models import Article
from apps.landing.models import MainPage, MainBanner
from apps.products.models import Product


class LandingPageView(DetailView):
    model = MainPage
    template_name = 'landing/landing_pages.html'
    context_object_name = 'landing_page'

    def get_queryset(self):
        return MainPage.objects.filter(slug=self.kwargs['slug'])


def get_main_page(request):
    context = {
        'actually_articles': Article.objects.filter(is_publish=True, is_active=True).order_by('-date')[:6],
        'new_products': Product.objects.filter(new_status=True).order_by('?')[:5],
        'main_banners': MainBanner.objects.all(),
        'selection_banners': MainBanner.objects.filter(banner_selection=True)
    }
    return render(request, "landing/main.html", context)

