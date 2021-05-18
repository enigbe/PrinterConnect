from unittest.mock import patch
from requests import Response

from models.client.client import ClientModel
from tests.base_test import BaseTest
from schema.client.client import ClientSchema
from tests.test_data import client

client_schema = ClientSchema()


class ClientEmailSignUpTest(BaseTest):
    @patch('resources.client.signup_email_password.ClientModel.send_verification_email')
    def test_create_client_user(self, mocked_send_verification_email):
        with self.app() as test_client:
            with self.app_context():
                mocked_send_verification_email.return_value = Response()

                signup_details = client.copy()

                response = test_client.post(
                    '/client/signup/email',
                    json=signup_details,
                    headers={'Content-Type': 'application/json'}
                )

                mocked_send_verification_email.assert_called_once()
                self.assertEqual(201, response.status_code)

                self.assertIsNotNone(ClientModel.find_client_by_username('jane_d'))
                expected_response = {
                    'msg': 'Client account created successfully. Check your email to activate your account'
                }
                # response.get_json() or json.loads(response.data)
                self.assertDictEqual(response.get_json(), expected_response)

    @patch('resources.client.signup_email_password.ClientModel.send_verification_email')
    def test_client_unique_email(self, mocked_send_verification_email):
        with self.app() as test_client:
            with self.app_context():
                mocked_send_verification_email.return_value = Response()
                # Two client requests with same email (details)
                first_signup_details = client.copy()
                second_signup_details = client.copy()
                second_signup_details['username'] = 'john_d'

                test_client.post(
                    '/client/signup/email',
                    json=first_signup_details,
                    headers={'Content-Type': 'application/json'}
                )
                response = test_client.post(
                    '/client/signup/email',
                    json=second_signup_details,
                    headers={'Content-Type': 'application/json'}
                )

                mocked_send_verification_email.called_count = 2

                self.assertEqual(400, response.status_code)

                expected_response_data = {
                    'msg': 'A user with email \'{}\' already exists.'.format('janedoe@email.com')
                }
                self.assertEqual(expected_response_data, response.get_json())

    @patch('resources.client.signup_email_password.ClientModel.send_verification_email')
    def test_client_unique_username(self, mocked_send_verification_email):
        with self.app() as test_client:
            with self.app_context():
                mocked_send_verification_email.return_value = Response()

                first_signup_details = client.copy()
                second_signup_details = client.copy()
                second_signup_details['email'] = 'johndoe@email.com'

                test_client.post(
                    '/client/signup/email',
                    json=first_signup_details,
                    headers={'Content-Type': 'application/json'}
                )
                response = test_client.post(
                    '/client/signup/email',
                    json=second_signup_details,
                    headers={'Content-Type': 'application/json'}
                )

                mocked_send_verification_email.called_count = 2

                self.assertEqual(400, response.status_code)

                expected_response_data = {'msg': 'A user with username \'{}\' already exists.'.format('jane_d')}
                self.assertEqual(expected_response_data, response.get_json())

    @patch('resources.client.signup_email_password.ClientModel.send_verification_email')
    def test_verify_email(self, mocked_send_verification_email):
        with self.app() as test_client:
            with self.app_context():
                mocked_send_verification_email.return_value = Response()
                signup_details = client.copy()

                response = test_client.post('/client/signup/email', json=signup_details)
                mocked_send_verification_email.assert_called_once()

                self.assertEqual(response.status_code, 201)
                expected_dict = {
                    'msg': 'Client account created successfully. Check your email to activate your account'}
                self.assertDictEqual(expected_dict, response.get_json())
