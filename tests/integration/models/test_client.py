from werkzeug.security import generate_password_hash, check_password_hash
from tests.base_test import BaseTest
from models.client.client import ClientModel


class ClientTest(BaseTest):
    def test_verify_password(self):
        with self.app_context():
            client = ClientModel('janedoe@email.com', 'jane_d', 'jane', 'doe', '12345')
            verified_password = client.verify_password('12345')

            self.assertIs(verified_password, True)

    def test_find_client_with_email(self):
        with self.app_context():
            client = ClientModel('janedoe@email.com', 'jane_d', 'jane', 'doe', '12345')
            client.save_client_to_db()

            expected_client = ClientModel.find_client_by_email('janedoe@email.com')
            self.assertEqual(expected_client, client)

    def test_find_client_with_username(self):
        with self.app_context():
            client = ClientModel('janedoe@email.com', 'jane_d', 'jane', 'doe', '12345')
            client.save_client_to_db()

            expected_client = ClientModel.find_client_by_username('jane_d')
            self.assertEqual(expected_client, client)

    def test_create_client(self):
        with self.app_context():
            client = ClientModel('janedoe@email.com', 'jane_d', 'jane', 'doe', '12345')

            self.assertIsNone(ClientModel.find_client_by_email('janedoe@email.com'))
            client.save_client_to_db()
            self.assertIsNotNone(ClientModel.find_client_by_email('janedoe@email.com'))

    def test_delete_client(self):
        with self.app_context():
            client = ClientModel('janedoe@email.com', 'jane_d', 'jane', 'doe', '12345')
            client.save_client_to_db()

            self.assertIsNotNone(ClientModel.find_client_by_username('jane_d'))
            client.delete_client_from_db()
            self.assertIsNone(ClientModel.find_client_by_username('jane_d'))
