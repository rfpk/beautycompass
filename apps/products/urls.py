from django.urls import path
from apps.products import views
from apps.products.models import Review

from apps.products.views import TagProductsView, ProductCreateView, \
    ProductUpdateView, SeriesCreateView, SeriesUpdateView, BrandUpdateView, BrandCreateView, ProductFilterView, \
    BrandArticlesView, create_review, ProductDetailReviewView, brand_subscribe, ProductQuestionsView, get_reviews, \
    get_tags

from apps.products.views import ProductDetailView, ProductReviewsView, SeriesDetailView, BrandDetailView, ProductPhotosView
from apps.profile.views import LikeDislikeView
from apps.tools.database_operations import ADD, REMOVE

app_name = "products"
urlpatterns = [
    # product urls
    path("create-product/<str:brand_slug>/<str:series_slug>", ProductCreateView.as_view(), name="create_product"),
    path("change-product/<slug:slug>/", ProductUpdateView.as_view(), name="change_product"),
    path("delete-product/<slug:slug>/", views.delete_product, name='delete_product'),
    path("product/<slug:slug>/", ProductDetailView.as_view(), name='product_detail'),
    path("product/reviews/<slug:slug>/", ProductReviewsView.as_view(), name='product_reviews'),
    path("product/review/<int:pk>/", ProductDetailReviewView.as_view(), name='product_review_detail'),
    path("product/questions/<slug:slug>/", ProductQuestionsView.as_view(), name='product_questions'),
    path("product/photos/<slug:slug>/", ProductPhotosView.as_view(), name='product_photos'),
    path("sort-product-date/", views.sort_products_date, name='sort_products_date'),
    path("filter-product/", ProductFilterView.as_view(), name='filter_products'),
    path("product-tag/<str:tag_slug>/", TagProductsView.as_view(), name='tag_products'),
    path("create-review/<int:pk>/", create_review, name="create_review"),
    
    path("review/", get_reviews, name='review_get'),
    path("product/<slug:slug>/<str:word>/", get_tags, name='product_tags'),

    # brand urls
    path("create-brand/", BrandCreateView.as_view(), name="create_brand"),
    path("update-brand/<slug:slug>/", BrandUpdateView.as_view(), name="change_brand"),
    path("delete-brand/<slug:slug>/", views.delete_brand, name='delete_brand'),
    path("brand/<slug:slug>/", BrandDetailView.as_view(), name='brand_detail'),
    path("brand-articles/<slug:slug>/", BrandArticlesView.as_view(), name='brand_articles'),
    path("subscribe-brand-action/<slug:slug>/", brand_subscribe, name='brand_subscribe'),

    # series urls
    path("create-series/<slug:slug>/", SeriesCreateView.as_view(), name="create_series"),
    path("change-series/<slug:slug>/", SeriesUpdateView.as_view(), name="change_series"),
    path("delete-series/<slug:slug>/", views.delete_series, name='delete_series'),
    path("series/<slug:slug>/", SeriesDetailView.as_view(), name='series_detail'),

    # actions urls
    path('review_like/<int:pk>/', LikeDislikeView.as_view(model=Review, type_action=ADD),
         name='review_like'),
    path('review_dislike/<int:pk>/', LikeDislikeView.as_view(model=Review, type_action=REMOVE),
         name='review_dislike'),

]
