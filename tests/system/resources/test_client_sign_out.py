from unittest.mock import patch
from requests import Response

from flask_jwt_extended import create_access_token

from tests.base_test import BaseTest
from models.client.client import ClientModel
from tests.test_data import client


class ClientSignOutTest(BaseTest):
    @patch.object(ClientModel, 'send_verification_email')
    def test_sign_out_successful(self, mock_send_verification_email):
        """Test client sign in successful"""
        with self.app() as test_client, self.app_context():
            # 1. Create and confirm client user
            mock_send_verification_email.return_value = Response()
            signup_resp = test_client.post('/client/signup/email', json=client)
            mock_send_verification_email.assert_called_once()
            self.assertEqual(signup_resp.status_code, 201)
            # 2. Confirm user
            saved_client = ClientModel.find_user_by_email(client['email'])
            saved_client.most_recent_confirmation.confirmed = True
            saved_client.save_user_to_db()
            # 3. Sign in
            signin_details = {'email': client['email'], 'password': client['password']}
            signin_resp = test_client.post('/client/signin/email', json=signin_details)
            self.assertEqual(signin_resp.status_code, 200)
            self.assertIn('access_token', signin_resp.json)
            self.assertIn('refresh_token', signin_resp.json)
            # 4. Sign out
            access_token = create_access_token(identity=saved_client.id, fresh=True)
            header = {'Authorization': f'Bearer {access_token}'}
            signout_resp = test_client.post('/client/signout', headers=header)
            self.assertEqual(signout_resp.json, {'msg': 'Sign out successful'})
            self.assertEqual(signout_resp.status_code, 200)
