from unittest.mock import patch

from tests.test_data import client
from libs.user_helper import save_and_confirm_user
from models.client.client import ClientModel
from tests.base_test import BaseTest
from libs.strings import gettext


class TokenRefreshTest(BaseTest):
    """Test refresh token endpoint"""
    @patch('resources.client.token_refresh.create_access_token', autospec=True)
    @patch('resources.client.token_refresh.get_jwt_identity', autospec=True)
    def test_refresh_token_provided(self, mock_get_jwt_identity, mock_create_access_token):
        """Refresh token provided"""
        with self.app() as test_client:
            with self.app_context():
                # 1. Arrange: Get refresh JWT (authorization) for header
                new_client = ClientModel(**client.copy())
                new_client.hash_password(password=client['password'])
                save_and_confirm_user(new_client)

                signin_request_data = {'email': client['email'], 'password': client['password']}

                signin_response = test_client.post(
                    '/client/signin/email',
                    json=signin_request_data,
                    headers={'Content-Type': 'application/json'}
                )

                authorization_token = signin_response.json['refresh_token']
                header = {
                    'Authorization': 'Bearer {}'.format(authorization_token),
                    'Content-Type': 'application/json'
                }
                # 2. Mock get_jwt_identity() and create_access_token()
                mock_get_jwt_identity.return_value = 'JWTIdentity'
                mock_create_access_token.return_value = 'refreshed_access_token'

                # 3. Act: Send post request to endpoint
                resp = test_client.post(
                    '/token/refresh',
                    headers=header
                )
                # 4. Assert
                mock_get_jwt_identity.assert_called_once()
                mock_create_access_token.assert_called_once()
                mock_create_access_token.assert_called_with(identity='JWTIdentity', fresh=False)
                self.assertEqual(resp.json, {'access_token': 'refreshed_access_token'})

    def test_access_token_used(self):
        """Access token provided"""
        with self.app() as test_client:
            with self.app_context():
                # 1. Arrange: Get refresh JWT (authorization) for header
                new_client = ClientModel(**client.copy())
                new_client.hash_password(password=client['password'])
                save_and_confirm_user(new_client)

                signin_request_data = {'email': client['email'], 'password': client['password']}
                signin_response = test_client.post(
                    '/client/signin/email',
                    json=signin_request_data,
                    headers={'Content-Type': 'application/json'}
                )

                authorization_token = signin_response.json['access_token']
                header = {
                    'Authorization': 'Bearer {}'.format(authorization_token),
                    'Content-Type': 'application/json'
                }
                # 3. Act: Send post request to endpoint
                resp = test_client.post(
                    '/token/refresh',
                    headers=header
                )
                # 4. Assert
                self.assertEqual(resp.json, {'msg': 'Only refresh tokens are allowed'})

    def test_no_token_used(self):
        """No token provided"""
        with self.app() as test_client:
            with self.app_context():
                # 1. Arrange: Create new client and get access and refresh tokens
                new_client = ClientModel(**client.copy())
                new_client.hash_password(password=client['password'])
                save_and_confirm_user(new_client)

                signin_request_data = {'email': client['email'], 'password': client['password']}

                test_client.post(
                    '/client/signin/email',
                    json=signin_request_data,
                    headers={'Content-Type': 'application/json'}
                )

                header = {
                    'Content-Type': 'application/json'
                }
                # 3. Act: Send post request to endpoint without JWT
                resp = test_client.post(
                    '/token/refresh',
                    headers=header
                )
                # 4. Assert
                self.assertEqual(resp.json, {'msg': 'Missing Authorization Header'})


class BlockedTokensTest(BaseTest):
    """Test the blocked tokens endpoint"""
    def test_blocked_tokens_existing_client(self):
        """Client already signed out"""
        with self.app() as test_client:
            with self.app_context():
                # ARRANGE
                # 1. Get new client
                new_client = ClientModel(**client.copy())
                new_client.hash_password(password=client['password'])
                save_and_confirm_user(new_client)
                # 2. Sign in client and get JWT
                signin_request_data = {'email': client['email'], 'password': client['password']}
                signin_response = test_client.post(
                    '/client/signin/email',
                    json=signin_request_data,
                    headers={'Content-Type': 'application/json'}
                )
                authorization_token = signin_response.json['access_token']
                header = {
                    'Authorization': 'Bearer {}'.format(authorization_token),
                    'Content-Type': 'application/json'
                }
                # 3. Sign out client
                signout_response = test_client.post(
                    '/client/signout',
                    headers=header
                )
                self.assertEqual(signout_response.status_code, 200)
                self.assertEqual(signout_response.json, {'msg': 'Sign out successful'})
                # ACT
                blocked_resp = test_client.get(f'/token/blocked/{client["email"]}')
                # 4. Send get request to endpoint
                # ASSERT
                self.assertEqual(blocked_resp.status_code, 200)
                self.assertIn('jti', blocked_resp.json['msg'][0])

    def test_blocked_tokens_no_client(self):
        """Client does not exist"""
        with self.app() as test_client:
            with self.app_context():
                # ARRANGE
                # 1. Get new client
                email = 'johndoe@email.com'
                # ACT
                blocked_resp = test_client.get(f'/token/blocked/{email}')
                # 2. Send get request to endpoint
                # ASSERT
                self.assertEqual(blocked_resp.status_code, 400)
                self.assertEqual(blocked_resp.json, {'msg': gettext('client_profile_client_does_not_exist')})

    def test_no_blocked_tokens_existing_client(self):
        """Client has not signed out"""
        with self.app() as test_client:
            with self.app_context():
                # ARRANGE
                # 1. Get new client
                new_client = ClientModel(**client.copy())
                new_client.hash_password(password=client['password'])
                save_and_confirm_user(new_client)
                # 2. Sign in client and get JWT
                signin_request_data = {'email': client['email'], 'password': client['password']}
                test_client.post(
                    '/client/signin/email',
                    json=signin_request_data,
                    headers={'Content-Type': 'application/json'}
                )
                blocked_resp = test_client.get(f'/token/blocked/{client["email"]}')
                # 3. Send get request to endpoint
                # ASSERT
                self.assertEqual(blocked_resp.status_code, 200)
                self.assertEqual(blocked_resp.json, {'msg': gettext('token_refresh_token_blocklist_empty')})
