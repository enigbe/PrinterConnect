from unittest import TestCase
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
