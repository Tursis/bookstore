

from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from pip._vendor import requests

from bookstore.settings import SITE_DOMAIN


class EmailCommunication:

    def send(self, plaintext, html, email, context):
        context = context
        context['domain'] = SITE_DOMAIN
        subject, from_email, to = 'Them', 'from@example.com', email
        text_content = plaintext.render(context)
        html_content = html.render(context)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v3/sandbox179b6ebaa0594a0f951760f80e877e4d.mailgun.org/messages",
        auth=("api", "9dbed12e9a14c2c3794fbc2ecf5a6bf3-b6190e87-a7293014"),
        data={"from": "mailgun@sandbox179b6ebaa0594a0f951760f80e877e4d.mailgun.org",
              "to": ["tursis94@gmail.com"],
              "subject": "Hello",
              "text": "Testing some Mailgun awesomness!"})
