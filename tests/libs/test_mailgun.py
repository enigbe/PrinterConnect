from unittest.mock import patch
from requests import Response
from tests.base_test import BaseTest
from libs.mailgun import Mailgun, MailgunException

MISSING_MAILGUN_API_KEY = 'Missing Mailgun API key.'
MISSING_MAILGUN_DOMAIN = 'Missing Mailgun Domain.'
ERROR_SENDING_EMAIL = 'Error in sending verification email. Client registration failed.'


class MailgunTest(BaseTest):
    def test_send_email_no_api_key(self):
        email = ['ochekliyeenigbe@gmail.com']
        subject = 'Account Verification'
        text = 'Hello, your account has been verified.'

        with patch('libs.mailgun.Mailgun.send_email') as mock_send_email:
            mock_send_email.side_effect = MailgunException(MISSING_MAILGUN_API_KEY)
            with self.assertRaises(MailgunException):
                Mailgun.send_email(email, subject, text)

    def test_send_email_no_domain(self):
        email = ['ochekliyeenigbe@gmail.com']
        subject = 'Account Verification'
        text = 'Hello, your account has been verified.'

        with patch('libs.mailgun.Mailgun.send_email') as mock_send_email:
            mock_send_email.side_effect = MailgunException(MISSING_MAILGUN_DOMAIN)
            with self.assertRaises(MailgunException):
                Mailgun.send_email(email, subject, text)

    def test_send_email_status_code_not_200(self):
        email = ['ochekliyeenigbe@gmail.com']
        subject = 'Account Verification'
        text = 'Hello, your account has been verified.'

        with patch('libs.mailgun.Mailgun.send_email') as mock_send_email:
            mock_send_email.side_effect = MailgunException(ERROR_SENDING_EMAIL)
            mock_send_email.response.status_code = 500
            with self.assertRaises(MailgunException):
                Mailgun.send_email(email, subject, text)

    def test_send_email_successful(self):
        email = ['ochekliyeenigbe@gmail.com']
        subject = 'Account Verification'
        text = 'Hello, your account has been verified.'

        with patch('libs.mailgun.Mailgun.send_email') as mock_send_email:
            mock_send_email.return_value = Response()
            mock_send_email.return_value.status_code = 200

            response = Mailgun.send_email(email, subject, text)

            mock_send_email.assert_called()
            self.assertIsInstance(response, Response)
            self.assertEqual(response.status_code, 200)
