from bookstore import settings
from django.views.generic import CreateView
from django.views.generic.edit import FormView
from profile.forms import SignUpForm
from .token import AccountToken
from .models import Profile, Token
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.views import generic
from django.contrib.sites.shortcuts import get_current_site


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
        ActivateAccountMessageView.form_valid(self, form)
        return super(SignUpView, self).form_valid(form)


class ActivateAccountMessageView(FormView):
    form_class = SignUpForm

    def form_valid(self, form):
        plaintext = get_template('registration/email.txt')
        html = get_template('registration/email.html')
        if form.is_valid():
            user_form = form.cleaned_data
            user = User.objects.get(username=user_form['username'])
            current_site = get_current_site(self.request)
            context = {'domain': current_site.domain,
                       'id': user.id,
                       'token': AccountToken.create_token(self, user_form['username'])}
            subject, from_email, to = 'Them', 'from@example.com', user_form['email']
            text_content = plaintext.render(context)
            html_content = html.render(context)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()


class ActivateAccountView(generic.View):
    def get(self, request, token, *args, **kwargs):
        user_token = Token(id=self.request)
        token_user = Token(token=token)
        if token_user.token == token:
            token_user.save()
            context = {'username': token}
            return render(request, 'registration/account_activation_email.html', context=context)
        else:
            context = {'username': 'пісос'}
            return render(request, 'registration/account_activation_email.html', context=context)
