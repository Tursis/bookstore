from django.shortcuts import render
from bookstore import settings
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from profile.forms import SignUpForm


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/sign_up.html'

    def form_valid(self, form):
        ActiveMailView.form_valid(self, form)
        return super(SignUpView, self).form_valid(form)


class ActiveMailView(FormView):
    form_class = SignUpForm

    def form_valid(self, form):
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data

            email = EmailMessage(
                'Tursis@ua',
                'Body goes hereooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo',
                'tursis94@gmail.com',
                [cd['email']],
                ['bcc@example.com'],
                reply_to=['another@example.com'],
                headers={'Message-ID': 'foo'},
            )
            return email.send()
