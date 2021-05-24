from django.core.exceptions import ValidationError
from django.urls import reverse

from django.contrib.auth.models import User

from django.test import RequestFactory, TestCase

from profile.profile import change_password, change_profile_data, change_profile_email

PROFILE_DETAIL_URL = reverse('profile:profile_detail')


class MakingChangesProfileTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        first_user = User.objects.create_user(username='Tursis')
        first_user.set_password('123456')
        first_user.email = 'oleh94@inbox.ru'
        first_user.save()

        second_user = User.objects.create_user(username='Milisento')
        second_user.set_password('123456')
        second_user.email = 'test@gmail.com'
        second_user.save()

    def test_change_profile_data(self):
        user = User.objects.get(pk=1)
        data = {'last_name': 'Спиця', 'name': 'Олег', 'middle_name': 'Вікторович', 'gender': 'М',
                'birth_day': '7', 'birth_month': '3', 'birth_year': '1994', 'phone_number': ''}
        request = self.factory.post(PROFILE_DETAIL_URL, data=data)
        request.user = user
        change_profile_data(request)
        user = User.objects.get(pk=1)

        self.assertEqual(user.profile.birthday.day, int(data['birth_day']))
        self.assertEqual(user.profile.birthday.month, int(data['birth_month']))
        self.assertEqual(user.profile.birthday.year, int(data['birth_year']))
        self.assertEqual(user.first_name, data['name'])
        self.assertEqual(user.last_name, data['last_name'])
        self.assertEqual(user.profile.surname, data['middle_name'])
        self.assertEqual(user.profile.gender, data['gender'])

    def test_change_profile_email(self):
        user = User.objects.get(pk=1)
        data = {'email': 'tursis94@gmail.com'}
        request = self.factory.post(PROFILE_DETAIL_URL, data=data)
        request.user = user
        change_profile_email(request)
        user = User.objects.get(pk=1)
        self.assertEqual(user.email, data['email'])

    def test_email_is_already_use(self):
        user = User.objects.get(pk=1)
        data = {'email': 'test@gmail.com'}
        request = self.factory.post(PROFILE_DETAIL_URL, data=data)
        request.user = user
        with self.assertRaisesRegexp(ValidationError, 'email уже занят'):
            change_profile_email(request)

    def test_change_password(self):
        user = User.objects.get(pk=1)
        data = {'old_password': '123456', 'new_password': 'Qwe1432fQr', 'repeat_new_password': 'Qwe1432fQr'}
        request = self.factory.post(PROFILE_DETAIL_URL, data=data)
        request.user = user
        change_password(request)
        user = User.objects.get(pk=1)
        self.assertTrue(user.check_password(data['new_password']))

    def test_empty_password(self):
        user = User.objects.get(pk=1)
        data = {'old_password': '', 'new_password': 'Qwe1432fQr', 'repeat_new_password': 'Qwe1432fQr'}
        request = self.factory.post(PROFILE_DETAIL_URL, data=data)
        request.user = user
        change_password(request)
        user = User.objects.get(pk=1)
        self.assertFalse(user.check_password(data['new_password']))

    def test_wrong_old_password(self):
        user = User.objects.get(pk=1)
        data = {'old_password': '12345678', 'new_password': 'Qwe1432fQr', 'repeat_new_password': 'Qwe1432fQr'}
        request = self.factory.post(PROFILE_DETAIL_URL, data=data)
        request.user = user
        with self.assertRaisesRegexp(ValidationError, 'Не правильный пароль'):
            change_password(request)

    def test_Equal_passwords(self):
        user = User.objects.get(pk=1)
        data = {'old_password': '123456', 'new_password': 'Qwe1432fQr', 'repeat_new_password': 'Qwe143'}
        request = self.factory.post(PROFILE_DETAIL_URL, data=data)
        request.user = user
        with self.assertRaisesRegexp(ValidationError, 'Пароли не равны'):
            change_password(request)