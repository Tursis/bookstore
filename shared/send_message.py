from pip._vendor import requests
from .env_variables import mailgun


def send_simple_message(email, subject, message_date):
    """
    Отправка писем
    """
    message_body = {"from": "mailgun@sandbox179b6ebaa0594a0f951760f80e877e4d.mailgun.org",
                    "to": [email],
                    "subject": subject,
                    }
    message_body.update(message_date)
    print(message_body)
    return requests.post(
        "https://api.mailgun.net/v3/sandbox179b6ebaa0594a0f951760f80e877e4d.mailgun.org/messages",
        auth=("api", mailgun),
        data=message_body
    )

# files=[
#        ("attachment", ("test.txt", open("d://test.mime", "rb").read()))],
