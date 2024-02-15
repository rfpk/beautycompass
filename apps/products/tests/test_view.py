import json
from django.urls import reverse
from django.test import TestCase
from datetime import date, datetime
from pytils.translit import slugify
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.manufacturers.models import Manufacturer, ManufacturerTariffHistory
from apps.products.models import Product, Series, SeriesBanner, Brand, BrandBanner, \
    Review, ReviewImage, Format, KeyAsset, Category, Tag
from apps.profile.models import User, Profile, Question
from apps.services.models import Tariff, Plan


class TestCommentCase(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user(username='article@mail.ru', password='dsfsdfds')
        self.user_2 = User.objects.create_user(username='art@mail.ru', password='qwerty1')
        self.user_3 = User.objects.create_user(username='user_3@mail.ru', password='qwerty1')
        self.tariff = Tariff.objects.create(type=Plan.objects.create(period=30, quantity=50, status_start_plan=True),
                                            price=30.000)
        self.manufacturer = Manufacturer.objects.create(profile=self.user_1.user_profile, name='Test manufacturer')
        self.brand = Brand.objects.create(manufacturer=self.manufacturer, name='test brand')
        self.series = Series.objects.create(brand=self.brand, name='test series')
        self.product = Product.objects.create(series=self.series, brand=self.brand, name='product', slug='test-product')
        self.url_review = reverse('products:create_review')
        self.url_create_product = reverse('products:create_product')

    # Not Working
    # def get_test_data(self):
    #     self.form_data_1 = {
    #         'product': self.product.pk,
    #         'profile': self.user_1.user_profile.pk,
    #         'text': 'Good product!',
    #         'rating': 5,
    #     }
    #
    #     self.form_data_2 = {
    #         'product': self.product.pk,
    #         'profile': self.user_2.user_profile.pk,
    #         'text': 'Bad!',
    #         'rating': 2,
    #     }
    #
    #     self.form_data_3 = {
    #         'product': self.product.pk,
    #         'profile': self.user_3.user_profile.pk,
    #         'text': 'Ddasdasdasd!',
    #         'rating': 3,
    #     }
    #     return self.form_data_1, self.form_data_2, self.form_data_3
    #
    # def test_product_rating_value(self):
    #     self.client.login(username='art@mail.ru', password='qwerty1')
    #     data = self.get_test_data()
    #     for i in data:
    #         self.client.post(self.url_review, i)
    #     self.product.refresh_from_db()
    #     self.assertEqual(len(self.product.reviews.all()), 3)
    #     self.assertEqual(self.product.rating, 3.33)
    #     self.client.logout()


class TestProductCase(TestCommentCase):
    def setUp(self):
        self.user_1 = User.objects.create_user(username='article@mail.ru', password='dsfsdfds')
        self.user_2 = User.objects.create_user(username='art@mail.ru', password='qwerty1')
        self.user_3 = User.objects.create_user(username='user_3@mail.ru', password='qwerty1')

        self.create_manufacturer_data = {
            'name': 'Test manufacturer',
            'email': 'mypost2@gmail.com',
            'phone': '+79122220303',
        }
        self.create_brand_data = {
            'name': 'Test Brand',
            'short_description': 'Description Brand',
        }
        self.create_series_data = {
            'name': 'Test Series 2',
            'description': 'Series Description',
        }
        self.create_products_data = [
            {
                'name': 'Product One',
            },
            {
                'name': 'Product Two',
            },
            {
                'name': 'Product Three'
            }
        ]
        self.images = [
            SimpleUploadedFile("face.jpg", b"file data"),
            SimpleUploadedFile("face2.jpg", b"file data 2"),
            SimpleUploadedFile("face3.jpg", b"file data 3"),
        ]

        self.tariff = Tariff.objects.create(
            type=Plan.objects.create(period=1, quantity=1000, status_start_plan=False), price=10.00
        )
        self.manufacturer = Manufacturer.objects.create(
            profile=self.user_1.user_profile, **self.create_manufacturer_data
        )
        self.brand = Brand.objects.create(
            manufacturer=self.manufacturer, slug=slugify('Test Brand'), **self.create_brand_data
        )
        self.brand_banner = BrandBanner.objects.create(
            brand=self.brand, banner=self.images[0], url='https://google.com/10'
        )
        self.series = Series.objects.create(brand=self.brand, slug=slugify('Test Series 2'), **self.create_series_data)
        self.series_banner = SeriesBanner.objects.create(
            series=self.series, banner=self.images[0], url='https://google.com/20'
        )
        self.product = Product.objects.create(series=self.series, brand=self.brand, name='product', slug='test-product')
        self.manufacturer_tariff = ManufacturerTariffHistory.objects.create(
            manufacturer=self.manufacturer,
            tariff_plan=self.tariff,
            end_date=datetime(2030, 1, 1)
        )
        self.category = Category.objects.create(name='Category Test', slug=slugify('Category Test'))
        self.tag_one = Tag.objects.create(name='Tag One', slug=slugify('Tag One'))
        self.tag_two = Tag.objects.create(name='Tag Two', slug=slugify('Tag Two'))
        self.tag_three = Tag.objects.create(name='Tag Three', slug=slugify('Tag Three'))

        self.url_create_product = reverse('products:create_product')
        self.url_profile_detail = reverse('profile:profile_detail')
        self.url_create_brand = reverse('products:create_brand')
        self.url_sort_products_date = reverse('products:sort_products_date')
        self.url_filter_products = reverse('products:filter_products')

    def test_create_product(self):
        """test for checking correctly create product"""
        create_product_data = {
            'name': 'Test Product Name',
            'product_images-TOTAL_FORMS': '1',
            'product_images-INITIAL_FORMS': '0',
            'product_links-TOTAL_FORMS': '1',
            'product_links-INITIAL_FORMS': '0',
        }
        self.client.login(username='article@mail.ru', password='dsfsdfds')

        # =================================================================
        # ====================== Create Product Success ===================
        # =================================================================
        response = self.client.post(self.url_create_product, create_product_data)
        product = Product.objects.filter(
            brand__manufacturer__profile=self.user_1.user_profile,
            name=create_product_data['name'],
        ).first()
        self.url_update_product = reverse('products:change_product', args=[product.slug])
        # Check Response
        self.assertRedirects(response, self.url_update_product, 302,
                             target_status_code=200, fetch_redirect_response=True)
        # Check Product Data
        self.assertEqual(product.name, create_product_data['name'])

        # =================================================================
        # ====================== Create Product Error =====================
        # =================================================================
        del create_product_data['product_links-TOTAL_FORMS']
        create_product_data['name'] = 'New Product'
        response = self.client.post(self.url_create_product, create_product_data)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'status': 'error', 'message': 'The data is incorrect'}
        )
        # Check Product Doesn't Exist
        product_exist = Product.objects.filter(
            brand__manufacturer__profile=self.user_1.user_profile,
            brand=self.brand,
            series=self.series,
            name=create_product_data['name'],
        ).exists()
        self.assertFalse(product_exist)

        self.client.logout()

    def test_update_product(self):
        """test for checking correctly update product"""
        update_product_data = {
            'name': 'Test Product Name',
            'product_images-TOTAL_FORMS': '1',
            'product_images-INITIAL_FORMS': '0',
            'product_links-TOTAL_FORMS': '1',
            'product_links-INITIAL_FORMS': '0',
        }
        self.client.login(username='article@mail.ru', password='dsfsdfds')

        self.url_update_product = reverse('products:change_product', args=[self.product.slug])
        response = self.client.post(self.url_update_product, update_product_data)

        # Check Response
        self.assertRedirects(response, self.url_update_product, 302,
                             target_status_code=200, fetch_redirect_response=True)

        self.product.refresh_from_db()
        # Check Product Data
        self.assertEqual(self.product.name, update_product_data['name'])

        self.client.logout()

    def test_delete_product(self):
        """test for checking correctly delete product"""
        self.client.login(username='article@mail.ru', password='dsfsdfds')

        slug = self.product.slug
        self.url_delete_product = reverse('products:delete_product', args=[slug])
        response = self.client.post(self.url_delete_product)
        # Check Response
        self.assertRedirects(response, self.url_profile_detail, 302,
                             target_status_code=200, fetch_redirect_response=True)

        # Check Product DoesntExist
        product_exists = Product.objects.filter(slug=slug).exists()
        self.assertFalse(product_exists)

        self.client.logout()

    def test_create_brand(self):
        """test for checking correctly create brand"""
        def create_brand(status: str):
            create_brand_data = {
                'name': 'Test Brand One',
                'short_description': 'Description Brand',
                'brand_links-TOTAL_FORMS': '1',
                'brand_links-INITIAL_FORMS': '0',
                'brand_banners-TOTAL_FORMS': '1',
                'brand_banners-INITIAL_FORMS': '0',
            }
            if status == 'error':
                del create_brand_data['brand_links-TOTAL_FORMS']
            response = self.client.post(self.url_create_brand, create_brand_data)
            if status == 'success':
                self.url_change_brand = reverse(
                    'products:change_brand', args=[slugify(create_brand_data.get('name'))]
                )
                # Check Response
                self.assertRedirects(
                    response,
                    self.url_change_brand,
                    302,
                    target_status_code=200,
                    fetch_redirect_response=True
                )
                # Check Brand Data
                brand = Brand.objects.filter(
                    name=create_brand_data.get('name'),
                    manufacturer__profile=self.user_2.user_profile
                ).first()
                self.assertEqual(brand.name, create_brand_data.get('name'))
                self.assertEqual(brand.short_description, create_brand_data.get('short_description'))
            else:
                # Check Response
                self.assertJSONEqual(
                    str(response.content, encoding='utf8'),
                    {'status': 'error', 'message': 'The data is incorrect'}
                )
                # Check Brand Doesn't Exist
                brand_exist = Brand.objects.filter(
                    name=create_brand_data.get('name'),
                    manufacturer__profile=self.user_2.user_profile,
                    short_description=create_brand_data.get('short_description')
                ).exists()
                self.assertFalse(brand_exist)

        self.client.login(username='art@mail.ru', password='qwerty1')

        # Create Manufacturer
        create_manufacturer_data = {
            'name': 'Test',
            'email': 'test@gmail.com',
            'phone': '+79000220303',
        }
        Manufacturer.objects.create(
            profile=self.user_2.user_profile, **create_manufacturer_data
        )

        # Create Brand Error
        create_brand(status='error')

        # Create Brand Success
        create_brand(status='success')

        self.client.logout()

    def test_update_brand(self):
        """test for checking correctly update brand"""
        def update_brand(status: str):
            update_brand_data = {
                'name': 'Test Brand Update',
                'short_description': 'Description Brand Update',
                'brand_links-TOTAL_FORMS': '1',
                'brand_links-INITIAL_FORMS': '0',
                'brand_banners-TOTAL_FORMS': '1',
                'brand_banners-INITIAL_FORMS': '0',
            }
            if status == 'error':
                del update_brand_data['brand_links-TOTAL_FORMS']

            self.url_update_brand = reverse('products:change_brand', args=[self.brand.slug])
            response = self.client.post(self.url_update_brand, update_brand_data)
            self.brand.refresh_from_db()

            if status == 'success':
                self.url_update_brand = reverse(
                    'products:change_brand', args=[slugify(update_brand_data.get('name'))]
                )
                # Check Response
                self.assertRedirects(
                    response,
                    self.url_update_brand,
                    302,
                    target_status_code=200,
                    fetch_redirect_response=True
                )
                # Check Update Data
                self.assertEqual(self.brand.name, update_brand_data.get('name'))
                self.assertEqual(self.brand.short_description, update_brand_data.get('short_description'))
                self.assertEqual(self.brand.slug, slugify(update_brand_data.get('name')))
            else:
                # Check Response
                self.assertJSONEqual(
                    str(response.content, encoding='utf8'),
                    {'status': 'error', 'message': 'The data is incorrect'}
                )
                # Check Doesn't Update Brand
                self.assertNotEquals(self.brand.name, update_brand_data.get('name'))
                self.assertNotEquals(self.brand.short_description, update_brand_data.get('short_description'))

        self.client.login(username='article@mail.ru', password='dsfsdfds')

        # Update Brand Error
        update_brand(status='error')

        # Update Brand Success
        update_brand(status='success')

        self.client.logout()

    def test_delete_brand(self):
        """test for checking correctly delete brand"""
        self.client.login(username='article@mail.ru', password='dsfsdfds')
        # Delete Brand
        url_delete_brand = reverse('products:delete_brand', args=[self.brand.slug])
        response = self.client.post(url_delete_brand)
        # Check Redirect
        self.assertRedirects(
            response,
            self.url_profile_detail,
            302,
            target_status_code=200,
            fetch_redirect_response=True
        )
        # Check Exist Brand
        brand_exist = Brand.objects.filter(
            name=self.brand.name,
            manufacturer__profile=self.user_1.user_profile
        ).exists()
        self.assertFalse(brand_exist)

        self.client.logout()

    def test_brand_detail(self):
        """test for checking correctly detail brand page"""

        self.client.login(username='article@mail.ru', password='dsfsdfds')

        # Request Brand Detail Success
        url_detail_brand = reverse('products:brand_detail', args=[self.brand.slug])
        response = self.client.get(url_detail_brand)
        # Check Response Status
        self.assertEqual(response.status_code, 200)
        # Check Brand
        brand = response.context['brand']
        self.assertEqual(brand.name, self.brand.name)
        self.assertEqual(brand.short_description, self.brand.short_description)
        # Check Series
        series = response.context['brand_series']
        self.assertEqual(series.count(), 1)
        series = series[0]
        self.assertEqual(series.name, self.series.name)
        self.assertEqual(series.description, self.series.description)
        # Check Author
        author = response.context['author']
        self.assertEqual(author.username, self.user_1.username)
        self.assertEqual(author.user_profile, self.user_1.user_profile)
        # Check Banners
        banners = response.context['brand_banners']
        self.assertEqual(banners.count(), 1)
        banner = banners[0]
        self.assertEqual(banner.brand, self.brand)
        self.assertEqual(banner.banner, self.brand_banner.banner)
        self.assertEqual(banner.url, self.brand_banner.url)

        self.client.logout()

    def test_create_series(self):
        """test for checking correctly create series"""
        def create_series(status: str, brand_slug: str, brand_pk: int):
            create_series_data = {
                'name': 'Test Test Series',
                'description': 'Series Description',
                'series_banners-TOTAL_FORMS': '1',
                'series_banners-INITIAL_FORMS': '0',
                'brand': brand_pk
            }
            if status == 'error':
                del create_series_data['series_banners-TOTAL_FORMS']

            self.url_create_series = reverse('products:create_series', args=[brand_slug])
            response = self.client.post(self.url_create_series, create_series_data)
            if status == 'success':
                # Check Redirect
                series = Series.objects.filter(brand__manufacturer__profile=self.user_2.user_profile,
                                               name=create_series_data.get('name')).first()
                self.url_change_series = reverse('products:change_series', args=[series.slug])
                self.assertRedirects(
                    response,
                    self.url_change_series,
                    302,
                    target_status_code=200,
                    fetch_redirect_response=True
                )
                # Check Data
                self.assertEqual(series.name, create_series_data.get('name'))
                self.assertEqual(series.description, create_series_data.get('description'))
            else:
                # Check Response
                self.assertJSONEqual(
                    str(response.content, encoding='utf8'),
                    {'status': 'error', 'message': 'The data is incorrect'}
                )

                # Check Series Doesn't Exist
                series_exist = Series.objects.filter(brand__manufacturer__profile=self.user_2.user_profile).exists()
                self.assertFalse(series_exist)

        self.client.login(username='art@mail.ru', password='qwerty1')

        # Create Manufacturer
        create_manufacturer_data = {
            'name': 'Test Test',
            'email': 'testtest@gmail.com',
            'phone': '+79000220300',
        }
        manufacturer = Manufacturer.objects.create(
            profile=self.user_2.user_profile, **create_manufacturer_data
        )

        # Create Tariff
        ManufacturerTariffHistory.objects.create(
            manufacturer=manufacturer,
            tariff_plan=self.tariff,
            end_date=datetime(2030, 1, 1)
        )

        # Create Brand
        create_brand_data = {
            'name': 'Test Test Brand',
            'short_description': 'Description Brand',
        }
        brand = Brand.objects.create(
            manufacturer=manufacturer, slug=slugify('Test Test Brand'), **create_brand_data
        )

        # Create Brand Error
        create_series(status='error', brand_slug=brand.slug, brand_pk=brand.pk)

        # Create Brand Success
        create_series(status='success', brand_slug=brand.slug, brand_pk=brand.pk)

        self.client.logout()

    def test_update_series(self):
        """test for checking correctly update series"""
        def update_series(status: str):
            self.update_series_data = {
                'description': 'Series Description New',
                'series_banners-TOTAL_FORMS': '1',
                'series_banners-INITIAL_FORMS': '0',
                'brand': self.brand.pk
            }
            if status == 'error':
                del self.update_series_data['brand']

            self.url_update_series = reverse('products:change_series', args=[self.series.slug])
            response = self.client.post(self.url_update_series, self.update_series_data)
            self.series.refresh_from_db()
            if status == 'success':
                # Check Redirect
                self.assertRedirects(
                    response,
                    self.url_update_series,
                    302,
                    target_status_code=200,
                    fetch_redirect_response=True
                )
                # Check Data
                self.assertEquals(self.series.description, self.update_series_data.get('description'))
            else:
                # Check Response
                self.assertJSONEqual(
                    str(response.content, encoding='utf8'),
                    {'status': 'error', 'message': 'The data is incorrect'}
                )
                # Check Data Doesn't Change
                self.assertNotEquals(self.series.description, self.update_series_data.get('description'))

        self.client.login(username='article@mail.ru', password='dsfsdfds')

        # Update Series Error
        update_series(status='error')

        # Update Series Success
        update_series(status='success')

        self.client.logout()

    def test_delete_series(self):
        """test for checking correctly delete series"""
        self.client.login(username='article@mail.ru', password='dsfsdfds')
        # Delete Series
        url_delete_series = reverse('products:delete_series', args=[self.series.slug])
        response = self.client.post(url_delete_series)
        # Check Redirect
        self.assertRedirects(
            response,
            self.url_profile_detail,
            302,
            target_status_code=200,
            fetch_redirect_response=True
        )
        # Check Exist Series
        series_exist = Series.objects.filter(
            name=self.series.name,
            brand__manufacturer__profile=self.user_1.user_profile
        ).exists()
        self.assertFalse(series_exist)

        self.client.logout()

    def test_series_detail(self):
        """test for checking correctly detail series page"""
        self.client.login(username='article@mail.ru', password='dsfsdfds')
        # Request Series Detail Page
        url_detail_series = reverse('products:series_detail', args=[self.series.slug])
        response = self.client.get(url_detail_series)
        # Check Response Status
        self.assertEqual(response.status_code, 200)
        # Check Series
        series = response.context['series']
        self.assertEqual(series.name, self.series.name)
        self.assertEqual(series.description, self.series.description)
        # Check Banners
        banners = response.context['series_banners']
        self.assertEqual(banners.count(), 1)
        banner = banners[0]
        self.assertEqual(banner.series, self.series)
        self.assertEqual(banner.banner, self.series_banner.banner)
        self.assertEqual(banner.url, self.series_banner.url)
        # Check Products
        products = response.context['series_products']
        self.assertEqual(products.count(), 1)
        product = products[0]
        self.assertEqual(product.name, self.product.name)
        self.assertEqual(product.slug, self.product.slug)
        self.assertEqual(product.brand, self.brand)
        self.assertEqual(product.series, self.series)

        self.client.logout()

    def test_product_detail(self):
        """test for checking correctly output product detail"""
        self.client.login(username='article@mail.ru', password='dsfsdfds')

        url_product_detail = reverse('products:product_detail', args=[self.product.slug])
        response = self.client.get(url_product_detail)

        # Check Response Status
        self.assertEqual(response.status_code, 200)

        # Check Data
        context_product = response.context['product']
        self.assertEqual(self.product.name, context_product.name)
        self.assertEqual(self.product.slug, context_product.slug)
        self.assertEqual(self.product.brand, context_product.brand)
        self.assertEqual(self.product.series, context_product.series)

        self.client.logout()

    def test_create_review(self):
        """test for checking correctly create review"""
        def create_review(status: str, profile: Profile, is_author: bool):
            review_create_data = {
                'text': 'Test Text Review'
            }

            url_review_create = reverse('products:create_review', args=[self.product.pk])
            response = self.client.post(url_review_create, review_create_data)
            review = Review.objects.filter(profile=profile, product=self.product)
            if status == 'success':
                # Check Redirect
                self.assertRedirects(
                    response,
                    reverse('products:product_reviews', args=[self.product.slug]),
                    302,
                    target_status_code=200,
                    fetch_redirect_response=True
                )
                # Check Data Review
                review = review.first()
                self.assertEqual(review.product, self.product)
                self.assertEqual(review.profile, profile)
                self.assertEqual(review.text, review_create_data.get('text'))
            else:
                if is_author:
                    # Check Response
                    self.assertJSONEqual(
                        str(response.content, encoding='utf8'),
                        {
                            'status': 'error', 'message': 'Forbidden to leave a review about your own product!'
                        }
                    )

                    # Check Review Doesn't Exist
                    review_exist = review.exists()
                    self.assertFalse(review_exist)

        self.client.login(username='article@mail.ru', password='dsfsdfds')

        # Create Review Author
        create_review(status='error', profile=self.user_1.user_profile, is_author=True)
        self.client.logout()

        # Create Review User Success
        self.client.login(username='art@mail.ru', password='qwerty1')
        create_review(status='success', profile=self.user_2.user_profile, is_author=False)
        self.client.logout()

    def test_output_reviews(self):
        """test for checking correctly output reviews product"""
        def get_reviews(count: int):
            url_product_reviews = reverse('products:product_reviews', args=[self.product.slug])
            response = self.client.get(url_product_reviews)
            # Check Count
            self.assertEqual(response.context['reviews'].count(), count)
            # Check Data
            for idx, review in enumerate(response.context['reviews']):
                self.assertEqual(review.text, create_reviews_data[idx].get('text'))

        create_reviews_data = [
            {
                'text': 'Review One'
            },
            {
                'text': 'Review Two'
            },
            {
                'text': 'Review Three'
            }
        ]
        self.client.login(username='art@mail.ru', password='qwerty1')

        # Create Reviews
        for data in create_reviews_data:
            review = Review.objects.create(
                product=self.product, profile=self.user_1.user_profile, **data
            )
            review.is_publish = True
            review.save()

        self.client.logout()

        # Get Page List Reviews
        self.client.login(username='article@mail.ru', password='dsfsdfds')

        get_reviews(len(create_reviews_data))

        # Update is_publish = False
        reviews = Review.objects.filter(product=self.product, profile=self.user_1.user_profile)
        for review in reviews:
            review.is_publish = False
            review.save()

        # Check Page List Reviews
        get_reviews(0)

        self.client.logout()

    def test_output_questions(self):
        """test for checking correctly output questions product"""
        def get_questions(count: int):
            url_product_questions = reverse('products:product_questions', args=[self.product.slug])
            response = self.client.get(url_product_questions)
            # Check Count
            self.assertEqual(response.context['questions'].count(), count)
            # Check Data
            for idx, review in enumerate(response.context['questions']):
                self.assertEqual(review.text, create_questions_data[idx].get('text'))

        create_questions_data = [
            {
                'text': 'Question One'
            },
            {
                'text': 'Question Two'
            },
            {
                'text': 'Question Three'
            }
        ]

        # Create Questions
        self.client.login(username='art@mail.ru', password='qwerty1')
        for data in create_questions_data:
            Question.objects.create(product=self.product, profile=self.user_1.user_profile, **data)

        self.client.logout()

        # Get Page List Questions
        self.client.login(username='article@mail.ru', password='dsfsdfds')
        get_questions(len(create_questions_data))

        self.client.logout()

    def test_output_photos(self):
        """test for checking correctly output photos product"""
        def get_questions(count: int):
            url_product_questions = reverse('products:product_photos', args=[self.product.slug])
            response = self.client.get(url_product_questions)
            # Check Count
            self.assertEqual(response.context['photos'].count(), count)

        create_reviews_data = [
            {
                'text': 'Review One',
                'images': self.images,
            },
            {
                'text': 'Review Two',
                'images': self.images,
            },
            {
                'text': 'Review Three',
                'images': self.images,
            }
        ]

        # Create Reviews with Photos
        self.client.login(username='art@mail.ru', password='qwerty1')
        for data in create_reviews_data:
            # Save Review
            review = Review.objects.create(
                product=self.product, profile=self.user_1.user_profile, text=data.get('text')
            )
            review.is_publish = True
            review.save()

            # Save Photos
            for image in data.get('images'):
                ReviewImage.objects.create(
                    review=review,
                    image=image
                )

        self.client.logout()

        # Check Page List Questions
        get_questions(len(self.images) * len(create_reviews_data))

    def test_sort_products_date(self):
        """test for checking correctly sorting product by created_at"""
        def check_product(sort_by: str):
            response = self.client.get(self.url_sort_products_date + f'?{sort_by}')
            # Check Response
            self.assertEqual(response.status_code, 200)
            # Check Data
            product_check = [el['id'] for el in json.loads(response.content)['products']]
            order_by = '-created_at' if sort_by == 'newest' else 'created_at'
            products = list((Product.objects
                            .filter(brand__manufacturer__manufacturer_tariffs__end_date__gte=date.today())
                            .order_by(order_by)
                            .values_list('id', flat=True)))
            self.assertEqual(product_check, products)

        self.client.login(username='article@mail.ru', password='dsfsdfds')

        # Create Products
        for data in self.create_products_data:
            Product.objects.create(series=self.series, brand=self.brand, **data)

        # Check Sorting
        check_product('newest')
        check_product('oldest')

        self.client.logout()

    def test_filter_products(self):
        """test for checking correctly filter products"""
        def request_filter(count: int, category_slug: str, **kwargs):
            # Add Category
            query_params = {
                'category': category_slug
            }

            # Add Query Kwargs
            for key in kwargs:
                query_params[f'{key}[]'] = kwargs[key]

            # Request
            response = self.client.get(self.url_filter_products, query_params)
            products = json.loads(response.content)['data']
            # Check Count
            self.assertEqual(len(products), count)

        self.client.login(username='article@mail.ru', password='dsfsdfds')

        # Create Products
        key_asset = KeyAsset.objects.create(name='Key Asset Test', slug=slugify('Key Asset Test'))
        format_elem = Format.objects.create(name='Format Test', slug=slugify('Format Test'))
        for idx, data in enumerate(self.create_products_data):
            product = Product.objects.create(series=self.series, brand=self.brand, **data)
            if idx in [0, 2]:
                product.key_asset.add(key_asset)
            else:
                product.format = format_elem
            product.category.add(self.category)
            product.save()

        # Request Without Filter
        request_filter(len(self.create_products_data), self.category.slug)

        # Request With Format
        request_filter(1, self.category.slug, format=format_elem.slug)

        # Request With Key_Asset
        request_filter(2, self.category.slug, key_asset=key_asset.slug)

        # Request With Format and Key_Asset
        request_filter(0, self.category.slug, format=format_elem.slug, key_asset=key_asset.slug)

        self.client.logout()

    def test_filter_products_by_tag(self):
        """test for checking correctly filter products by tag"""
        def request_check(count: int, category_slug: str, tag_name: str):
            url_get_tags = reverse('products:product_tags', args=[category_slug, tag_name])
            response = self.client.get(url_get_tags)
            # Check Status
            self.assertEqual(response.status_code, 200)
            # Check Count
            self.assertEqual(response.context['data'].count(), count)

        # Create Products
        self.client.login(username='article@mail.ru', password='dsfsdfds')

        for idx, data in enumerate(self.create_products_data):
            product = Product.objects.create(series=self.series, brand=self.brand, **data)
            if idx == 0:
                product.tag.add(self.tag_one)
            elif idx == 1:
                product.tag.add(self.tag_two)
            else:
                product.tag.add(self.tag_three)

            product.category.add(self.category)
            product.save()

        # Check If word started with T
        request_check(count=3, category_slug=self.category.slug, tag_name='T')
        # Check If word started with Tag
        request_check(count=3, category_slug=self.category.slug, tag_name='Tag')
        # Check If word started with W
        request_check(count=1, category_slug=self.category.slug, tag_name='w')
        # Check If word started with e
        request_check(count=2, category_slug=self.category.slug, tag_name='e')

        self.client.logout()
