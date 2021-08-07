from unittest import TestCase
from unittest.mock import patch
from requests import Response

from models.client.client import ClientModel
from tests.test_data import client


class ClientTest(TestCase):
    def test_client_constructor(self):
        sample_client = ClientModel(**client)

        self.assertEqual(sample_client.email, client['email'])
        self.assertEqual(sample_client.username, client['username'])
        self.assertEqual(sample_client.first_name, client['first_name'])
        self.assertEqual(sample_client.last_name, client['last_name'])

    def test_client_repr(self):
        sample_client = ClientModel(**client)
        repr_output = f"<Client => {client['first_name']} {client['last_name']}: [@{client['username']} - ({client['email']})]>"

        self.assertEqual(sample_client.__repr__(), repr_output)

    def test_verify_password(self):
        sample_client = ClientModel(**client)
        sample_client.hash_password(sample_client.password)
        verified_password = sample_client.verify_password(client['password'])

        self.assertIs(verified_password, True)

    @patch('resources.client.signup_email_password.ClientModel.send_verification_email')
    def test_verify_email(self, mock_send_verification_email):
        sample_client = ClientModel(**client)
        mock_send_verification_email.return_value = Response()
        response = sample_client.send_verification_email()
        mock_send_verification_email.assert_called_once()
        self.assertIsInstance(response, Response)
