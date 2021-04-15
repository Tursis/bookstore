from datetime import timedelta

from django.contrib.auth.password_validation import password_validators_help_texts
from django.views import View
from django.views.generic import CreateView
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from django.core import exceptions
from bookstore.settings import SITE_DOMAIN
from profile.forms import SignUpForm
from .profile import change_password, change_profile_data, change_profile_email
from .token import AccountToken
from .models import Token
from shared.send_message import send_simple_message
from shared.mixins import AuthCheckerMixin


class SignUpView(AuthCheckerMixin, CreateView):
    """
    Форма регистрации
    """
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/sign_up.html'
    model = User

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        user = form.save(commit=False)
        user.is_active = False  # Deactivate account till it is confirmed
        user.save()
        if form.is_valid():
            user_form = form.cleaned_data
            user_token = Token(id=user.id)
            user_token.user = user
            user_token.token = AccountToken.create_token(self, user_form['username'])
            user_token.save()

            html = get_template('registration/email.html')
            context = {'username': user,
                       'token': user_token.token,
                       "domain": SITE_DOMAIN
                       }
            send_simple_message(user.email, 'Activate Account', html, context)
        return super(SignUpView, self).form_valid(form)


class ActivateAccountView(View):
    """"
    Активация пользователя
    """

    def get(self, request, token):
        try:
            token = Token.objects.get(token=token)
            user = User.objects.get(id=token.user.id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, Token.DoesNotExist):
            user = None
            token = None

        if user is not None and token is not None:
            final_date = token.user.date_joined + timedelta(days=14)
            if final_date >= timezone.now():
                token.user.is_active = True  # activate account till it is confirmed
                token.delete()
                token.user.save()
                context = {'username': token.user}
                return render(request, 'registration/account_activation_email.html', context=context)
            else:
                user.delete()
                return render(request, 'registration/error.html')
        else:
            context = {'error': 'Пользователя не существует'}
            return render(request, 'registration/error.html', context=context)


class ProfileDetailView(View):
    def get(self, request):
        return render(request, 'profile_detail.html', context={'user': request.user})

    def post(self, request, *args, **kwargs):
        errors = dict()
        try:
            change_profile_data(request)
        except exceptions.ValidationError as e:
            errors['profile_data'] = list(e.messages)

        try:
            change_profile_email(request)
        except exceptions.ValidationError as e:
            errors['email'] = list(e.messages)

        if request.POST.get("old_password") != '':
            try:
                change_password(request)
            except exceptions.ValidationError as e:
                errors['password'] = list(e.messages)
        return render(request, 'profile_detail.html', context={'user': request.user, 'errors': errors})
