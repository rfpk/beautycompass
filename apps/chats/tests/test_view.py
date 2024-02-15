from django.test import TestCase

from django.urls import reverse

from apps.products.models import Tag
from apps.profile.models import User


class TestChatCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_post1@mail.ru')
        self.user.set_password('12345')
        self.user.save()
        self.tag1 = Tag.objects.create(name='test1', slug='test-1')
        self.tag2 = Tag.objects.create(name='test2', slug='test-2')
        self.tag3 = Tag.objects.create(name='test3', slug='test-3')
        self.create_post_data = {
            'title': 'Title post',
            'text': 'Test post',
            'tag': (self.tag1.pk, self.tag2.pk, self.tag3.pk)
        }
        self.url_create_post = reverse('chats:create_conversation_post')

    def test_create_post(self):
        """Test for correctly create/update conversation post data"""
        self.client.login(username='test_post1@mail.ru', password='12345')
        response = self.client.post(self.url_create_post, self.create_post_data)
        self.assertEqual(response.status_code, 302)  # проверяем, что редирект произошел
        profile_post = self.user.user_profile.profile_conversation_posts.first()
        self.assertEqual(profile_post.title, 'Title post')
        self.assertEqual(len(profile_post.tag.all()), 3)
        self.client.logout()



