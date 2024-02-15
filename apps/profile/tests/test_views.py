from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.urls import reverse
from freezegun import freeze_time

from apps.blog.models import Article
from apps.manufacturers.models import Manufacturer
from apps.products.mixins import ViewMixin
from apps.products.models import Brand, Series, Product, Review
from apps.profile.models import User, Profile, Author, Appeal, AuthorHistory, Overview, OverviewComment
from apps.services.models import Tariff, Plan
from apps.tools.database_operations import ADD, REMOVE
from django.core.files.uploadedfile import SimpleUploadedFile


class TestProfileCase(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user(username='article@mail.ru', password='dsfsdfds')
        self.user_2 = User.objects.create_user(username='art@mail.ru', password='qwerty1')
        self.user_3 = User.objects.create_user(username='user_3@mail.ru', password='qwerty1')

        Author.objects.filter(profile__user=self.user_3).update(type=Author.AuthorType.AUTHOR)

        self.author = self.user_3.user_profile.profile_author.first()
        self.user_test = User.objects.create_user(username='test@mail.ru', password='qwerty1')
        self.update_user_data = {
            'email': self.user_test.username,
            'contact_email': self.user_test.username,
            'first_name': 'Profile name',
            'last_name': 'Profile last name',
            'phone': '+79504455490',
            'sex': 'M',
        }
        self.sorting_by = [
            {'value': 'created_at', 'text': 'Сначала новые'},
            {'value': '-created_at', 'text': 'Сначала старые'},
            {'value': 'title', 'text': 'По названию (А-Я)'},
            {'value': '-title', 'text': 'По названию (Я-А)'}
        ]
        self.create_overview_data = {
            'title': 'title overview',
            'description': 'test',
            'thumbnail': SimpleUploadedFile("face.jpg", b"file data"),
        }
        self.create_chat_data = {
            'title': 'Title test',
            'text': 'Text test',
        }
        # self.tariff = Tariff.objects.create(type=Plan.objects.create(period=30, quantity=50, status_start_plan=True),
        #                                     price=30.000)
        self.manufacturer = Manufacturer.objects.create(profile=self.user_1.user_profile, name='Test manufacturer')
        self.brand = Brand.objects.create(manufacturer=self.manufacturer, name='test brand')
        self.series = Series.objects.create(brand=self.brand, name='test series')
        self.product = Product.objects.create(series=self.series, brand=self.brand, name='product', slug='test-product')

        self.article = Article.objects.create(manufacturer=self.manufacturer, title='test article',
                                              text='test text', slug='test-slug')
        self.review = Review.objects.create(product=self.product, profile=self.user_1.user_profile)

        self.url_action_article = reverse('profile:set_action', args=[self.article.slug])
        self.url_action_product = reverse('profile:set_action', args=[self.product.slug])
        self.url_action_like_review = reverse('products:review_like', args=[self.review.pk])
        self.url_action_dislike_review = reverse('products:review_dislike', args=[self.review.pk])
        self.url_detail_profile = reverse('profile:profile_detail')
        self.url_update_profile = reverse('profile:change_profile')
        self.url_delete_profile = reverse('profile:delete_profile')
        self.url_create_overview = reverse('profile:create_overview')
        self.url_list_draft_author_overviews = reverse('profile:author_drafts')
        self.url_list_publish_author_overviews = reverse('profile:author_publish')
        self.url_list_publish_overview = reverse('profile:list_overviews')
        self.url_create_overview_comment = reverse('profile:create_overview_comment')

        self.url_chats_profile = reverse('profile:profile_chats')
        self.url_create_chat = reverse('chats:create_message')
        self.url_create_appeal = reverse('profile:create_appeal')
        self.url_get_appeals = reverse('profile:profile_appeals')
        self.url_search_by_nickname = reverse('profile:search_author')
        self.url_comments_overview = reverse('profile:profile_comments')
        self.url_create_product = reverse('products:create_product')
        # self.url_create_manufacturer = reverse('')

    # PROFILE
    def test_change_data_profile(self):
        """test for checking correctly update data of profile"""
        self.client.login(username='test@mail.ru', password='qwerty1')
        response = self.client.post(self.url_update_profile, self.update_user_data)
        # self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'status': 'success', 'message': 'Profile data was changed'}
        )
        self.user_test.user_profile.refresh_from_db()
        self.assertEqual(self.user_test.user_profile.phone, '+79504455490')
        self.assertEqual(self.user_test.user_profile.first_name, 'Profile name')
        self.assertEqual(self.user_test.user_profile.last_name, 'Profile last name')
        self.client.logout()

    def test_change_data_profile_error_incorrect_data(self):
        """test to check if not all data is transferred an error will be returned"""
        data = self.update_user_data
        data.pop('sex')
        self.client.login(username='test@mail.ru', password='qwerty1')
        response = self.client.post(self.url_update_profile, data)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'status': 'error', 'message': 'The data is incorrect'}
        )
        self.user_test.user_profile.refresh_from_db()
        self.assertEqual(self.user_test.user_profile.phone, None)
        self.assertEqual(self.user_test.user_profile.first_name, '')
        self.assertEqual(self.user_test.user_profile.last_name, '')
        self.client.logout()

    def test_delete_profile(self):
        """test to check correctly delete profile"""
        self.client.login(username='test@mail.ru', password='qwerty1')
        response = self.client.delete(self.url_delete_profile)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'status': 'complete', 'message': 'The profile delete'}
        )
        self.user_test.user_profile.refresh_from_db()
        self.assertFalse(self.user_test.user_profile.is_active)
        self.client.logout()

    def test_profile_detail(self):
        """test to check output profile detail view"""

        def check_data(type_: str, context: list):
            if type_ == Author.AuthorType.AUTHOR:
                self.assertNotIn('form', context)
                self.assertNotIn('profile', context)
            else:
                self.assertIn('form', context)
                self.assertIn('profile', context)
                # Check Profile
                profile = Profile.objects.filter(user=self.user_3).first()
                self.assertEqual(context['profile'], profile)

        # Request Profile Page with Author
        self.client.login(username='user_3@mail.ru', password='qwerty1')
        response = self.client.get(self.url_detail_profile)
        check_data(self.author.type, response.context)

        # Request Profile Page with Reader
        self.author.type = Author.AuthorType.READER
        self.author.save()
        self.author.refresh_from_db()
        response = self.client.get(self.url_detail_profile)
        check_data(self.author.type, response.context)

        self.client.logout()

    def test_profile_create_appeal(self):
        """test to check output profile create appeal view"""

        def create_appeal(status: str):
            response = self.client.post(self.url_create_appeal, self.create_appeal_data)
            if status == 'success':
                self.assertRedirects(
                    response,
                    self.url_get_appeals,
                    302,
                    target_status_code=200,
                    fetch_redirect_response=True
                )
            else:
                self.assertJSONEqual(
                    str(response.content, encoding='utf8'),
                    {'status': 'error', 'message': 'The data is incorrect'}
                )

        self.client.login(username='user_3@mail.ru', password='qwerty1')
        # Create Appeal
        self.create_appeal_data = {
            'title': 'Test Title',
            'text': 'Test Text',
            'subject_appeal': 'TS',
        }
        create_appeal(status='success')
        # Create Appeal Invalid Data
        del self.create_appeal_data['subject_appeal']
        create_appeal(status='invalid')
        self.client.logout()

    def test_list_appeals(self):
        """test to check correctly output appeals"""

        def check_appeals(count: int = 0, type_appeal: str = None):
            response = self.client.get(self.url_get_appeals)
            self.assertEqual(response.context['appeals'].count(), count)
            if count:
                appeal = response.context['appeals'][count - 1]
                self.assertEqual(appeal.title, self.create_appeal_data['title'])
                self.assertEqual(appeal.text, self.create_appeal_data['text'])
                self.assertEqual(appeal.subject_appeal, type_appeal)

        def create_appeal():
            response = self.client.post(self.url_create_appeal, self.create_appeal_data)
            self.assertRedirects(response, self.url_get_appeals, 302,
                                 target_status_code=200, fetch_redirect_response=True)

        self.client.login(username='user_3@mail.ru', password='qwerty1')
        # Get Appeal Without Create
        check_appeals()
        # Get Appeals With Data
        self.create_appeal_data = {
            'title': 'Test Title',
            'text': 'Test Text',
            'subject_appeal': 'LF',
        }
        create_appeal()
        check_appeals(1, Appeal.AppealType.LEGAL_FINANCE)

        # Check Subject Appeal Type

        # QUESTION_SUGGEST
        self.create_appeal_data['subject_appeal'] = Appeal.AppealType.QUESTION_SUGGEST
        create_appeal()
        check_appeals(2, Appeal.AppealType.QUESTION_SUGGEST)
        # TECH_SUPPORT
        self.create_appeal_data['subject_appeal'] = Appeal.AppealType.TECH_SUPPORT
        create_appeal()
        check_appeals(3, Appeal.AppealType.TECH_SUPPORT)

        self.client.logout()

    def test_search_by_nickname_view(self):
        """Test for correctly get users by nickname"""

        def request_get_nickname(count: int, nickname: str, period: str = '', type_: str = ''):
            url = f'{self.url_search_by_nickname}?nickname={nickname}'
            url += f'&period={period}' if period else f'&type={type_}' if type_ else ''
            response = self.client.get(url)
            self.assertEqual(len(response.context['data']), count)
            for author in response.context['data']:
                if isinstance(author, dict):
                    self.assertIn(nickname, author['author'].profile.nickname)
                else:
                    self.assertIn(nickname, author.profile.nickname)

        def change_type_author(type_: str):
            users = [self.user_1, self.user_2]
            for idx, user in enumerate(users):
                Author.objects.filter(profile__user=user).update(type=type_)
                Profile.objects.filter(user=user).update(nickname=f'Test {idx}')

        self.client.login(username='user_3@mail.ru', password='qwerty1')

        nickname = 'Test'
        # Request Total Period
        change_type_author(type_=Author.AuthorType.AUTHOR)
        request_get_nickname(2, nickname, 'total')

        # Request Reader Period Without Change Type
        request_get_nickname(0, nickname, 'readers')

        # Request Total Period With Change Type
        change_type_author(type_=Author.AuthorType.READER)
        request_get_nickname(0, nickname, 'total')

        # Request Readers Period
        request_get_nickname(2, nickname, 'readers')

        # Request with type
        request_get_nickname(2, nickname, type_='test')

        # Request with type and Other Nickname
        request_get_nickname(0, 'Best', type_='test')

        self.client.logout()

    # OVERVIEW
    def test_create_update_overview(self):
        """Test for correctly create/update overview data"""
        self.update_overview_data = {
            'title': 'title overview',
            'description': 'update',
        }

        self.client.login(username='user_3@mail.ru', password='qwerty1')
        # Create
        response = self.client.post(self.url_create_overview, self.create_overview_data)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'redirect': self.url_list_publish_overview}
        )
        overview = get_object_or_404(Overview, title=self.create_overview_data.get('title'))
        self.assertEqual(overview.title, 'title overview')
        self.assertEqual(overview.slug, 'title-overview')

        # Update
        self.url_update_overview = reverse('profile:update_overview', args=[overview.slug])
        response = self.client.post(self.url_update_overview, self.update_overview_data)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'redirect': self.url_list_publish_overview}
        )
        overview.refresh_from_db()
        self.assertEqual(overview.description, self.update_overview_data.get('description'))
        self.client.logout()

    def test_create_update_overview_block_author(self):
        """Test the creating and updating overview if author block"""
        self.client.login(username='user_3@mail.ru', password='qwerty1')
        statuses = [AuthorHistory.AuthorStatus.BLOCKED_UNTIL, AuthorHistory.AuthorStatus.BLOCKED_FOREVER]

        for idx, status in enumerate(statuses):
            author = AuthorHistory.objects.filter(author=self.author)
            author.update(current_status=status)
            self.author.refresh_from_db()
            response_create = self.client.post(self.url_create_overview)
            response_update = self.client.post(reverse('profile:update_overview', args=[1]))
            self.assertJSONEqual(
                str(response_create.content, encoding='utf8'),
                {'status': 'error', 'message': 'Author has a block status'}
            )
            self.assertJSONEqual(
                str(response_update.content, encoding='utf8'),
                {'status': 'error', 'message': 'Author has a block status'}
            )

        self.client.logout()

    def test_delete_overview(self):
        """test to check correctly delete overview"""

        def request_delete(overview_id: int, type_: str) -> None:
            self.url_delete_overview = reverse('profile:delete_overview', args=[overview_id])
            response = self.client.delete(self.url_delete_overview)
            if type_ == 'success':
                self.assertJSONEqual(
                    str(response.content, encoding='utf8'),
                    {'status': 'complete', 'message': 'Overview success delete'}
                )
            elif type_ == 'repeat':
                self.assertJSONEqual(
                    str(response.content, encoding='utf8'),
                    {'status': 'error', 'message': 'Overview already deleted!'}
                )
            else:
                self.assertJSONEqual(
                    str(response.content, encoding='utf8'),
                    {'status': 'error', 'message': 'Such overview not exists!'}
                )

        self.client.login(username='test@mail.ru', password='qwerty1')
        # Create
        response = self.client.post(self.url_create_overview, self.create_overview_data)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'redirect': self.url_list_publish_overview}
        )
        overview = get_object_or_404(Overview, title=self.create_overview_data.get('title'))
        overview.is_active = True
        overview.save()
        overview.refresh_from_db()
        # Delete
        request_delete(overview.pk, 'success')
        # Check Delete Overview
        overview.refresh_from_db()
        self.assertFalse(overview.is_active)
        # Delete request Repeat Delete
        request_delete(overview.pk, 'repeat')
        # Delete request don't exist Overview
        request_delete(100, 'exist')
        self.client.logout()

    def test_list_overviews_output_context(self):
        """testing for correctly output list overviews published"""

        def check_sortings_by(tags: list) -> None:
            for idx, tag in enumerate(tags):
                self.assertEqual(tag, self.sorting_by[idx])

        def check_list_overview(count: int) -> None:
            res = self.client.get(self.url_list_publish_overview)
            # Check Count QuerySet
            self.assertEqual(res.context['overviews'].count(), count)
            self.assertEqual(res.context['selection_banners'].count(), 0)
            self.assertEqual(res.context['tags'].count(), 0)
            # Check Sorting_by
            check_sortings_by(res.context['sortings_by'])
            if count == 3:
                # Check Data
                for idx, overview in enumerate(res.context['overviews']):
                    self.assertEqual(overview.title, self.create_overviews_data[idx]['title'])
                    self.assertEqual(overview.description, self.create_overviews_data[idx]['description'])

        self.create_overviews_data = [
            {
                'title': 'title overview',
                'description': 'test',
                'thumbnail': SimpleUploadedFile("face.jpg", b"file data"),
            },
            {
                'title': 'title overview 2',
                'description': 'test 2',
                'thumbnail': SimpleUploadedFile("face2.jpg", b"file data2"),
            },
            {
                'title': 'title overview 3',
                'description': 'test 3',
                'thumbnail': SimpleUploadedFile("face3.jpg", b"file data3"),
            }
        ]
        self.client.login(username='user_3@mail.ru', password='qwerty1')

        # Create
        for overview in self.create_overviews_data:
            response = self.client.post(self.url_create_overview, overview)
            self.assertJSONEqual(
                str(response.content, encoding='utf8'),
                {'redirect': self.url_list_publish_overview}
            )
            # Publish Article
            overview = get_object_or_404(Overview, title=overview.get('title'))
            overview.is_publish = True
            overview.is_active = True
            overview.save()
            overview.refresh_from_db()

        # Request List Overview
        check_list_overview(3)

        # Change Publish to Draft
        for overview in self.create_overviews_data:
            overview = get_object_or_404(Overview, title=overview.get('title'))
            overview.is_publish = False
            overview.is_draft = True
            overview.save()
            overview.refresh_from_db()

        # Request List Overview
        check_list_overview(0)

        self.client.logout()

    def test_detail_overview_output_context(self):
        """testing for correctly output detail overview published"""

        def check_overview(is_publish: bool = True) -> None:
            self.url_detail_overview = reverse('profile:detail_overview', args=[overview.slug])
            res = self.client.get(self.url_detail_overview)
            if is_publish:
                # Check Count
                self.assertEqual(res.context['selection_banners'].count(), 0)
                # Check Form
                self.assertIn('complaint_form', res.context)
                # Check Overview
                self.assertEqual(res.context['overview'].title, self.create_overview_data['title'])
                self.assertEqual(res.context['overview'].description, self.create_overview_data['description'])
            else:
                self.assertEqual(res.status_code, 404)

        self.client.login(username='user_3@mail.ru', password='qwerty1')

        response = self.client.post(self.url_create_overview, self.create_overview_data)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'redirect': self.url_list_publish_overview}
        )
        # Publish Article
        overview = get_object_or_404(Overview, title=self.create_overview_data.get('title'))
        overview.is_publish = True
        overview.is_active = True
        overview.save()
        overview.refresh_from_db()

        # Request Detail Overview
        check_overview(is_publish=True)

        # Change Publish to Draft
        overview.is_publish = False
        overview.is_draft = True
        overview.save()
        overview.refresh_from_db()

        # Request Detail Overview
        check_overview(is_publish=False)

    def test_create_overview_comment(self):
        """testing for correctly create comment overview"""

        def create_comment(type_: str, data: dict, overview: Overview, author: Author) -> OverviewComment:
            res = self.client.post(self.url_create_overview_comment, data)
            if type_ == 'create':
                self.assertJSONEqual(
                    str(res.content, encoding='utf8'),
                    {'status': 'success', 'message': 'New comment saved success!'}
                )
                overview_comment = get_object_or_404(OverviewComment, overview=overview, author=author)
                self.assertEqual(overview_comment.text, data.get('text'))
                self.assertEqual(overview_comment.overview, overview)
                self.assertEqual(overview_comment.author, author)
                return overview_comment
            else:
                self.assertJSONEqual(
                    str(res.content, encoding='utf8'),
                    {'status': 'error', 'message': 'Form is a not valid'}
                )

        self.client.login(username='user_3@mail.ru', password='qwerty1')
        # Create Overview
        response = self.client.post(self.url_create_overview, self.create_overview_data)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'redirect': self.url_list_publish_overview}
        )
        overview = get_object_or_404(Overview, title=self.create_overview_data.get('title'))

        # Create Comment
        create_comment_data = {'text': 'Comment One', 'overview': overview.pk}
        comment = create_comment('create', create_comment_data, overview, self.author)
        self.client.logout()

        # Create Comment Reply
        self.client.login(username='article@mail.ru', password='dsfsdfds')
        author = Author.objects.filter(profile=self.user_1.user_profile).first()

        create_comment_data['parent'] = comment.pk
        create_comment_data['text'] = 'Comment Two'
        create_comment('create', create_comment_data, overview, author)
        self.client.logout()

        # Create Comment Invalid Data
        self.client.login(username='art@mail.ru', password='qwerty1')
        author = Author.objects.filter(profile=self.user_2.user_profile).first()
        create_comment_data['parent'] = 'test'
        create_comment('invalid', create_comment_data, overview, author)
        self.client.logout()

    def test_create_overview_block_author(self):
        """Test the creating comment overview if author block"""
        self.client.login(username='user_3@mail.ru', password='qwerty1')
        statuses = [AuthorHistory.AuthorStatus.BLOCKED_UNTIL, AuthorHistory.AuthorStatus.BLOCKED_FOREVER]

        # Create Overview
        response = self.client.post(self.url_create_overview, self.create_overview_data)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'redirect': self.url_list_publish_overview}
        )
        for idx, status in enumerate(statuses):
            # Change Status history Author
            author = AuthorHistory.objects.filter(author=self.author)
            author.update(current_status=status)
            self.author.refresh_from_db()
            # Create Comment
            response = self.client.post(self.url_create_overview_comment)
            self.assertJSONEqual(
                str(response.content, encoding='utf8'),
                {'status': 'error', 'message': 'Current author has block status'}
            )

        self.client.logout()

    def test_list_overviews_draft_and_publish(self):
        """test to check correctly output overviews draft and publish"""
        create_overviews_data = [
            {
                'title': 'title overview 1',
                'description': 'test 1',
                'thumbnail': SimpleUploadedFile("face1.jpg", b"file data"),
            },
            {
                'title': 'title overview 2',
                'description': 'test 2',
                'thumbnail': SimpleUploadedFile("face2.jpg", b"file data"),
            },
            {
                'title': 'title overview 3',
                'description': 'test 3',
                'thumbnail': SimpleUploadedFile("face3.jpg", b"file data"),
            },
        ]
        self.client.login(username='user_3@mail.ru', password='qwerty1')

        def change_draft(is_draft: bool, is_publish: bool, overview: Overview):
            overview.is_active = True
            overview.is_draft = is_draft
            overview.is_publish = is_publish
            overview.save()
            overview.refresh_from_db()

        def check_output(type_: str, count: int):
            url = self.url_list_draft_author_overviews if type_ == 'draft' else self.url_list_publish_author_overviews
            context = 'draft_overviews' if type_ == 'draft' else 'publish_overviews'

            res = self.client.get(url)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.context[context].count(), count)

        # Create Overviews
        for data in create_overviews_data:
            response = self.client.post(self.url_create_overview, data)
            self.assertJSONEqual(
                str(response.content, encoding='utf8'),
                {'redirect': self.url_list_publish_overview}
            )
            overview = get_object_or_404(Overview, title=data.get('title'))
            change_draft(is_draft=True, is_publish=False, overview=overview)

        # Check Draft List
        check_output('draft', len(create_overviews_data))

        # Edit One Overview is_draft
        overview = get_object_or_404(Overview, title=create_overviews_data[0].get('title'))
        change_draft(is_draft=False, is_publish=True, overview=overview)
        # Check Draft List
        check_output('draft', len(create_overviews_data) - 1)
        # Check Publish List
        check_output('publish', 1)

    def test_change_draft_publish_overview(self):
        """test view for update draft and publish"""

        def change_overview(status: str, slug: str, data: dict):
            url_update_overview = reverse('profile:publish_overview', args=[slug])
            response = self.client.post(url_update_overview, data)
            if status == 'success':
                self.assertJSONEqual(
                    str(response.content, encoding='utf8'),
                    {'status': 'complete', 'message': 'Overview Update Success'}
                )
            else:
                self.assertJSONEqual(
                    str(response.content, encoding='utf8'),
                    {'status': 'error', 'message': 'Current overview not found!'}
                )

        def check_overview(is_draft: bool, is_publish: bool, overview: Overview):
            self.assertEqual(overview.is_draft, is_draft)
            self.assertEqual(overview.is_publish, is_publish)
            self.assertEqual(overview.is_active, True)

        self.client.login(username='user_3@mail.ru', password='qwerty1')
        # Create Overview
        response = self.client.post(self.url_create_overview, self.create_overview_data)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'redirect': self.url_list_publish_overview}
        )
        overview = get_object_or_404(Overview, title=self.create_overview_data.get('title'))
        overview.is_active = True
        overview.save()

        # Request change is_draft = True
        change_overview(status='success', slug=overview.slug, data={'is_draft': 'true', 'is_publish': 'false'})
        overview.refresh_from_db()
        check_overview(is_draft=True, is_publish=False, overview=overview)

        # Request change is_publish = True
        change_overview(status='success', slug=overview.slug, data={'is_draft': 'false', 'is_publish': 'true'})
        overview.refresh_from_db()
        check_overview(is_draft=False, is_publish=True, overview=overview)

        # Request Invalid Overview
        change_overview(status='not found overview', slug='test', data={})
        overview.refresh_from_db()
        check_overview(is_draft=False, is_publish=True, overview=overview)

        self.client.logout()

    # Block correspndence
    def test_list_chats(self):
        """test for checking correctly output chats"""

        def create_chat():
            response = self.client.post(self.url_create_chat, self.create_chat_data)
            self.assertRedirects(
                response, self.url_chats_profile, 302, target_status_code=200, fetch_redirect_response=True
            )

        def get_chats():
            response = self.client.get(self.url_chats_profile)
            # Check Count
            self.assertEqual(response.context['chats'].count(), 1)

        self.client.login(username='user_3@mail.ru', password='qwerty1')
        # Request Create Chat
        sender = Profile.objects.filter(user=self.user_3).first()
        receiver = Profile.objects.filter(user=self.user_1).first()
        self.create_chat_data['sender'] = sender.pk
        self.create_chat_data['receiver'] = receiver.pk
        create_chat()
        self.client.logout()

        # Check Chats
        self.client.login(username='article@mail.ru', password='dsfsdfds')
        get_chats()
        self.client.logout()

    def test_list_comments(self):
        def login_user(username: str, password: str):
            self.client.login(username=username, password=password)

        def create_comment(data: dict):
            res = self.client.post(self.url_create_overview_comment, data)
            self.assertJSONEqual(
                str(res.content, encoding='utf8'),
                {'status': 'success', 'message': 'New comment saved success!'}
            )

        def check_comments(count: int):
            response = self.client.get(self.url_comments_overview)
            # Check Data
            self.assertEqual(response.context['profile_comments'].count(), count)

        # Create Overview
        login_user(username='user_3@mail.ru', password='qwerty1')
        response = self.client.post(self.url_create_overview, self.create_overview_data)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'redirect': self.url_list_publish_overview}
        )
        overview = get_object_or_404(Overview, title=self.create_overview_data.get('title'))
        self.client.logout()

        # Create Comment
        login_user(username='art@mail.ru', password='qwerty1')
        create_comment_data = {'text': 'Comment One', 'overview': overview.pk}
        create_comment(create_comment_data)
        overview.refresh_from_db()
        self.client.logout()

        # Get Comments
        login_user(username='user_3@mail.ru', password='qwerty1')
        check_comments(1)
        self.client.logout()

        # Create New Comment
        login_user(username='art@mail.ru', password='qwerty1')
        create_comment(create_comment_data)
        overview.refresh_from_db()
        self.client.logout()

        # Get Comments
        login_user(username='user_3@mail.ru', password='qwerty1')
        check_comments(2)
        self.client.logout()

    # OTHER
    # def test_create_question(self):
    #     """test for checking correctly create question"""
    #     self.client.login(username='user_3@mail.ru', password='qwerty1')
    #
    #     # Create Manufacturer
    #     create_manufacturer_data = {
    #
    #     }
    #     response = self.client.post('')
    #
    #     # # Create Product
    #     # create_product_data = {
    #     #     'name': 'Product Test',
    #     # }
    #     # response = self.client.post(self.url_create_product, create_product_data)
    #     # print('response: ', response)
    #     # print('response.context: ', response.context)
    #
    #     # Create Question
    #     # response = self.client.post(reverse('profile:create_question', args=[1]))

    def test_set_action_profile_object(self):
        """test for checking correctly setting like/unlike on object"""

        # user_1 actions: like article, product and add in favorite
        self.client.login(username='article@mail.ru', password='dsfsdfds')
        response = self.client.post(self.url_action_article, {'model': 'article', 'action': 'like'})
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.url_action_article, {'model': 'article', 'action': 'favorite'})
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.url_action_product, {'model': 'product', 'action': 'like'})
        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.article.get_like_count, 1)
        self.assertEqual(self.product.get_like_count, 1)
        self.assertEqual(self.article.status_likes(response.wsgi_request.user), ADD)
        self.assertEqual(self.article.get_favorite_count, 1)
        self.assertEqual(self.article.status_favorite(response.wsgi_request.user), ADD)
        self.client.logout()

        # user_2 actions: like article, product and add in favorite
        self.client.login(username='art@mail.ru', password='qwerty1')
        response = self.client.post(self.url_action_article, {'model': 'article', 'action': 'like'})
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.url_action_article, {'model': 'article', 'action': 'favorite'})
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.url_action_product, {'model': 'product', 'action': 'like'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.article.get_like_count, 2)
        self.assertEqual(self.product.get_like_count, 2)
        self.assertEqual(self.article.status_likes(response.wsgi_request.user), ADD)
        self.assertEqual(self.article.get_favorite_count, 2)
        self.assertEqual(self.article.status_favorite(response.wsgi_request.user), ADD)
        self.client.logout()

        # user_1 actions: unlike article, product and remove from favorite
        self.client.login(username='article@mail.ru', password='dsfsdfds')
        response = self.client.post(self.url_action_article, {'model': 'article', 'action': 'like'})
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.url_action_article, {'model': 'article', 'action': 'favorite'})
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.url_action_product, {'model': 'product', 'action': 'like'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.article.get_like_count, 1)
        self.assertEqual(self.product.get_like_count, 1)
        self.assertEqual(self.article.status_likes(response.wsgi_request.user), REMOVE)
        self.assertEqual(self.article.get_favorite_count, 1)
        self.assertEqual(self.article.status_favorite(response.wsgi_request.user), REMOVE)
        self.client.logout()

        # user_2 actions: unlike article, product and remove from favorite
        self.client.login(username='art@mail.ru', password='qwerty1')
        response = self.client.post(self.url_action_article, {'model': 'article', 'action': 'like'})
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.url_action_article, {'model': 'article', 'action': 'favorite'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.article.get_like_count, 0)
        self.assertEqual(self.article.status_likes(response.wsgi_request.user), REMOVE)
        self.assertEqual(self.article.get_favorite_count, 0)
        self.assertEqual(self.article.status_favorite(response.wsgi_request.user), REMOVE)
        self.assertEqual(self.article.get_like_count, 0)
        self.client.logout()

    def test_view_count_profile(self):
        """test for checking correctly setting views on object"""
        self.client.login(username='art@mail.ru', password='qwerty1')
        response = self.client.post(self.url_action_article, {'model': 'article', 'action': 'favorite'})

        # user_2 reaction: view article
        ViewMixin.check_view_user(response.wsgi_request, self.article)
        self.assertEqual(self.article.get_view_count, 1)

        # user_2 reaction: view article
        ViewMixin.check_view_user(response.wsgi_request, self.article)
        self.assertEqual(self.article.get_view_count, 1)

        # AnonymousUser reaction: view article
        response.wsgi_request.user = AnonymousUser()
        ViewMixin.check_view_user(response.wsgi_request, self.article)
        self.assertEqual(self.article.get_view_count, 1)

        # AnonymousUser reaction: view article
        ViewMixin.check_view_user(response.wsgi_request, self.article)
        self.assertEqual(self.article.get_view_count, 1)
        self.client.logout()

    # Not Working

    # def test_set_like_dislike_profile_objects(self):
    #     """test for checking correctly setting likes/dislikes and unset them for object"""
    #
    #     self.client.login(username='art@mail.ru', password='qwerty1')
    #
    #     # user_2 reaction: set like and check review reaction
    #     response = self.client.post(self.url_action_like_review)
    #     self.assertEqual(response.status_code, 200)
    #     reactions = self.review.reaction(response.wsgi_request)
    #     self.assertEqual(reactions, ((1, True), (0, False)))
    #
    #     # user_2 reaction: set unlike and check review reaction
    #     response = self.client.post(self.url_action_like_review)
    #     self.assertEqual(response.status_code, 200)
    #     reactions = self.review.reaction(response.wsgi_request)
    #     self.assertEqual(reactions, ((0, False), (0, False)))
    #
    #     # user_2 reaction: set dislike and check review reaction
    #     response = self.client.post(self.url_action_dislike_review)
    #     self.assertEqual(response.status_code, 200)
    #     reactions = self.review.reaction(response.wsgi_request)
    #     self.assertEqual(reactions, ((0, False), (1, True)))
    #
    #     # user_2 reaction: set like and check review reaction
    #     response = self.client.post(self.url_action_like_review)
    #     self.assertEqual(response.status_code, 200)
    #     reactions = self.review.reaction(response.wsgi_request)
    #     self.assertEqual(reactions, ((1, True), (0, False)))
    #
    #     # AnonymousUser reaction: set like and check review reaction
    #     self.client.logout()
    #     response = self.client.post(self.url_action_like_review)
    #     response.wsgi_request.user = AnonymousUser()
    #     reactions = self.review.reaction(response.wsgi_request)
    #     self.assertEqual(reactions, ((1, False), (0, False)))
    #
    #     # user_1 reaction
    #     self.client.login(username='article@mail.ru', password='dsfsdfds')
    #     response = self.client.post(self.url_action_like_review)
    #     self.assertEqual(response.status_code, 200)
    #
    #     response = self.client.post(self.url_action_like_review)
    #     self.assertEqual(response.status_code, 200)
    #
    #     response = self.client.post(self.url_action_dislike_review)
    #     self.assertEqual(response.status_code, 200)
    #
    #     reactions = self.review.obj_reactions(response.wsgi_request)
    #     self.assertEqual(reactions, ((1, False), (1, True)))
    #     self.client.logout()

    # def test_author_rating(self):
    #     """test for checking correctly setting author rating"""
    #     with freeze_time("2023-08-20 15:00:00"):
    #         self.overview = Overview.objects.create(author=self.author, title='test', slug='test-overview',
    #                                                 description='test', is_publish=True)
    #         self.url_author_reaction = reverse('profile:author_action', args=[self.author.pk])
    #         self.url_action_overview = reverse('profile:set_action', args=[self.overview.slug])
    #
    #         # action by user_2
    #         self.client.login(username='art@mail.ru', password='qwerty1')
    #         response = self.client.post(self.url_author_reaction, {'model': 'subscribe'})
    #         self.assertEqual(response.status_code, 200)
    #         response = self.client.post(self.url_author_reaction, {'model': 'gratitude'})
    #         self.assertEqual(response.status_code, 200)
    #         self.assertEqual(self.author.get_rating_value(), 3)
    #         ViewMixin.check_view_user(response.wsgi_request, self.overview)
    #         ViewMixin.check_view_user(response.wsgi_request, self.overview)
    #         self.assertEqual(self.author.get_rating_value(), 4)
    #         self.client.post(self.url_action_overview, {'model': 'overview', 'action': 'favorite'})
    #         self.client.post(self.url_action_overview, {'model': 'overview', 'action': 'like'})
    #         self.assertEqual(self.author.get_rating_value(), 6)
    #     with freeze_time("2023-08-31 15:00:00"):
    #         response = self.client.post(self.url_author_reaction, {'model': 'subscribe'})
    #         self.assertEqual(response.status_code, 200)
    #         self.assertEqual(self.author.get_rating_value(), 5)
    #         response = self.client.post(self.url_author_reaction, {'model': 'gratitude'})
    #         self.assertEqual(response.status_code, 200)
    #         self.assertEqual(self.author.get_rating_value(), 4)
    #         self.client.post(self.url_action_overview, {'model': 'overview', 'action': 'favorite'})
    #         self.client.post(self.url_action_overview, {'model': 'overview', 'action': 'like'})
    #         self.assertEqual(self.author.get_rating_value(), 2)
    #         self.client.logout()
    #         self.client.login(username='article@mail.ru', password='dsfsdfds')
    #         self.client.post(self.url_action_overview, {'model': 'overview', 'action': 'favorite'})
    #         self.assertEqual(self.author.get_rating_value(), 3)
    #         response = self.client.post(self.url_author_reaction, {'model': 'subscribe'})
    #         self.assertEqual(response.status_code, 200)
    #         self.assertEqual(self.author.get_rating_value(), 4)
    #         self.client.logout()
    #         self.assertEqual(self.author.get_rating_value('week'), 0)
    #         self.assertEqual(self.author.get_rating_value('month'), 4)
    #         self.assertEqual(self.author.get_rating_value('quarter'), 4)
    #         self.assertEqual(self.author.get_rating_value('year'), 4)
