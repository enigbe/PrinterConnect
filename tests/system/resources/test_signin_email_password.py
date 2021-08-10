from unittest.mock import patch
from requests import Response

from tests.base_test import BaseTest
from tests.test_data import client
from models.client.client import ClientModel


class ClientEmailSignInTest(BaseTest):
    @patch.object(ClientModel, 'send_verification_email')
    def test_valid_confirmed_signin_credentials(self, mock_send_verification_email):
        with self.app() as test_client:
            with self.app_context():
                # 1. Create a new client user

                mock_send_verification_email.return_value = Response()
                url = '/client/signup/email'
                sample_client = client.copy()
                response_new_client = test_client.post(
                    url,
                    json=sample_client,
                    headers={'Content-Type': 'application/json'}
                )

                mock_send_verification_email.assert_called_once()

                expected = {
                    'msg': 'Client account created successfully. Check your email to activate your account'
                }
                self.assertEqual(response_new_client.status_code, 201)
                self.assertEqual(response_new_client.json, expected)
                self.assertIsNotNone(ClientModel.find_user_by_email(sample_client['email']))

                # 2. Confirm the client
                created_client = ClientModel.find_user_by_email(sample_client['email'])
                client_confirmation_id = created_client.most_recent_confirmation.id
                test_client.get(f'/client/confirmation/{client_confirmation_id}')
                self.assertEqual(created_client.most_recent_confirmation.confirmed, True)

                # 3. Sign in
                client_signin = {'email': sample_client['email'], 'password': sample_client['password']}
                signin_response = test_client.post(
                    '/client/signin/email',
                    json=client_signin,
                    headers={'Content-Type': 'application/json'}
                )
                signin_response_data = signin_response.get_json()
                mock_send_verification_email.call_count = 2

                self.assertEqual(signin_response.status_code, 200)
                self.assertEqual(signin_response_data['msg'], 'Sign in successful.')
                self.assertIn('access_token', signin_response_data.keys())

    @patch('resources.client.signup_email_password.ClientModel.send_verification_email')
    def test_signin_client_exists(self, mock_send_verification_email):
        with self.app() as test_client:
            with self.app_context():
                # 1. Create a new client user
                mock_send_verification_email.return_value = Response()
                url = '/client/signup/email'
                sample_client_request = client.copy()
                response_new_client = test_client.post(
                    url,
                    json=sample_client_request,
                    headers={'Content-Type': 'application/json'}
                )

                mock_send_verification_email.assert_called_once()

                expected = {
                    'msg': 'Client account created successfully. Check your email to activate your account'
                }

                self.assertEqual(response_new_client.status_code, 201)
                self.assertEqual(response_new_client.get_json(), expected)

                # 2. Check the client exists
                created_client = ClientModel.find_user_by_email(client['email'])
                self.assertIsInstance(created_client, ClientModel)

    @patch('resources.client.signup_email_password.ClientModel.send_verification_email')
    def test_invalid_signin_credentials(self, mock_send_verification_email):
        with self.app() as test_client:
            with self.app_context():
                # 1. Create a new client user

                mock_send_verification_email.return_value = Response()
                url = '/client/signup/email'
                sample_client = client.copy()
                response_new_client = test_client.post(
                    url,
                    json=sample_client,
                    headers={'Content-Type': 'application/json'}
                )
                mock_send_verification_email.assert_called_once()

                expected = {
                    'msg': 'Client account created successfully. Check your email to activate your account'
                }
                self.assertEqual(response_new_client.status_code, 201)
                self.assertEqual(response_new_client.get_json(), expected)

                # 2. Check if a different client exists
                different_client = {'email': 'johndoe@email.com', 'password': sample_client['password']}
                response = test_client.post(
                    '/client/signin/email',
                    json=different_client,
                    headers={'Content-Type': 'application/json'}
                )

                mock_send_verification_email.call_count = 2
                self.assertEqual(response.status_code, 401)
                self.assertEqual(response.get_json(), {'msg': 'Invalid sign in credentials.'})

    @patch('resources.client.signup_email_password.ClientModel.send_verification_email')
    def test_client_not_confirmed(self, mock_send_verification_email):
        with self.app() as test_client:
            with self.app_context():
                # 1. Create a new client user

                mock_send_verification_email.return_value = Response()
                url = '/client/signup/email'
                sample_client = client.copy()
                response_new_client = test_client.post(
                    url,
                    json=sample_client,
                    headers={'Content-Type': 'application/json'}
                )
                mock_send_verification_email.assert_called_once()

                expected = {
                    'msg': 'Client account created successfully. Check your email to activate your account'
                }
                self.assertEqual(response_new_client.status_code, 201)
                self.assertEqual(response_new_client.get_json(), expected)

                # 2. Sign in
                client_signin = {'email': sample_client['email'], 'password': sample_client['password']}
                signin_response = test_client.post(
                    '/client/signin/email',
                    json=client_signin,
                    headers={'Content-Type': 'application/json'}
                )

                mock_send_verification_email.call_count = 2

                signin_response_data = signin_response.json
                exp = {'msg': 'Your account has not been confirmed. Please check your email for the confirmation link or request a new confirmation link.'}
                self.assertEqual(signin_response_data, exp)
                self.assertEqual(signin_response.status_code, 401)
