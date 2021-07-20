from django.test import TestCase

from profile.models import User


class UserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create(first_name='Oleh', last_name='Spytsiya')

    def test_len_gender(self):
        user = User.objects.get(id=1)
        gender_len = len(user.profile.gender)
        self.assertEqual(gender_len, 0)
