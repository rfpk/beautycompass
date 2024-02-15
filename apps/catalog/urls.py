from django.urls import path

from apps.catalog.views import CatalogView, CategoryProductView


app_name = "catalog"
urlpatterns = [
    path("", CatalogView.as_view(), name='catalog'),
    path("<slug:cat_slug>/", CategoryProductView.as_view(), name='category'),
    path("<slug:cat_slug>/<slug:sub_slug>/", CategoryProductView.as_view(), name='sub_category'),
    path("<slug:cat_slug>/<slug:sub_slug>/<slug:prod_slug>/", CategoryProductView.as_view(), name='sub_products'),
]
