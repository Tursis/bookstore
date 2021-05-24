from django.contrib.auth import get_user_model
from django.urls import reverse

from django.contrib.auth.models import User

from django.test import RequestFactory, TestCase

from profile.token import create_token

PROFILE_DETAIL_URL = reverse('profile:profile_detail')


class CreateTokenTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        first_user = User.objects.create_user(username='Tursis')
        first_user.set_password('123456')
        first_user.email = 'test@gmail.com'
        first_user.save()

    def test_create_token(self):
        user = get_user_model().objects.get(pk=1)
        token = create_token(user.username)
        self.assertTrue(token)