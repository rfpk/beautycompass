import json
from datetime import datetime
from django.test import TestCase
from django.urls import reverse
from freezegun import freeze_time
from pytils.translit import slugify
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.blog.models import Article, ArticleComment
from apps.manufacturers.models import Manufacturer, ManufacturerBanner, ManufacturerTariffHistory, ManufacturerMailing
from apps.products.mixins import ViewMixin
from apps.products.models import Brand, Series, Product, Review, ProductLink, BrandLink
from apps.profile.models import User, Author, Profile, Question
from apps.services.models import Plan, Tariff


class TestManufacturerCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='manufacturer@mail.ru', password='dsfsdfds')
        self.user_test_1 = User.objects.create_user(username='profile@mail.ru', password='dsfsdfds')
        self.user_test_2 = User.objects.create_user(username='test_2@mail.ru', password='dsfsdfds')
        self.user_test_3 = User.objects.create_user(username='test_3@mail.ru', password='dsfsdfds')

        self.create_manufacturer_data = {
            'name': 'Test',
            'email': 'test@gmail.com',
            'phone': '+79122220303',
            'manufacturer_links-TOTAL_FORMS': '1',
            'manufacturer_links-INITIAL_FORMS': '0',
            'manufacturer_banners-TOTAL_FORMS': '1',
            'manufacturer_banners-INITIAL_FORMS': '0',
        }
        self.articles = [
            {
                'title': 'Article One',
                'text': 'Text Article One',
                'slug': 'article-one'
            },
            {
                'title': 'Article Two',
                'text': 'Text Article Two',
                'slug': 'article-two'
            },
            {
                'title': 'Article Three',
                'text': 'Text Article Three',
                'slug': 'article-three'
            },
        ]
        self.questions_data = [
            {
                'text': 'Text Question One',
            },
            {
                'text': 'Text Question Two',
            },
            {
                'text': 'Text Question Three',
            },
        ]
        self.reviews_data = [
            {
                'text': 'Text Review One',
            },
            {
                'text': 'Text Review Two',
            },
            {
                'text': 'Text Review Three',
            },
        ]

        self.tariff = Tariff.objects.create(
            type=Plan.objects.create(period=30, quantity=50, status_start_plan=True), price=30.000
        )
        self.manufacturer = Manufacturer.objects.create(profile=self.user.user_profile, name='Test manufacturer')
        self.banner = ManufacturerBanner.objects.create(
            manufacturer=self.manufacturer,
            banner=SimpleUploadedFile("face.jpg", b"file data"),
            url='https://google.com/20'
        )
        self.article = Article.objects.create(manufacturer=self.manufacturer, title='adsd', text='sdasd', slug='fds')
        self.brand = Brand.objects.create(manufacturer=self.manufacturer, name='test brand', slug='test-brand')
        self.series = Series.objects.create(brand=self.brand, name='test series', slug='test-series')
        self.product = Product.objects.create(series=self.series, brand=self.brand,name='product', slug='test-product')
        self.product_link = ProductLink.objects.create(product=self.product, name='WB', url='test-url.com')
        self.brand_link = BrandLink.objects.create(brand=self.brand, name='WB', url='test-ussrl.com')
        self.brand_link_2 = BrandLink.objects.create(brand=self.brand, name='OZON', url='test-ozon.com')
        self.manufacturer_tariff = ManufacturerTariffHistory.objects.create(
            manufacturer=self.manufacturer,
            tariff_plan=self.tariff,
            end_date=datetime(2030, 1, 1)
        )
        self.url_action_product = reverse('profile:set_action', args=[self.product.slug])
        self.url_statistic_product = reverse('manufacturer:statistic_data_object',
                                             args=['product', self.product.pk])
        self.url_statistic_brand = reverse('manufacturer:statistic_data_object',
                                             args=['brand', self.brand.pk])
        self.url_statistic_article = reverse('manufacturer:statistic_data_object',
                                             args=['article', self.article.pk])

        self.url_create_manufacturer = reverse('manufacturer:manufacturer_create')
        self.url_change_manufacturer = reverse('manufacturer:change_manufacturer')
        self.url_draft_articles = reverse('manufacturer:manufacturer_drafts')
        self.url_publish_articles = reverse('manufacturer:manufacturer_publish')
        self.url_manufacturer_questions = reverse('manufacturer:manufacturer_questions')
        self.url_manufacturer_reviews = reverse('manufacturer:manufacturer_reviews')
        self.url_manufacturer_comments = reverse('manufacturer:manufacturer_comments')
        self.url_manufacturer_answer = reverse('manufacturer:manufacturer_create_answer')
        self.url_create_mailing = reverse('manufacturer:create-mailing')
        self.url_profile_detail = reverse('profile:profile_detail')

    # Create Manufacturer
    def test_create_manufacturer(self):
        """test for checking correctly create manufacturer"""
        def create_manufacturer(status: str, data: dict):
            response = self.client.post(self.url_create_manufacturer, data)
            if status == 'success':
                # Check Redirect
                self.assertRedirects(
                    response,
                    self.url_change_manufacturer,
                    302,
                    target_status_code=200,
                    fetch_redirect_response=True
                )
                # Check Data
                manufacturer = Manufacturer.objects.filter(
                    profile=self.user_test_1.user_profile,
                    name=data.get('name')
                ).first()
                self.assertEqual(manufacturer.email, data.get('email'))
                self.assertEqual(manufacturer.phone, data.get('phone'))
            else:
                self.assertJSONEqual(
                    str(response.content, encoding='utf8'),
                    {'status': 'error', 'message': 'The data is incorrect'}
                )
                # Check Manufacturer Doesn't Exist
                manufacturer_exist = Manufacturer.objects.filter(
                    profile=self.user_test_1.user_profile,
                    name=data.get('name')
                ).exists()
                self.assertFalse(manufacturer_exist)

        self.client.login(username='profile@mail.ru', password='dsfsdfds')

        # Create Manufacturer Error
        create_manufacturer(status='error', data={'name': 'Test 2'})

        # Create Manufacturer Success
        create_manufacturer(status='success', data=self.create_manufacturer_data)
        self.client.logout()

    def test_update_manufacturer(self):
        """test for checking correctly update manufacturer"""
        def manufacturer_update(status: str, data: dict):
            response = self.client.post(self.url_change_manufacturer, data)
            self.manufacturer.refresh_from_db()
            if status == 'success':
                # Check Redirect
                self.assertRedirects(
                    response,
                    self.url_change_manufacturer,
                    302,
                    target_status_code=200,
                    fetch_redirect_response=True
                )
                # Check Update Data
                self.assertEqual(self.manufacturer.name, data.get('name'))
                self.assertEqual(self.manufacturer.email, data.get('email'))
                self.assertEqual(self.manufacturer.phone, data.get('phone'))
            else:
                self.assertJSONEqual(
                    str(response.content, encoding='utf8'),
                    {'status': 'error', 'message': 'The data is incorrect'}
                )
                # Check Manufacturer Doesn't Update
                self.assertNotEquals(self.manufacturer.name, data.get('name'))

        self.client.login(username='manufacturer@mail.ru', password='dsfsdfds')

        # Create Manufacturer Error
        manufacturer_update(status='error', data={'name': 'Update Manufacturer'})

        # Create Manufacturer Success
        manufacturer_update(status='success', data=self.create_manufacturer_data)
        self.client.logout()

    def test_manufacturer_detail(self):
        """test for checking correctly manufacturer detail"""
        self.client.login(username='manufacturer@mail.ru', password='dsfsdfds')
        # Publish Article
        self.article.is_publish = True
        self.article.is_draft = False
        self.article.is_active = True
        self.article.save()
        # Request Manufacturer Detail
        url_manufacturer_detail = reverse('manufacturer:profile_manufacturer', args=[self.manufacturer.pk])
        response = self.client.get(url_manufacturer_detail)
        # Check Response Status
        self.assertEqual(response.status_code, 200)
        # Check Manufacturer
        manufacturer = response.context['manufacturer']
        self.assertEqual(manufacturer.name, self.manufacturer.name)
        self.assertEqual(manufacturer.profile, self.user.user_profile)
        # Check Banner
        banners = response.context['manufacturer_banners']
        self.assertEqual(banners.count(), 1)
        banner = banners[0]
        self.assertEqual(banner.manufacturer, self.manufacturer)
        self.assertEqual(banner.banner, self.banner.banner)
        self.assertEqual(banner.url, self.banner.url)
        # Check Articles
        articles = response.context['manufacturer_articles'].object_list
        self.assertEqual(len(articles), 1)
        article = articles[0]
        self.assertEqual(article.title, self.article.title)
        self.assertEqual(article.text, self.article.text)
        self.assertEqual(article.slug, self.article.slug)
        self.assertEqual(article.manufacturer, self.manufacturer)

        self.client.logout()

    def test_draft_articles(self):
        """test for checking correctly output draft articles"""
        def get_articles(count: int):
            response = self.client.get(self.url_draft_articles)
            articles = response.context['draft_articles']
            # Check Count
            self.assertEqual(articles.count(), count)
            # Check Data
            for context_article, article in zip(articles, self.articles):
                self.assertEqual(context_article.title, article.get('title'))
                self.assertEqual(context_article.text, article.get('text'))
                self.assertEqual(context_article.slug, article.get('slug'))

        self.client.login(username='manufacturer@mail.ru', password='dsfsdfds')

        # Create Articles
        for data in self.articles:
            Article.objects.create(
                manufacturer=self.manufacturer,
                brand=self.brand,
                is_active=True,
                is_draft=True,
                is_publish=False,
                **data
            )

        # Request Get Articles
        get_articles(len(self.articles))

        # Publish Last Element
        (Article.objects
         .filter(title='Article Three', manufacturer=self.manufacturer, brand=self.brand)
         .update(is_draft=False, is_publish=True))
        get_articles(2)

        self.client.logout()

    def test_publish_article(self):
        """test for checking correctly output publish articles"""
        def get_articles(count: int):
            response = self.client.get(self.url_publish_articles)
            articles = response.context['publish_articles']
            # Check Count
            self.assertEqual(articles.count(), count)
            # Check Data
            for context_article, article in zip(articles, self.articles):
                self.assertEqual(context_article.title, article.get('title'))
                self.assertEqual(context_article.text, article.get('text'))
                self.assertEqual(context_article.slug, article.get('slug'))

        self.client.login(username='manufacturer@mail.ru', password='dsfsdfds')

        # Create Articles
        for data in self.articles:
            Article.objects.create(
                manufacturer=self.manufacturer,
                brand=self.brand,
                is_active=True,
                is_draft=False,
                is_publish=True,
                **data
            )

        # Request Get Articles
        get_articles(len(self.articles))

        # Draft Last Element
        (Article.objects
         .filter(title='Article Three', manufacturer=self.manufacturer, brand=self.brand)
         .update(is_draft=True, is_publish=False))
        get_articles(2)

        self.client.logout()

    def test_questions_article(self):
        """test for checking correctly output questions"""

        # Create Questions
        self.client.login(username='test_2@mail.ru', password='dsfsdfds')
        for data in self.questions_data:
            Question.objects.create(
                profile=self.user_test_2.user_profile,
                product=self.product,
                **data
            )
        self.client.logout()

        # Request Get Questions
        self.client.login(username='manufacturer@mail.ru', password='dsfsdfds')
        response = self.client.get(self.url_manufacturer_questions)
        questions_context = response.context['manufacturer_questions']
        # Check Count
        self.assertEqual(questions_context.count(), len(self.questions_data))
        # Check Data
        for question_context, question in zip(questions_context, self.questions_data):
            self.assertEqual(question_context.text, question.get('text'))
            self.assertEqual(question_context.profile, self.user_test_2.user_profile)
            self.assertEqual(question_context.product, self.product)

        self.client.logout()

    def test_manufacturer_reviews(self):
        """test for checking correctly output reviews"""

        # Create Reviews
        self.client.login(username='test_2@mail.ru', password='dsfsdfds')
        for data in self.reviews_data:
            Review.objects.create(
                profile=self.user_test_2.user_profile,
                product=self.product,
                is_publish=True,
                **data
            )
        self.client.logout()

        # Request Get Reviews
        self.client.login(username='manufacturer@mail.ru', password='dsfsdfds')
        response = self.client.get(self.url_manufacturer_reviews)
        reviews = response.context['manufacturer_reviews']
        # Check Count
        self.assertEqual(reviews.count(), len(self.reviews_data))
        # Check Data
        for context_review, review in zip(reviews, self.reviews_data):
            self.assertEqual(context_review.text, review.get('text'))
            self.assertEqual(context_review.profile, self.user_test_2.user_profile)
            self.assertEqual(context_review.product, self.product)
            self.assertTrue(context_review.is_publish)

        self.client.logout()

    def test_manufacturer_comments(self):
        """test for checking correctly output comments"""
        comments_data = [
            {
                'text': 'Text Comment One'
            },
            {
                'text': 'Text Comment Two'
            },
            {
                'text': 'Text Comment Three'
            },

        ]
        # Create Comments
        self.client.login(username='test_2@mail.ru', password='dsfsdfds')
        author = Author.objects.filter(profile=self.user_test_2.user_profile).first()
        for data in comments_data:
            ArticleComment.objects.create(
                article=self.article, author=author, is_publish=True, **data
            )
        self.client.logout()

        # Request Get Comments
        self.client.login(username='manufacturer@mail.ru', password='dsfsdfds')
        response = self.client.get(self.url_manufacturer_comments)
        comments = response.context['manufacturer_comments']
        # Check Count
        self.assertEqual(comments.count(), len(comments_data))
        # Check Data
        comments_data.reverse()
        for context_comment, comment in zip(comments, comments_data):
            self.assertEqual(context_comment.text, comment.get('text'))
            self.assertEqual(context_comment.article, self.article)
            self.assertEqual(context_comment.author, author)
            self.assertTrue(context_comment.is_publish)

        self.client.logout()

    def test_manufacturer_answer(self):
        """test for checking correctly answer manufacturer"""
        def answer_request(status: str, model_name: str, text: str, question: Question = None, review: Review = None):
            data = {
                'model_name': model_name,
                'text': text,
                'question': question if question else '',
                'review': review if review else '',
            }
            response = self.client.post(self.url_manufacturer_answer, data)
            if status == 'success':
                # Check Response Status
                self.assertEqual(response.status_code, 200)
                # Check Response Content
                self.assertJSONEqual(
                    str(response.content, encoding='utf8'),
                    {
                        'status': 'success',
                        'message': 'Answer was created success!',
                        'data': {
                            'new_answer': text
                        },
                    }
                )
                # Check Data
                content = json.loads(response.content)
                self.assertEqual(content['data']['new_answer'], text)
            else:
                if model_name not in ['question', 'review']:
                    self.assertJSONEqual(
                        str(response.content, encoding='utf8'),
                        {
                            'status': 'error',
                            'message': 'There is no such model',
                        }
                    )

        # Create Questions and Reviews
        self.client.login(username='test_2@mail.ru', password='dsfsdfds')

        for question_data, review_data in zip(self.questions_data, self.reviews_data):
            profile = self.user_test_2.user_profile
            Question.objects.create(profile=profile, product=self.product, **question_data)
            Review.objects.create(profile=profile, product=self.product, is_publish=True, **review_data)

        self.client.logout()

        self.client.login(username='manufacturer@mail.ru', password='dsfsdfds')

        # Answers Questions
        questions = Question.objects.filter(profile=self.user_test_2.user_profile, product=self.product)
        for idx, question in enumerate(questions):
            answer_request(status='success', model_name='question', text=f'Answer {idx}', question=question.id)
            answer_request(status='error', model_name='test', text='')

        # Answers Reviews
        reviews = Review.objects.filter(profile=self.user_test_2.user_profile, product=self.product, is_publish=True)
        for idx, review in enumerate(reviews):
            answer_request(status='success', model_name='review', text=f'Review {idx}', review=review.id)
            answer_request(status='error', model_name='test', text='')

        self.client.logout()

    def test_create_mailing(self):
        """test for checking correctly create mailing"""
        def create_mailing(status: str):
            create_mailing_data = {
                'company_name': 'Сompany Name Test',
                'text': 'Mailing Text',
                'image': SimpleUploadedFile("image.jpg", b"file data"),
                'banner': SimpleUploadedFile("banner.jpg", b"file data"),
                'background_image': SimpleUploadedFile("background.jpg", b"file data"),
                'link_banner': 'https://google.com/11',
                'email__form-TOTAL_FORMS': '1',
                'email__form-INITIAL_FORMS': '0',
                'email__form-0-email': 'test@gmail.com',
                'phone__form-TOTAL_FORMS': '1',
                'phone__form-INITIAL_FORMS': '0',
                'phone__form-0-phone': '+79081256014'
            }
            if status == 'error':
                del create_mailing_data['email__form-TOTAL_FORMS']

            response = self.client.post(self.url_create_mailing, create_mailing_data)
            if status == 'success':
                # Check Redirect
                self.assertRedirects(response, self.url_profile_detail, 302,
                                     target_status_code=200, fetch_redirect_response=True)
                # Check Exists Mailing
                mailing_exist = ManufacturerMailing.objects.filter(
                    manufacturer=self.manufacturer,
                    company_name=create_mailing_data.get('company_name'),
                    text=create_mailing_data.get('text'),
                ).exists()
                self.assertTrue(mailing_exist)
            else:
                # Check Content
                self.assertJSONEqual(
                    str(response.content, encoding='utf8'),
                    {
                        'status': 'error',
                        'message': 'The data is incorrect',
                    }
                )
        self.client.login(username='manufacturer@mail.ru', password='dsfsdfds')

        # Add Phone to Profile
        Profile.objects.filter(user=self.user).update(phone='+79001256012')

        # Create Mailing Success
        create_mailing(status='success')

        # Create Mailing Error
        create_mailing(status='error')
        self.client.logout()

    # Doesn't Work

    # def test_manufacturer_statistic_object(self):
    #     """test for check correctly load manufacturer statistic data for charts"""
    #     # set actions user_test_1 for product
    #     with freeze_time("2023-08-25 15:00:00"):
    #         self.client.login(username='profile@mail.ru', password='dsfsdfds')
    #         response = self.client.post(self.url_action_product, {'model': 'product', 'action': 'like'})
    #         self.assertEqual(response.status_code, 200)
    #         response = self.client.post(self.url_action_product, {'model': 'product', 'action': 'favorite'})
    #         self.assertEqual(response.status_code, 200)
    #         ViewMixin.check_view_user(response.wsgi_request, self.product)
    #         self.review = Review.objects.create(product=self.product, profile=self.user.user_profile)
    #         ViewMixin.check_view_user(response.wsgi_request, self.brand_link)
    #         ViewMixin.check_view_user(response.wsgi_request, self.brand_link_2)
    #         ViewMixin.check_view_user(response.wsgi_request, self.product_link)
    #         self.client.logout()
    #
    #         # set actions user_test_2 for product
    #         self.client.login(username='test_2@mail.ru', password='dsfsdfds')
    #         response = self.client.post(self.url_action_product, {'model': 'product', 'action': 'like'})
    #         self.assertEqual(response.status_code, 200)
    #         response = self.client.post(self.url_action_product, {'model': 'product', 'action': 'favorite'})
    #         self.assertEqual(response.status_code, 200)
    #         ViewMixin.check_view_user(response.wsgi_request, self.product)
    #         self.assertEqual(self.product.get_view_count, 2)
    #         self.review = Review.objects.create(product=self.product, profile=self.user.user_profile)
    #         Product.check_conversion(self.product, response.wsgi_request,
    #                                  'series', 'test-series')
    #
    #         # set actions user_test_2 for product
    #         response = self.client.post(self.url_action_product, {'model': 'product', 'action': 'like'})
    #         self.assertEqual(response.status_code, 200)
    #         response = self.client.post(self.url_action_product, {'model': 'product', 'action': 'favorite'})
    #         self.assertEqual(response.status_code, 200)
    #         ViewMixin.check_view_user(response.wsgi_request, self.product)
    #         self.assertEqual(self.product.get_view_count, 2)
    #         self.review = Review.objects.create(product=self.product, profile=self.user.user_profile)
    #         Product.check_conversion(self.product, response.wsgi_request,
    #                                  'series', 'test-series')
    #         ViewMixin.check_view_user(response.wsgi_request, self.product_link)
    #         ArticleComment.objects.create(article=self.article, profile=self.user_test_1.user_profile, text='dasda')
    #         ArticleComment.objects.create(article=self.article, profile=self.user_test_2.user_profile, text='dasda')
    #         self.client.logout()
    #
    #     with freeze_time("2023-08-26 15:00:00"):
    #         # set actions user_test_3 for product
    #         self.client.login(username='test_3@mail.ru', password='dsfsdfds')
    #         response = self.client.post(self.url_action_product, {'model': 'product', 'action': 'like'})
    #         self.assertEqual(response.status_code, 200)
    #         response = self.client.post(self.url_action_product, {'model': 'product', 'action': 'favorite'})
    #         self.assertEqual(response.status_code, 200)
    #         ViewMixin.check_view_user(response.wsgi_request, self.product)
    #         self.assertEqual(self.product.get_view_count, 3)
    #         self.review = Review.objects.create(product=self.product, profile=self.user.user_profile)
    #         ViewMixin.check_view_user(response.wsgi_request, self.product_link)
    #         ViewMixin.check_view_user(response.wsgi_request, self.brand_link)
    #         ViewMixin.check_view_user(response.wsgi_request, self.brand_link_2)
    #         ArticleComment.objects.create(article=self.article, profile=self.user_test_3.user_profile, text='dasda')
    #         self.client.logout()
    #
    #         # set actions user_test_2 for product
    #         self.client.login(username='test_2@mail.ru', password='dsfsdfds')
    #         response = self.client.post(self.url_action_product, {'model': 'product', 'action': 'like'})
    #         self.assertEqual(response.status_code, 200)
    #         response = self.client.post(self.url_action_product, {'model': 'product', 'action': 'favorite'})
    #         self.assertEqual(response.status_code, 200)
    #         ViewMixin.check_view_user(response.wsgi_request, self.product)
    #         self.assertEqual(self.product.get_view_count, 3)
    #         self.review = Review.objects.create(product=self.product, profile=self.user.user_profile)
    #         Product.check_conversion(self.product, response.wsgi_request,
    #                                  'series', 'test-series')
    #         ViewMixin.check_view_user(response.wsgi_request, self.product_link)
    #         ViewMixin.check_view_user(response.wsgi_request, self.brand_link)
    #         ViewMixin.check_view_user(response.wsgi_request, self.brand_link_2)
    #         self.client.logout()
    #
    #     # set actions user_test_2
    #     self.client.login(username='test_2@mail.ru', password='dsfsdfds')
    #     self.client.post(self.url_action_product, {'model': 'product', 'action': 'like'})
    #     self.client.post(self.url_action_product, {'model': 'product', 'action': 'favorite'})
    #     self.client.post(self.url_action_product, {'model': 'product', 'action': 'favorite'})
    #     ArticleComment.objects.create(article=self.article, profile=self.user.user_profile, text='dasda')
    #     ViewMixin.check_view_user(response.wsgi_request, self.product_link)
    #     response_error = self.client.get(self.url_statistic_product)
    #     self.assertEqual(response_error.json()['message'],
    #                      "Current manufacturer user is not instance this objects pk")
    #     self.client.logout()
    #
    #     self.client.login(username='manufacturer@mail.ru', password='dsfsdfds')
    #     response_1 = self.client.get(self.url_statistic_product)
    #     res = response_1.json()['data']
    #
    #     res_brand = self.client.get(self.url_statistic_brand).json()['data']
    #     self.assertEqual(res_brand['links_views'][0]['total_value'], 2)
    #     self.assertEqual(res_brand['links_views'][1]['total_value'], 4)
    #
    #     res_article = self.client.get(self.url_statistic_article).json()['data']
    #     self.assertEqual(res_article['comments'][0]['value'], 2)
    #     self.assertEqual(res_article['comments'][1]['value'], 1)
    #     self.assertEqual(res_article['comments'][2]['value'], 1)
    #     res_response = {
    #            'likes': {
    #                        'day_1': res['likes'][0]['value'],
    #                        'day_2': res['likes'][1]['value'],
    #                        'day_3': res['likes'][2]['value'],
    #                     },
    #            'favorites': {
    #                        'day_1': (res['favorites'][0]['add_value'], res['favorites'][0]['remove_value']),
    #                        'day_2': (res['favorites'][1]['add_value'], res['favorites'][1]['remove_value']),
    #                        'day_3': (res['favorites'][2]['add_value'], res['favorites'][2]['remove_value']),
    #                     },
    #            'views': {
    #                        'day_1': res['views'][0]['value'],
    #                        'day_2': res['views'][1]['value'],
    #                     },
    #            'links_views': {
    #                        'day_1': res['links_views'][0]['total_value'],
    #                        'day_2': res['links_views'][1]['total_value'],
    #                     },
    #            'reviews': {
    #                        'day_1': res['reviews'][0]['value'],
    #                        'day_2': res['reviews'][1]['value'],
    #                     },
    #            'conversion': {
    #                        'day_1': res['conversion'][0]['value'],
    #                     },
    #            }
    #     expected_res = {
    #            'likes': {
    #                        'day_1': 1,
    #                        'day_2': 3,
    #                        'day_3': 2,
    #                     },
    #            'favorites': {
    #                        'day_1': (2, 1),
    #                        'day_2': (2, 0),
    #                        'day_3': (1, 1),
    #                     },
    #            'views': {
    #                        'day_1': 2,
    #                        'day_2': 1,
    #                     },
    #            'links_views': {
    #                 'day_1': 2,
    #                 'day_2': 1,
    #                     },
    #            'reviews': {
    #                        'day_1': 3,
    #                        'day_2': 2,
    #                     },
    #            'conversion': {'day_1': 1},
    #            }
    #     self.assertEqual(expected_res, res_response)
    #     self.client.logout()

    # def test_manufacturer_answer(self):
    #     self.user_review = User.objects.create_user(username='review@mail.ru', password='dsfsdfds')
    #     self.url_create_question = reverse('profile:create_question')
    #     self.create_question_data = {
    #         'product': self.product.pk,
    #         'text': 'question text example..?'
    #     }
    #
    #     self.client.login(username='review@mail.ru', password='dsfsdfds')
    #     self.client.post(self.url_create_question, self.create_question_data)
    #     question = self.user_review.user_profile.profile_questions.first()
    #     self.assertEqual(question.product, self.product)
    #     self.assertEqual(question.text, self.create_question_data['text'])
    #
    #     self.url_create_answer = reverse('manufacturer:manufacturer_create_answer')
    #     self.create_answer_data = {
    #         'model_name': 'question',
    #         'product': self.product.pk,
    #         'question': question.pk,
    #         'text': 'answer text example..?'
    #     }
    #     self.client.logout()
    #
    #     self.client.login(username='manufacturer@mail.ru', password='dsfsdfds')
    #     response = self.client.post(self.url_create_answer, self.create_answer_data)
    #     answer = question.question_answers.first()
    #     self.assertEqual(answer.product, self.product)
    #     self.assertEqual(answer.text, self.create_answer_data['text'])
    #     self.client.logout()
