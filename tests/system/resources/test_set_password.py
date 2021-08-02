from unittest.mock import patch
from requests import Response


from tests.base_test import BaseTest
from models.client.client import ClientModel
from tests.test_data import client
from libs.user_helper import generate_random_password


class SetPasswordTest(BaseTest):
    @patch.object(ClientModel, 'send_verification_email')
    def test_missing_auth_jwt(self, mock_send_verification_email):
        with self.app() as test_client, self.app_context():
            # signup
            mock_send_verification_email.return_value = Response()
            signup_resp = test_client.post(f'/client/signup/email', json=client)
            self.assertEqual(signup_resp.status_code, 201)
            mock_send_verification_email.assert_called_once()
            # confirm user
            saved_client_user = ClientModel.find_user_by_email(client['email'])
            confirmation_id = saved_client_user.most_recent_confirmation.id
            confirm_resp = test_client.get(f'/client/confirmation/{confirmation_id}')
            self.assertEqual(confirm_resp.status_code, 200)
            # signin
            client_user = {'email': client['email'], 'password': client['password']}
            signin_resp = test_client.post('/client/signin/email', json=client_user)
            self.assertEqual(signin_resp.status_code, 200)
            self.assertIn('access_token', signin_resp.json)
            self.assertIn('refresh_token', signin_resp.json)
            # set password
            password = generate_random_password()
            sp_resp = test_client.post(f'/{client}/{client["username"]}/profile/password', json=password)
            self.assertEqual(sp_resp.json, {'msg': 'Missing Authorization Header'})
            self.assertEqual(sp_resp.status_code, 401)

    @patch.object(ClientModel, 'send_verification_email')
    def test_auth_with_jwt(self, mock_send_verification_email):
        with self.app() as test_client, self.app_context():
            # signup
            mock_send_verification_email.return_value = Response()
            signup_resp = test_client.post(f'/client/signup/email', json=client)
            self.assertEqual(signup_resp.status_code, 201)
            mock_send_verification_email.assert_called_once()
            # confirm user
            saved_client_user = ClientModel.find_user_by_email(client['email'])
            confirmation_id = saved_client_user.most_recent_confirmation.id
            confirm_resp = test_client.get(f'/client/confirmation/{confirmation_id}')
            self.assertEqual(confirm_resp.status_code, 200)
            # signin
            client_user = {'email': client['email'], 'password': client['password']}
            signin_resp = test_client.post('/client/signin/email', json=client_user)
            self.assertEqual(signin_resp.status_code, 200)
            self.assertIn('access_token', signin_resp.json)
            self.assertIn('refresh_token', signin_resp.json)
            # set password
            password = {'password': generate_random_password()}
            authorization_token = signin_resp.json['access_token']
            header = {'Authorization': 'Bearer {}'.format(authorization_token)}
            sp_resp = test_client.post(f'/client/{client["username"]}/profile/password', json=password, headers=header)
            self.assertEqual(sp_resp.status_code, 201)
            self.assertEqual(sp_resp.json, {'msg': 'Password updated successfully.'})


class PasswordResetLinkTest(BaseTest):
    @patch.object(ClientModel, 'send_password_reset_link')
    @patch.object(ClientModel, 'send_verification_email')
    def test_password_reset_link(self, mock_send_verification_email, mock_send_password_reset_link):
        with self.app() as test_client, self.app_context():
            # signup
            mock_send_verification_email.return_value = Response()
            mock_send_password_reset_link.return_value = Response()

            signup_resp = test_client.post(f'/client/signup/email', json=client)
            self.assertEqual(signup_resp.status_code, 201)
            mock_send_verification_email.assert_called_once()
            # confirm user
            saved_client_user = ClientModel.find_user_by_email(client['email'])
            confirmation_id = saved_client_user.most_recent_confirmation.id
            confirm_resp = test_client.get(f'/client/confirmation/{confirmation_id}')
            self.assertEqual(confirm_resp.status_code, 200)
            # send password reset link
            client_email = {'email': client['email']}
            prl_resp = test_client.post('/client/password/reset_link', json=client_email)
            mock_send_password_reset_link.assert_called_once()
            self.assertEqual(prl_resp.json, {'msg': 'Password reset link sent to email successfully'})
            self.assertEqual(prl_resp.status_code, 200)


class ResetPasswordTest(BaseTest):
    @patch.object(ClientModel, 'send_verification_email')
    def test_reset_password(self, mock_send_verification_email):
        with self.app() as test_client, self.app_context():
            # signup
            mock_send_verification_email.return_value = Response()
            signup_resp = test_client.post(f'/client/signup/email', json=client)
            self.assertEqual(signup_resp.status_code, 201)
            mock_send_verification_email.assert_called_once()
            # confirm user
            saved_client_user = ClientModel.find_user_by_email(client['email'])
            confirmation_id = saved_client_user.most_recent_confirmation.id
            confirm_resp = test_client.get(f'/client/confirmation/{confirmation_id}')
            self.assertEqual(confirm_resp.status_code, 200)
            # signin with current password
            new_client_data = {'email': client['email'], 'password': client['password']}
            signin_resp = test_client.post('/client/signin/email', json=new_client_data)
            self.assertEqual(signin_resp.status_code, 200)
            self.assertIn('access_token', signin_resp.json)
            self.assertIn('refresh_token', signin_resp.json)
            # reset password
            client_data = {'email': client['email'], 'password': generate_random_password()}
            reset_resp = test_client.post('/client/password/reset', json=client_data)
            self.assertEqual(reset_resp.json, {'msg': 'Password updated successfully.'})
            self.assertEqual(reset_resp.status_code, 201)
            # signin with new password
            new_client_data = {'email': client['email'], 'password': client_data['password']}
            signin_resp = test_client.post('/client/signin/email', json=new_client_data)
            self.assertEqual(signin_resp.status_code, 200)
            self.assertIn('access_token', signin_resp.json)
            self.assertIn('refresh_token', signin_resp.json)


