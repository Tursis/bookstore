from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from bookstore.settings import SITE_URL


class EmailCommunication:

    def send(self, plaintext, html, email, context):
        context = context
        context['domain'] = SITE_URL
        subject, from_email, to = 'Them', 'from@example.com', email
        text_content = plaintext.render(context)
        html_content = html.render(context)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
