from unittest.mock import patch

from requests import Response

from tests.base_test import BaseTest
from tests.test_data import business_data
from models.business.business import BusinessModel


class BusinessEmailSignUpTest(BaseTest):
    @patch.object(BusinessModel, 'send_verification_email')
    def test_business_signup_with_email_password(self, mock_send_verification_email):
        with self.app() as test_client, self.app_context():
            mock_send_verification_email.return_value = Response()
            resp = test_client.post('/business/signup/email', json=business_data)
            self.assertEqual(resp.status_code, 201)
            expected_resp = {'msg': 'Client account created successfully. Check your email to activate your account'}
            self.assertEqual(resp.json, expected_resp)
