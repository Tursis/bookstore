from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from profile.forms import SignUpForm


class SignUpFormTest(TestCase):

    # def test_username_form_field_label(self):
    #     form = SignUpForm()
    #     self.assertTrue(form.fields['username'].label is None or form.fields['username'] == 'username')
    #
    # def test_username_form_filed_help_text(self):
    #     form = SignUpForm()
    #     self.assertEqual(form.fields['username'].help_text, 'Enter your username')

    def test_sign_up_form(self):

        resp = self.client.post(reverse('profile:sign_up'), data={
            'username': 'tursis',
            'first_name': 'Oleh',
            'last_name': 'Spytsia',
            'email': 'oleh@inbox.ru',
            'password1': 'Jktu199437',
            'password2': 'Jktu199437'
        })
        self.assertEqual(resp.status_code, 200)

        users = get_user_model().objects.all()

        self.assertEqual(users.count(), 1)
