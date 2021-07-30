from unittest.mock import patch
from requests import Response

from flask_jwt_extended import create_access_token

from tests.base_test import BaseTest
from models.business.business import BusinessModel
from tests.test_data import business_data


class BusinessSignOutTest(BaseTest):
    @patch.object(BusinessModel, 'send_verification_email')
    def test_sign_out_successful(self, mock_send_verification_email):
        """Test client sign in successful"""
        with self.app() as test_client, self.app_context():
            # 1. Create and confirm client user
            mock_send_verification_email.return_value = Response()
            signup_resp = test_client.post('/business/signup/email', json=business_data)
            mock_send_verification_email.assert_called_once()
            self.assertEqual(signup_resp.status_code, 201)
            # 2. Confirm user
            saved_business = BusinessModel.find_user_by_email(business_data['email'])
            saved_business.most_recent_confirmation.confirmed = True
            saved_business.save_user_to_db()
            # 3. Sign in
            signin_details = {'email': business_data['email'], 'password': business_data['password']}
            signin_resp = test_client.post('/business/signin/email', json=signin_details)
            self.assertEqual(signin_resp.status_code, 200)
            self.assertIn('access_token', signin_resp.json)
            self.assertIn('refresh_token', signin_resp.json)
            # 4. Sign out
            access_token = create_access_token(identity=saved_business.id, fresh=True)
            header = {'Authorization': f'Bearer {access_token}'}
            signout_resp = test_client.post('/business/signout', headers=header)
            self.assertEqual(signout_resp.json, {'msg': 'Sign out successful'})
            self.assertEqual(signout_resp.status_code, 200)
