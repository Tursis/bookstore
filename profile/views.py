from django.views.generic import CreateView
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.views import generic
from django.shortcuts import render
from profile.forms import SignUpForm
from .token import AccountToken
from .models import Token
from datetime import timedelta
from shared.send_message import EmailCommunication, send_simple_message
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
            ActivateAccountMessageView(user_token.token)
            send_simple_message()
        return super(SignUpView, self).form_valid(form)


class ActivateAccountMessageView:
    """Отправка письма активации пользовалетя"""
    def __init__(self, token):
        self.send_message = EmailCommunication
        ActivateAccountMessageView.send(self, token)

    def send(self, token):
        user_token = Token.objects.get(token=token)
        user = User.objects.get(id=user_token.user.id)
        plaintext = get_template('registration/email.txt')
        html = get_template('registration/email.html')
        context = {'id': user.id,
                   'token': user.token.token}
        return self.send_message.send(self, plaintext, html, user.email, context)


class ActivateAccountView(generic.View):
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
