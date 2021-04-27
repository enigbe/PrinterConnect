from unittest import TestCase
from unittest.mock import patch
from requests import Response

from models.client.client import ClientModel


class ClientTest(TestCase):
    def test_client_constructor(self):
        client = ClientModel('janedoe@email.com', 'jane_d', 'jane', 'doe', '12345')

        self.assertEqual(client.email, 'janedoe@email.com')
        self.assertEqual(client.username, 'jane_d')
        self.assertEqual(client.first_name, 'Jane')
        self.assertEqual(client.last_name, 'Doe')

    def test_client_repr(self):
        client = ClientModel('janedoe@email.com', 'jane_d', 'jane', 'doe', '12345')
        repr_output = '<Client => Jane Doe: [@jane_d - (janedoe@email.com)]>'

        self.assertEqual(client.__repr__(), repr_output)

    def test_verify_password(self):
        client = ClientModel('janedoe@email.com', 'jane_d', 'jane', 'doe', '12345')
        verified_password = client.verify_password('12345')

        self.assertIs(verified_password, True)

    def test_verify_email(self):
        client = ClientModel('janedoe@email.com', 'jane_d', 'Jane', 'Doe', '012345678')
        with patch('models.client.client.ClientModel.verify_email') as mocked_verify_email:
            mocked_verify_email.return_value = Response()
            response = client.verify_email()
            self.assertIsInstance(response, Response)
