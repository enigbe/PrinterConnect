from unittest.mock import Mock
from flask_jwt_extended.exceptions import NoAuthorizationError

from tests.base_test import BaseTest
from models.client.client import ClientModel
from models.client.confirmation import ConfirmationModel
from tests.test_data import client
from libs.user_helper import save_and_confirm_user


class SetPasswordTest(BaseTest):

    def test_missing_auth_jwt(self):
        with self.app() as test_client:
            with self.app_context():
                # with patch('resources.client.set_password.SetPassword.post') as mock_post:
                test_client.post = Mock()
                test_client.post.side_effect = NoAuthorizationError
                signin_request_data = {'email': 'janedoe@email.com', 'password': 'pyotorovich'}
                with self.assertRaises(NoAuthorizationError, msg='Missing Authorization Header'):
                    test_client.post('/client/password',
                                     json=signin_request_data,
                                     headers={'Content-Type': 'application/json'}
                                     )

    def test_auth_jwt_available(self):
        with self.app() as test_client:
            with self.app_context():

                new_client = ClientModel(**client.copy())
                new_client.hash_password(password=client['password'])
                save_and_confirm_user(new_client)

                signin_request_data = {'email': 'janedoe@email.com', 'password': '12345678'}
                signin_response = test_client.post('/client/signin/email',
                                                   json=signin_request_data,
                                                   headers={'Content-Type': 'application/json'}
                                                   )
                authorization_token = signin_response.json['access_token']
                header = {'Authorization': 'Bearer {}'.format(authorization_token)}

                set_password_request_data = {'email': 'janedoe@email.com', 'password': 'pyotorovich'}
                set_password_response = test_client.post('/client/password',
                                                         json=set_password_request_data,
                                                         headers=header
                                                         )

                self.assertEqual(set_password_response.status_code, 201)
                self.assertEqual(set_password_response.json, {'msg': 'Password updated successfully.'})
