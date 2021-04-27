from unittest.mock import patch
from requests import Response

from models.client.client import ClientModel
from tests.base_test import BaseTest
from schema.client.client import ClientSchema

client_schema = ClientSchema()


class ClientEmailSignUpTest(BaseTest):
    def test_create_client_user(self):
        with self.app() as test_client:
            with self.app_context():
                signup_details = {
                    'email': 'janedoe@email.com',
                    'username': 'jane_d',
                    'first_name': 'Jane',
                    'last_name': 'Doe',
                    'password': '12345'
                }

                response = test_client.post(
                    '/client/signup/email',
                    json=signup_details,
                    headers={'Content-Type': 'application/json'}
                )

                self.assertEqual(201, response.status_code)

                self.assertIsNotNone(ClientModel.find_client_by_username('jane_d'))
                expected_response = {'msg': 'Client account created successfully. Check email to verify account'}
                # response.get_json() or json.loads(response.data)
                self.assertDictEqual(response.get_json(), expected_response)

    def test_client_unique_email(self):
        with self.app() as test_client:
            with self.app_context():

                first_signup_details = {
                    'email': 'janedoe@email.com',
                    'username': 'jane_d',
                    'first_name': 'Jane',
                    'last_name': 'Doe',
                    'password': '12345'
                }
                # Different signup details with same email as above
                second_signup_details = {
                    'email': 'janedoe@email.com',
                    'username': 'john_d',
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'password': '12345'
                }

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
                self.assertEqual(400, response.status_code)

                expected_response_data = {
                    'msg': 'A user with email \'{}\' already exists.'.format('janedoe@email.com')
                }
                self.assertEqual(expected_response_data, response.get_json())

    def test_client_unique_username(self):
        with self.app() as test_client:
            with self.app_context():
                first_signup_details = {
                    'email': 'janedoe@email.com',
                    'username': 'jane_d',
                    'first_name': 'Jane',
                    'last_name': 'Doe',
                    'password': '12345'
                }
                # Different signup details with same username as above
                second_signup_details = {
                    'email': 'johndoe@email.com',
                    'username': 'jane_d',
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'password': '12345'
                }

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
                self.assertEqual(400, response.status_code)

                expected_response_data = {'msg': 'A user with username \'{}\' already exists.'.format('jane_d')}
                self.assertEqual(expected_response_data, response.get_json())

    def test_verify_email(self):
        with self.app() as test_client:
            with self.app_context():
                with patch('models.client.client.ClientModel.verify_email') as mocked_verify_email:
                    mocked_verify_email.return_value = Response()
                    request_details = {
                        'email': 'janedoe@email.com',
                        'username': 'jane_d',
                        'first_name': 'Jane',
                        'last_name': 'Doe',
                        'password': '12345678'
                    }

                    response = test_client.post('/client/signup/email', json=request_details)
                    mocked_verify_email.assert_called_once()
                    self.assertEqual(response.status_code, 201)
                    expected_dict = {
                        'msg': 'Client account created successfully. Check your email to activate your account'}
                    self.assertDictEqual(expected_dict, response.get_json())
