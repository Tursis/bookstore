from pip._vendor import requests
from .env_variables import mailgun


def send_simple_message(email, subject, html, context):
    """
    Отправка писем
    """

    html_content = html.render(context)
    return requests.post(
        "https://api.mailgun.net/v3/sandbox179b6ebaa0594a0f951760f80e877e4d.mailgun.org/messages",
        auth=("api", mailgun),
        data={"from": "mailgun@sandbox179b6ebaa0594a0f951760f80e877e4d.mailgun.org",
                    "to": [email],
                    "subject": subject,
                    "html": html_content,
                    }
    )

# files=[
#        ("attachment", ("test.txt", open("d://test.mime", "rb").read()))],
