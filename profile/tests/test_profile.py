import urllib
from django.urls import reverse

from django.contrib.auth.models import User
from django.http import QueryDict
from django.test import TestCase
from django.utils.datastructures import MultiValueDict

from profile.profile import change_password, change_profile_data, change_profile_email


class MakingChangesProfileTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='Tursis')
        user.set_password('123456')
        user.email = 'oleh94@inbox.ru'
        user.save()

    def test_change_profile_data(self):
        user = User.objects.get(pk=1)
        test = {'csrfmiddlewaretoken': ['hXOApCs9SrjbvSPDIVzDbc6a1qUVVSmh4q5K0HrHVUuIUBtOpTtMvUwlZVcyu7Po'], 'last_name': ['Спиця'], 'name': ['Олег'], 'middle_name': ['Вікторович'], 'gender': ['М'],
                   'birth_day': ['7'], 'birth_month': ['3'], 'birth_year': ['1994'], 'phone_number': [''],
                   'email': ['tursis94@gmail.com'], 'old_password': [''],
                   'new_password': [''], 'repeat_new_password': ['']}

        login = self.client.login(username='Tursis', password='123456')

        resp = self.client.post(reverse('profile:profile_detail'), data=test)
        change_profile_data(resp.wsgi_request)
        user = User.objects.get(pk=1)
        print(user.email)
        print(resp.wsgi_request.POST)
        self.assertEqual(user.email, 'hello')
