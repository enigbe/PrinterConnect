from unittest import TestCase
from unittest.mock import patch
from requests import Response

from models.client.client import ClientModel
from libs.strings import client


class ClientTest(TestCase):
    def test_client_constructor(self):
        sample_client = ClientModel(**client.copy())

        self.assertEqual(sample_client.email, 'janedoe@email.com')
        self.assertEqual(sample_client.username, 'jane_d')
        self.assertEqual(sample_client.first_name, 'jane')
        self.assertEqual(sample_client.last_name, 'doe')

    def test_client_repr(self):
        sample_client = ClientModel(**client.copy())
        repr_output = '<Client => jane doe: [@jane_d - (janedoe@email.com)]>'

        self.assertEqual(sample_client.__repr__(), repr_output)

    def test_verify_password(self):
        sample_client = ClientModel(**client.copy())
        sample_client.hash_password(sample_client.password)
        verified_password = sample_client.verify_password('12345678')

        self.assertIs(verified_password, True)

    @patch('models.client.client.ClientModel.send_verification_email')
    def test_verify_email(self, mock_send_verification_email):
        sample_client = ClientModel(**client.copy())
        mock_send_verification_email.return_value = Response()
        response = sample_client.send_verification_email()
        self.assertIsInstance(response, Response)
