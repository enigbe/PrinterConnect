import os
from typing import List
from requests import Response, post

MISSING_MAILGUN_API_KEY = 'Missing Mailgun API key.'
MISSING_MAILGUN_DOMAIN = 'Missing Mailgun Domain.'
ERROR_SENDING_EMAIL = 'Error in sending verification email. Client registration failed.'


class MailgunException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class Mailgun:
    MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN')  # if not found, will be None
    MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')  # if not found, will be None
    TITLE = 'PrinterConnect'
    MAILGUN_EMAIL = os.environ.get('MAILGUN_EMAIL')

    @classmethod
    def send_email(cls, email: List[str], subject: str, text: str) -> Response:
        if cls.MAILGUN_API_KEY is None:
            raise MailgunException(MISSING_MAILGUN_API_KEY)

        if cls.MAILGUN_DOMAIN is None:
            raise MailgunException(MISSING_MAILGUN_DOMAIN)

        response = post(
            f'https://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages',
            auth=('api', cls.MAILGUN_API_KEY),
            data={
                'from': f'{cls.TITLE} <{cls.MAILGUN_EMAIL}>',
                'to': email,
                'subject': subject,
                'text': text
            },
        )

        if response.status_code != 200:
            raise MailgunException(ERROR_SENDING_EMAIL)

        return response
