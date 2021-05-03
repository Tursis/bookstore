from django.test import TestCase

from profile.forms import SignUpForm


class SignUpFormTest(TestCase):
    def test_username_form__field_label(self):
        form = SignUpForm()
        self.assertTrue(form.fields['username'].label is None or form.fields['username'] == 'username')

    def test_username_form_filed_help_text(self):
        form = SignUpForm()
        self.assertEqual(form.fields['username'].help_text, 'Enter your username')
