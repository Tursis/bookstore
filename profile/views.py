from django.views.generic import CreateView
from django.views.generic.edit import FormView
from profile.forms import SignUpForm
from .token import AccountToken
from .models import Token
from shared.send_message import EmailCommunication
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.template import Context
from django.views import generic
from django.contrib.sites.shortcuts import get_current_site
from datetime import timedelta
from django.utils import timezone


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/sign_up.html'
    model = User

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # Deactivate account till it is confirmed
        user.save()
        if form.is_valid():
            user_form = form.cleaned_data
            user_token = Token(id=self.object)
            user_token.user = user
            user_token.token = AccountToken.create_token(self, user_form['username'])
            user_token.save()
            ActivateAccountMessageView(user_token.token)

        return super(SignUpView, self).form_valid(form)


class ActivateAccountMessageView:

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
                token.user.is_active = True  # Deactivate account till it is confirmed
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
