from bookstore import settings
from django.views.generic import CreateView
from django.views.generic.edit import FormView
from profile.forms import SignUpForm
from .token import AccountToken
from .models import Profile
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.views import generic


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/sign_up.html'
    model = User

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # Deactivate account till it is confirmed
        user.save()
        ActivateAccountMessageView.form_valid(self, form)
        return super(SignUpView, self).form_valid(form)


class ActivateAccountMessageView(FormView):
    form_class = SignUpForm

    def form_valid(self, form):
        plaintext = get_template('registration/email.txt')
        html = get_template('registration/email.html')
        if form.is_valid():
            user_email = form.cleaned_data
            context = {'username': user_email['username'],
                       'token': AccountToken.create_token(self)}
            subject, from_email, to = 'hello', 'from@example.com', user_email['email']
            text_content = plaintext.render(context)
            html_content = html.render(context)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()


class ActivateAccountView(generic.View):
    model = User

    def get(self, request, username, *args, **kwargs):
        context = {'username': username}
        return render(request, 'registration/account_activation_email.html', context=context)
