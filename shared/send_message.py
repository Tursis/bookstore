from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from django.template.loader import get_template
from pip._vendor import requests
from .env_variables import mailgun

from bookstore.settings import SITE_DOMAIN


class EmailCommunication:
    """
    Отправка писем
    """

    def send(self, plaintext, html, email, context):
        context = context
        context['domain'] = SITE_DOMAIN
        subject, from_email, to = 'Them', 'from@example.com', email
        text_content = plaintext.render(context)
        html_content = html.render(context)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


def send_simple_message(email):
    cont = 'oleh'
    """
    Отправка писем
    """
    return requests.post(
        "https://api.mailgun.net/v3/sandbox179b6ebaa0594a0f951760f80e877e4d.mailgun.org/messages",
        auth=("api", mailgun),
        # files=[
        #        ("attachment", ("test.txt", open("d://test.mime", "rb").read()))],
        data={"from": "mailgun@sandbox179b6ebaa0594a0f951760f80e877e4d.mailgun.org",
              "to": [email],
              "subject": "Hello",
              # "tracking-opens": False,
              # "tracking-clicks": False,
              # "tracking": False,
              "template": "test",
              },
        )


# ("attachment", ("test.jpg", open("files/test.jpg", "rb").read())),
