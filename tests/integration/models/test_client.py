from models.client.confirmation import ConfirmationModel
from tests.base_test import BaseTest
from models.client.client import ClientModel
from schema.client.client import ClientSchema
from tests.test_data import client, updated_client

client_schema = ClientSchema(only=('email', 'username', 'first_name', 'last_name', 'bio',))


class ClientTest(BaseTest):
    def test_find_client_with_email(self):
        with self.app_context():
            sample_client = ClientModel(**client.copy())
            sample_client.save_client_to_db()

            expected_client = ClientModel.find_client_by_email('janedoe@email.com')
            self.assertEqual(expected_client, sample_client)

    def test_find_client_with_username(self):
        with self.app_context():
            sample_client = ClientModel(**client.copy())
            sample_client.save_client_to_db()

            expected_client = ClientModel.find_client_by_username('jane_d')
            self.assertEqual(expected_client, sample_client)

    def test_create_client(self):
        with self.app_context():
            sample_client = ClientModel(**client.copy())

            self.assertIsNone(ClientModel.find_client_by_email('janedoe@email.com'))
            sample_client.save_client_to_db()
            self.assertIsNotNone(ClientModel.find_client_by_email('janedoe@email.com'))

    def test_delete_client(self):
        with self.app_context():
            sample_client = ClientModel(**client.copy())

            sample_client.save_client_to_db()

            self.assertIsNotNone(ClientModel.find_client_by_username('jane_d'))
            sample_client.delete_client_from_db()
            self.assertIsNone(ClientModel.find_client_by_username('jane_d'))

    def test_most_recent_confirmation(self):
        with self.app_context():

            sample_client = ClientModel(**client.copy())
            sample_client.save_client_to_db()

            confirmation = ConfirmationModel(1)
            confirmation.save_to_db()

            self.assertIsInstance(sample_client.most_recent_confirmation, ConfirmationModel)

    def test_update_client(self):
        with self.app_context():
            sample_client = ClientModel(**client.copy())
            sample_client.save_client_to_db()

            sample_client.bio = 'Bio updated'
            sample_client.update_client_in_db()

            self.assertEqual(client_schema.dump(sample_client), updated_client)


