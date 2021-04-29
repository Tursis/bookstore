from django.test import TestCase

from profile.models import User


class UserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create(first_name='Oleh', last_name='Spytsiya')

    # def test_first_name_label(self):
    #     user = User.objects.get(id=1)
    #     field_label = user._meta.get_field('first_name').verbose_name
    #     self.assertEquals(field_label, 'first_name')
    #
    # def test_object_name_is_last_name_comma_first_name(self):
    #     user = User.objects.get(id=1)
    #     expected_object_name = '%s, %s' % (user.last_name, user.first_name)
    #     self.assertEquals(expected_object_name, str(user))

