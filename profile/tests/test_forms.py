from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from profile.forms import SignUpForm


# class SignUpFormTest(TestCase):
    # def test_username_form_field_label(self):
    #     form = SignUpForm()
    #     self.assertTrue(form.fields['username'].label is None or form.fields['username'] == 'username')
    #
    # def test_username_form_filed_help_text(self):
    #     form = SignUpForm()
    #     self.assertEqual(form.fields['username'].help_text, 'Enter your username')


