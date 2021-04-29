from models.client.confirmation import ConfirmationModel
from tests.base_test import BaseTest
from models.client.client import ClientModel


class ClientTest(BaseTest):
    def test_find_client_with_email(self):
        with self.app_context():
            client = ClientModel(
                email='janedoe@email.com',
                username='jane_d',
                first_name='jane',
                last_name='doe',
                password='123456789'
            )
            client.save_client_to_db()

            expected_client = ClientModel.find_client_by_email('janedoe@email.com')
            self.assertEqual(expected_client, client)

    def test_find_client_with_username(self):
        with self.app_context():
            client = ClientModel(
                email='janedoe@email.com',
                username='jane_d',
                first_name='jane',
                last_name='doe',
                password='123456789'
            )
            client.save_client_to_db()

            expected_client = ClientModel.find_client_by_username('jane_d')
            self.assertEqual(expected_client, client)

    def test_create_client(self):
        with self.app_context():
            client = ClientModel(
                email='janedoe@email.com',
                username='jane_d',
                first_name='jane',
                last_name='doe',
                password='123456789'
            )

            self.assertIsNone(ClientModel.find_client_by_email('janedoe@email.com'))
            client.save_client_to_db()
            self.assertIsNotNone(ClientModel.find_client_by_email('janedoe@email.com'))

    def test_delete_client(self):
        with self.app_context():
            client = ClientModel(
                email='janedoe@email.com',
                username='jane_d',
                first_name='jane',
                last_name='doe',
                password='123456789'
            )
            client.save_client_to_db()

            self.assertIsNotNone(ClientModel.find_client_by_username('jane_d'))
            client.delete_client_from_db()
            self.assertIsNone(ClientModel.find_client_by_username('jane_d'))

    def test_most_recent_confirmation(self):
        with self.app_context():

            client = ClientModel(
                email='janedoe@email.com',
                username='jane_d',
                first_name='jane',
                last_name='doe',
                password='123456789'
            )
            client.save_client_to_db()

            confirmation = ConfirmationModel(1)
            confirmation.save_to_db()

            self.assertIsInstance(client.most_recent_confirmation, ConfirmationModel)
