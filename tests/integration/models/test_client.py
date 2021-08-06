from models.shared_user.confirmation import ConfirmationModel
from tests.base_test import BaseTest
from models.client.client import ClientModel
from schema.client.client import ClientSchema
from tests.test_data import client, updated_client_data

client_schema = ClientSchema(only=('email', 'username', 'first_name', 'last_name', 'bio',))


class ClientTest(BaseTest):
    def test_find_client_with_email(self):
        with self.app_context():
            sample_client = ClientModel(**client)
            self.assertIsNone(ClientModel.find_user_by_email(sample_client.email))
            sample_client.save_user_to_db()
            self.assertIsNotNone(ClientModel.find_user_by_email(sample_client.email))

    def test_find_client_with_username(self):
        with self.app_context():
            sample_client = ClientModel(**client)
            self.assertIsNone(ClientModel.find_user_by_username(sample_client.username))
            sample_client.save_user_to_db()
            self.assertIsNotNone(ClientModel.find_user_by_username(sample_client.username))

    def test_create_client(self):
        with self.app_context():
            with self.app_context():
                sample_client = ClientModel(**client)
                self.assertIsNone(ClientModel.find_user_by_username(sample_client.username))
                sample_client.save_user_to_db()
                self.assertIsNotNone(ClientModel.find_user_by_username(sample_client.username))

    def test_delete_client(self):
        with self.app_context():
            with self.app_context():
                sample_client = ClientModel(**client)
                self.assertIsNone(ClientModel.find_user_by_username(sample_client.username))
                sample_client.save_user_to_db()
                self.assertIsNotNone(ClientModel.find_user_by_username(sample_client.username))
                sample_client.delete_user_from_db()
                self.assertIsNone(ClientModel.find_user_by_username(sample_client.username))

    def test_most_recent_confirmation(self):
        with self.app_context():
            sample_client = ClientModel(**client)
            self.assertIsNone(ClientModel.find_user_by_id(sample_client.id))
            sample_client.save_user_to_db()
            self.assertIsNotNone(ClientModel.find_user_by_id(sample_client.id))
            confirmation = ConfirmationModel(sample_client)
            self.assertIsNone(ConfirmationModel.find_by_id(confirmation.id))
            confirmation.save_to_db()
            self.assertIsNotNone(ConfirmationModel.find_by_id(confirmation.id))
            self.assertIsInstance(sample_client.most_recent_confirmation, ConfirmationModel)

    def test_update_client(self):
        with self.app_context():
            sample_client = ClientModel(**client)
            self.assertIsNone(ClientModel.find_user_by_id(sample_client.id))
            sample_client.save_user_to_db()
            self.assertIsNotNone(ClientModel.find_user_by_id(sample_client.id))

            existing_client = ClientModel.find_user_by_id(sample_client.id)
            self.assertNotEqual(existing_client.bio, updated_client_data['bio'])
            sample_client.bio = updated_client_data['bio']
            sample_client.update_user_in_db()
            self.assertEqual(existing_client.bio, sample_client.bio)
