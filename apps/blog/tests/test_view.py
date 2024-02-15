import datetime

from django.urls import reverse
from django.test import TestCase
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.blog.models import Article, ArticleComment, Complaint
from apps.manufacturers.models import Manufacturer
from apps.products.models import Brand, Tag
from apps.profile.models import User, Author
from apps.services.models import Tariff, Plan

from copy import deepcopy


class TestBlogCase(TestCase):

    def setUp(self):
        self.user_1 = User.objects.create_user(username='test@mail.ru', password='qwerty1')
        self.user_2 = User.objects.create_user(username='test2@mail.ru', password='qwerty1')
        self.user_article = User.objects.create_user(username='mam@mail.ru', password='dsfsdfds')

        self.article_create_data = {
            'title': 'Test title One',
            'text': 'Test text One',
            'slug': 'test-title-one',
        }

        self.complaint_title = [
            ('1', 'Хамство/грубость'),
            ('2', 'Флуд'),
            ('3', 'Нарушение УК РФ'),
            ('4', 'Реклама'),
            ('5', 'Технические проблемы'),
        ]

        self.images = [
            SimpleUploadedFile("face.jpg", b"file data"),
            SimpleUploadedFile("face2.jpg", b"file data 2"),
            SimpleUploadedFile("face3.jpg", b"file data 3"),
        ]

        self.tariff = Tariff.objects.create(type=Plan.objects.create(period=30, quantity=50, status_start_plan=True),
                                            price=30.000)
        self.manufacturer_test = Manufacturer.objects.create(profile=self.user_article.user_profile,
                                                             name='Test manufacturerer')
        self.brand_test = Brand.objects.create(manufacturer=self.manufacturer_test,
                                               name='test brandsss', slug='dsadas')
        self.tag1 = Tag.objects.create(name='test1', slug='test-1')
        self.tag2 = Tag.objects.create(name='test2', slug='test-2')
        self.tag3 = Tag.objects.create(name='test3', slug='test-3')

        manufacturer_tariff = self.manufacturer_test.manufacturer_tariffs.last()
        manufacturer_tariff.end_date = datetime.date.today() + datetime.timedelta(days=10)
        manufacturer_tariff.save()

        self.create_article_data = {
            'manufacturer': self.manufacturer_test,
            'brand': self.brand_test.pk,
            'title': 'Test title',
            'text': 'Test text',
            'tag': (self.tag1.pk, self.tag2.pk),
            # 'button_clicked': 'publish'
        }
        self.update_article_data = {
            'manufacturer': self.manufacturer_test,
            'brand': self.brand_test.pk,
            'title': 'Update title',
            'text': 'Test',
            'tag': (self.tag1.pk, self.tag2.pk, self.tag3.pk),
            # 'button_clicked': 'publish'
        }
        self.url_create_article = reverse('blog:create_article')
        self.url_list_articles = reverse('blog:articles')
        self.url_create_comment = reverse('blog:create_article_comment')
        self.url_create_complaint = reverse('blog:create_complaint')

    def test_create_update_article(self):
        """Test for correctly create/update article data"""
        self.client.login(username='mam@mail.ru', password='dsfsdfds')
        self.client.post(self.url_create_article, self.create_article_data)
        article = get_object_or_404(
            Article,
            brand=self.brand_test,
            manufacturer=self.manufacturer_test,
            text=self.create_article_data.get('text'),
            title=self.create_article_data.get('title'),
        )
        self.assertEqual(article.title, 'Test title')
        self.assertEqual(article.manufacturer, self.manufacturer_test)

        self.url_update_article = reverse('blog:update_article', kwargs={'slug': article.slug})
        self.client.post(self.url_update_article, self.update_article_data)
        article.refresh_from_db()
        self.assertEqual(article.title, 'Update title')
        self.assertEqual(len(article.tag.all()), 3)
        self.client.logout()

    def test_delete_article(self):
        """Test for correctly delete article"""

        def delete_article(status: str, is_active: bool, article_pk: int):
            url_delete_article = reverse('blog:delete_article', args=[article_pk])
            response = self.client.post(url_delete_article)
            if status == 'success':
                self.assertJSONEqual(
                    str(response.content, encoding='utf8'),
                    {'status': 'complete', 'message': 'Article success delete'}
                )
                # Check Status
                article = Article.objects.filter(pk=article_pk).first()
                self.assertFalse(article.is_active)
            else:
                if not is_active:
                    self.assertJSONEqual(
                        str(response.content, encoding='utf8'),
                        {'status': 'error', 'message': 'Article already deleted!'}
                    )
                else:
                    self.assertJSONEqual(
                        str(response.content, encoding='utf8'),
                        {'status': 'error', 'message': 'Such article not exists!'}
                    )

        self.client.login(username='mam@mail.ru', password='dsfsdfds')

        # Create Article
        article = Article.objects.create(
            manufacturer=self.manufacturer_test,
            is_draft=True,
            is_active=False,
            is_publish=False,
            **self.article_create_data,
        )

        # Delete Article Error (Not Article)
        delete_article(status='error', is_active=article.is_active, article_pk=article.pk)

        # Change Status is_active True
        article.is_active = True
        article.save()

        # Delete Article Error (Not is_active)
        delete_article(status='error', is_active=article.is_active, article_pk=100)

        # Delete Article Success
        delete_article(status='success', is_active=article.is_active, article_pk=article.pk)

        self.client.logout()

    def test_list_articles(self):
        """test for correctly output articles"""

        def request_articles(count: int):
            response = self.client.get(self.url_list_articles)
            articles = response.context['articles']
            # Check Status
            self.assertEqual(response.status_code, 200)
            # Check Count
            self.assertEqual(articles.count(), count)
            # Check Data
            for article_context, article in zip(articles, articles_create_data):
                self.assertEqual(article_context.title, article.get('title'))
                self.assertEqual(article_context.text, article.get('text'))
                self.assertEqual(article_context.slug, article.get('slug'))

        self.client.login(username='mam@mail.ru', password='dsfsdfds')
        # Create Articles
        articles_create_data = [
            {
                'title': 'Test title One',
                'text': 'Test text One',
                'slug': 'test-title-one',
            },
            {
                'title': 'Test title Two',
                'text': 'Test text Two',
                'slug': 'test-title-two',
            },
            {
                'title': 'Test title Three',
                'text': 'Test text Three',
                'slug': 'test-title-three',
            }
        ]
        for article in articles_create_data:
            Article.objects.create(
                manufacturer=self.manufacturer_test,
                brand=self.brand_test,
                is_active=True,
                is_publish=True,
                is_draft=False,
                **article
            )

        # Request Get Articles Success
        request_articles(count=len(articles_create_data))

        # Change Publish Article
        Article.objects.filter(title=articles_create_data[-1].get('title')).update(is_publish=False, is_draft=True)

        # Request Get Articles Error
        request_articles(count=len(articles_create_data) - 1)
        self.client.logout()

    def test_publish_article(self):
        """test for correctly publish/draft article"""

        def change_status(action: int, slug: str, is_draft: bool, is_publish: bool):
            is_draft = 'true' if is_draft else 'false'
            is_publish = 'true' if is_publish else 'false'

            url_change_status = reverse('blog:publish_article', args=[slug])
            response = self.client.post(url_change_status, {'is_draft': is_draft, 'is_publish': is_publish})
            # Check Response
            self.assertJSONEqual(
                str(response.content, encoding='utf8'),
                {'status': 'complete', 'message': 'Article Update Success'}
            )
            # Check Change Status
            article = Article.objects.filter(slug=slug).first()
            if action == 1:
                # Check Published Article
                self.assertTrue(article.is_active)
                self.assertFalse(article.is_draft)
                self.assertTrue(article.is_publish)
            else:
                # Check Drafted Article
                self.assertTrue(article.is_active)
                self.assertTrue(article.is_draft)
                self.assertFalse(article.is_publish)

        self.client.login(username='mam@mail.ru', password='dsfsdfds')
        # Create Article
        Article.objects.create(
            manufacturer=self.manufacturer_test,
            is_draft=True,
            is_active=True,
            is_publish=False,
            **self.article_create_data,
        )

        # Publish Article
        change_status(1, self.article_create_data.get('slug'), is_draft=False, is_publish=True)
        # Draft Article
        change_status(2, self.article_create_data.get('slug'), is_draft=True, is_publish=False)

        self.client.logout()

    def test_detail_article(self):
        """test for correctly check detail article"""

        def check_article(status: str):
            url_article_detail = reverse('blog:article_detail', args=[self.article_create_data.get('slug')])
            response = self.client.get(url_article_detail)
            if status == 'success':
                # Check Status
                self.assertEqual(response.status_code, 200)
                # Check Data
                article = response.context['article']
                self.assertEqual(article.title, self.article_create_data.get('title'))
                self.assertEqual(article.text, self.article_create_data.get('text'))
                self.assertEqual(article.slug, self.article_create_data.get('slug'))
                self.assertEqual(article.manufacturer, self.manufacturer_test)
                self.assertTrue(article.is_active)
                self.assertIn('complaint_form', response.context)
            else:
                # Check Status
                self.assertEqual(response.status_code, 404)

        self.client.login(username='mam@mail.ru', password='dsfsdfds')

        # Create Article
        article = Article.objects.create(
            manufacturer=self.manufacturer_test,
            is_draft=True,
            is_active=True,
            is_publish=False,
            **self.article_create_data,
        )
        # Request Detail Article If Draft Article (Author)
        check_article(status='success')
        self.client.logout()

        # Request Detail Article If Draft Article (User)
        self.client.login(username='test@mail.ru', password='qwerty1')
        check_article(status='error')
        self.client.logout()

        # Publish Article
        self.client.login(username='mam@mail.ru', password='dsfsdfds')
        article.is_draft = False
        article.is_publish = True
        article.save()

        # Request Detail Article If Publish Article (User)
        check_article(status='success')
        self.client.logout()

        # Request Detail Article If Publish Article (User)
        self.client.login(username='test@mail.ru', password='qwerty1')
        check_article(status='success')
        self.client.logout()

    def test_create_comment(self):
        """Test for correctly create comment"""

        def create_comment(status: str, article_id: int):
            create_comment_data = {
                'article_id': article_id,
                'text': 'Test Comment Text',
                'images': self.images
            }
            if status == 'error':
                del create_comment_data['article_id']
            response = self.client.post(self.url_create_comment, create_comment_data)
            if status == 'success':
                # Check Response
                self.assertJSONEqual(
                    str(response.content, encoding='utf8'),
                    {'status': 'success', 'message': 'New comment saved success!'}
                )
                # Check Comment Exist
                author = Author.objects.filter(profile=self.user_1.user_profile).first()
                comment_exist = ArticleComment.objects.filter(
                    article__pk=article_id,
                    author=author
                ).exists()
                self.assertTrue(comment_exist)
            else:
                # Check Response
                self.assertJSONEqual(
                    str(response.content, encoding='utf8'),
                    {'status': 'error', 'message': 'Form is a not valid'}
                )

        # Create Article
        self.client.login(username='mam@mail.ru', password='dsfsdfds')
        article = Article.objects.create(
            manufacturer=self.manufacturer_test,
            is_draft=False,
            is_active=True,
            is_publish=True,
            **self.article_create_data,
        )
        self.client.logout()

        self.client.login(username='test@mail.ru', password='qwerty1')

        # Create Comment Success
        create_comment(status='success', article_id=article.pk)

        # Create Comment Error
        create_comment(status='error', article_id=article.pk)

        self.client.logout()

    def test_create_complaint(self):
        """Test for correctly create compaint"""

        def create_complaint(status: str, count: int, data: dict):
            if status == 'error':
                del data['title']
            response = self.client.post(self.url_create_complaint, data)
            if status == 'success':
                # Check Status
                self.assertEqual(response.status_code, 200)
                # Check Response
                self.assertJSONEqual(
                    str(response.content, encoding='utf8'),
                    {'status': 'success', 'message': 'New complaint saved success!'}
                )
                # Check Exists
                complaint = Complaint.objects.filter(
                    content_type=ContentType.objects.get_for_model(ArticleComment)
                )
                self.assertTrue(complaint.exists())
                # Check Count
                self.assertEqual(complaint.count(), count)
                # Check Data
                complaint = complaint.filter(text=data.get('text')).first()
                self.assertEqual(complaint.title, self.complaint_title[int(data.get('title')) - 1][-1])
                self.assertEqual(complaint.text, data.get('text'))
                self.assertEqual(complaint.profile, self.user_2.user_profile)
            else:
                # Check Response
                self.assertJSONEqual(
                    str(response.content, encoding='utf8'),
                    {'status': 'error', 'message': 'Form is a not valid'}
                )

        self.client.login(username='mam@mail.ru', password='dsfsdfds')

        # Create Article
        article = Article.objects.create(
            manufacturer=self.manufacturer_test,
            is_draft=False,
            is_active=True,
            is_publish=True,
            **self.article_create_data,
        )
        self.client.logout()

        # Create Comments
        self.client.login(username='test@mail.ru', password='qwerty1')
        author = Author.objects.filter(profile=self.user_1.user_profile).first()

        create_comments_data = [
            ArticleComment(article=article, author=author, text=f'Test Comment {num}') for num in range(1, 4)
        ]
        ArticleComment.objects.bulk_create(create_comments_data)

        # Check Count Comments
        comments_count = ArticleComment.objects.filter(article=article, author=author).count()
        self.assertEqual(comments_count, len(create_comments_data))
        self.client.logout()

        # Create Complaints
        self.client.login(username='test2@mail.ru', password='qwerty1')

        create_complaint_data = {
            'title': '1',
            'text': 'Complaint One',
            'object_id': 1,
            'object_type': '1'
        }

        create_complaint(status='success', count=1, data=create_complaint_data)

        create_complaint(status='error', count=1, data=create_complaint_data)

        self.client.logout()

    def test_get_new_comments_count(self):
        """Test for correctly get count new comments"""

        def get_comments(status: str, data: dict = None, count: int = None):
            url_get_comments = reverse('blog:get_new_comments', args=[article.pk])
            response = None
            if status == 'get request':
                response = self.client.get(url_get_comments)
            else:
                response = self.client.post(url_get_comments, data)

            match status:
                case 'success':
                    # Check Status
                    self.assertEqual(response.status_code, 200)
                    # Check Context
                    self.assertTrue(response.context['comment'])
                case 'not found':
                    # Check Response
                    self.assertEqual(response.status_code, 404)
                case 'get request':
                    self.assertRedirects(response, reverse('profile:profile_detail'),
                        302, target_status_code=200, fetch_redirect_response=True)
                case 'error':
                    # Check Response
                    self.assertJSONEqual(
                        str(response.content, encoding='utf8'),
                        {'status': 'error', 'message': 'The data is incorrect'}
                    )
                case _:
                    pass

        def check_count(status: str, count: int, data: dict):
            url_check_count = reverse('blog:get_new_comments_count', args=[article.pk])
            if status == 'error':
                del data['object_type']

            response = self.client.post(url_check_count, data)
            # Check Status
            self.assertEqual(response.status_code, 200)
            if status == 'success':
                # Check Response
                self.assertJSONEqual(
                    str(response.content, encoding='utf8'),
                    {
                        'status': 'success',
                        'message': 'Success Get Count Comments',
                        'data': count
                    }
                )
            else:
                self.assertJSONEqual(
                    str(response.content, encoding='utf8'),
                    {
                        'status': 'error',
                        'message': 'The data is incorrect'
                    }
                )

        # Create Article
        self.client.login(username='mam@mail.ru', password='dsfsdfds')
        article = Article.objects.create(
            manufacturer=self.manufacturer_test, is_draft=False, is_active=True,
            is_publish=True,
            **self.article_create_data,
        )
        self.client.logout()

        # Create Comments
        self.client.login(username='test@mail.ru', password='qwerty1')
        author = Author.objects.filter(profile=self.user_1.user_profile).first()

        create_comments_data = [
            ArticleComment(article=article, author=author, text=f'Test Comment {num}') for num in range(1, 4)
        ]
        comments = ArticleComment.objects.bulk_create(create_comments_data)
        comments = [comment.pk for comment in comments]
        self.client.logout()

        # Check Count Comments
        check_count_data = {'objects_id[]': deepcopy(comments), 'object_type': '1'}
        self.client.login(username='test2@mail.ru', password='qwerty1')

        # Check All Comments
        check_count(
            status='success',
            count=0,
            data=check_count_data
        )

        # Check If Read Two Comments
        del check_count_data['objects_id[]'][0]
        check_count(status='success', count=1, data=check_count_data)

        # Check If Not Read Comments
        check_count_data['objects_id[]'] = []
        check_count(status='success', count=3, data=check_count_data)

        # Error Invalid Data
        check_count( status='error', count=0, data=check_count_data)

        # Check Get Comments Error
        get_comments(status='error', data=check_count_data)
        check_count_data = {'objects_id[]': comments, 'object_type': '1'}

        # Check Get Comments Error Not Found New comments
        get_comments(status='not found', data=check_count_data)

        # Check Get Comments Error Get Request
        get_comments(status='get request')

        # Check Get Comments Success
        del check_count_data['objects_id[]'][0]
        get_comments(status='success', data=check_count_data, count=1)

        self.client.logout()
