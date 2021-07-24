from unittest.mock import patch
from requests import Response

from tests.base_test import BaseTest
from tests.test_data import business_data
from models.business.business import BusinessModel


class BusinessEmailSignInTest(BaseTest):
    @patch.object(BusinessModel, 'send_verification_email')
    def test_signin_successful(self, mock_send_verification_email):
        with self.app() as test_client, self.app_context():
            # signup
            mock_send_verification_email.return_value = Response()
            business_user = {'email': business_data['email'], 'password': business_data['password']}
            signup_resp = test_client.post('/business/signup/email', json=business_data)
            self.assertEqual(signup_resp.status_code, 201)
            mock_send_verification_email.assert_called_once()
            # confirm user
            saved_business_user = BusinessModel.find_user_by_email(business_data['email'])
            confirmation_id = saved_business_user.most_recent_confirmation.id
            confirm_resp = test_client.get(f'/business/confirmation/{confirmation_id}')
            self.assertEqual(confirm_resp.status_code, 200)
            self.assertIn(business_data['email'], confirm_resp.json['msg'])
            # signin
            signin_resp = test_client.post('/business/signin/email', json=business_user)
            self.assertEqual(signin_resp.status_code, 200)
            self.assertIn('access_token', signin_resp.json)
            self.assertIn('refresh_token', signin_resp.json)
