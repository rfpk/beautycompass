from django.contrib import admin


from .models import (
    Brand,
    Series,
    Product,
    ProductImage,
    Review,
    ReviewImage, BrandLink, SeriesImage, Tag, PriceCategory, Prescription, KeyAction, KeyAsset, Sex, AgeRecommendation,
    ProductBanner, ProductLink, BrandBanner, BrandSocialLink, Format, SeriesBanner, BrandSubscriber
)

class BrandLinksInline(admin.TabularInline):
    model = BrandLink
    extra = 3

class BrandBannerInline(admin.TabularInline):
    model = BrandBanner
    extra = 3

class SeriesBannerInline(admin.TabularInline):
    model = SeriesBanner
    extra = 3

class SeriesInline(admin.TabularInline):
    model = Series
    extra = 3

class TagsFilter(admin.SimpleListFilter):
    title = 'Теги'
    parameter_name = 'tag'

    def lookups(self, request, model_admin):
        tags = Tag.objects.all()
        return [(tag.id, tag.name) for tag in tags]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(tag__id=self.value())
        else:
            return queryset


class BrandSocialInline(admin.TabularInline):
    model = BrandSocialLink
    extra = 3


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'manufacturer', 'country')
    search_fields = ('name', 'manufacturer__name')
    list_filter = ['name', 'manufacturer', TagsFilter]
    prepopulated_fields = {'slug': ('name',)}
    inlines = (BrandSocialInline, BrandLinksInline, BrandBannerInline)


@admin.register(BrandSubscriber)
class BrandSubscriberAdmin(admin.ModelAdmin):
    list_display = ('brand', 'profile', 'type_action', 'created_at')


class SeriesImageInline(admin.TabularInline):
    model = SeriesImage
    extra = 3


class ProductInline(admin.TabularInline):
    model = Product
    extra = 3


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'brand', 'get_manufacturer')
    search_fields = ('name', 'brand__name',)
    list_filter = ['name', 'brand', 'brand__manufacturer', TagsFilter]
    inlines = (SeriesImageInline, SeriesBannerInline)
    prepopulated_fields = {'slug': ('name',)}

    def get_manufacturer(self, obj):
        return obj.brand.manufacturer
    get_manufacturer.short_description = 'Производитель'


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 3


class ProductBannerInline(admin.TabularInline):
    model = ProductBanner
    extra = 3



class ProductLinkInline(admin.TabularInline):
    model = ProductLink
    extra = 3



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'brand', 'series', 'get_manufacturer', 'rating')

    inlines = (ProductImageInline, ProductLinkInline, ProductBannerInline)
    search_fields = ('name', 'description')
    list_filter = ['name', 'series', 'brand__name', 'brand__manufacturer', 'price_category',
                   'prescription', 'age_recommendation', 'rating', TagsFilter]
    prepopulated_fields = {'slug': ('name',)}

    def get_manufacturer(self, obj):
        return obj.brand.manufacturer

    get_manufacturer.short_description = 'Производитель'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(PriceCategory)
class PriceCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Prescription)
class PrescriptionCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(KeyAction)
class KeyActionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(KeyAsset)
class KeyAssetAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Sex)
class SexAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(AgeRecommendation)
class AgeRecommendationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Format)
class FormatAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 3


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'product', 'rating', 'is_publish')
    list_filter = ['product', 'profile', 'is_publish']
    inlines = (ReviewImageInline, )
