from unittest.mock import patch
from requests import Response

from tests.base_test import BaseTest
from models.client.client import ClientModel
from models.client.confirmation import ConfirmationModel
from tests.test_data import client


class ConfirmationModelTest(BaseTest):
    def test_save_confirmation_to_db(self):
        with self.app_context():
            sample_client = ClientModel(**client)
            self.assertIsNone(ClientModel.find_client_by_email(sample_client.email))
            sample_client.save_client_to_db()
            self.assertIsNotNone(ClientModel.find_client_by_email(sample_client.email))
            self.assertIsNone(sample_client.most_recent_confirmation)
            confirmation = ConfirmationModel(sample_client.id)
            confirmation.save_to_db()
            self.assertIsNotNone(confirmation.find_by_client_id(sample_client.id))

    def test_delete_confirmation_from_db(self):
        with self.app_context():
            sample_client = ClientModel(**client)
            self.assertIsNone(ClientModel.find_client_by_email(sample_client.email))
            sample_client.save_client_to_db()
            self.assertIsNotNone(ClientModel.find_client_by_email(sample_client.email))
            self.assertIsNone(sample_client.most_recent_confirmation)
            confirmation = ConfirmationModel(sample_client.id)
            confirmation.save_to_db()
            self.assertIsNotNone(sample_client.most_recent_confirmation)
            confirmation.delete_from_db()
            self.assertIsNone(sample_client.most_recent_confirmation)

    @patch.object(ClientModel, 'send_verification_email')
    def test_find_confirmation_by_id(self, mock_send_verification_email):
        # 1. With a test client and in an application context, create a client and confirmation
        # (mock the send_verification_email method)
        # 2. The client.most_recent_confirmation.id == ConfirmationModel.find_by_id().id
        with self.app() as test_client:
            with self.app_context():
                mock_send_verification_email.return_value = Response()
                sample_client = client.copy()
                test_client.post('/client/signup/email', json=sample_client)
                mock_send_verification_email.assert_called_once()
                loaded_client = ClientModel.find_client_by_email(sample_client['email'])
                confirmation = ConfirmationModel.find_by_client_id(loaded_client.id)
                for item in confirmation:
                    self.assertIsInstance(item, ConfirmationModel)
                    self.assertEqual(loaded_client.id, item.client_id)

    @patch('resources.client.signup_email_password.ClientModel.send_verification_email')
    def test_confirmation_has_expired(self, mock_send_verification_email):
        with self.app() as test_client:
            with self.app_context():
                mock_send_verification_email.return_value = Response()
                sample_client = client
                test_client.post('/client/signup/email', json=sample_client)
                mock_send_verification_email.assert_called_once()
                loaded_client = ClientModel.find_client_by_email(sample_client['email'])
                confirmation = ConfirmationModel.find_by_client_id(loaded_client.id)
                for item in confirmation:
                    self.assertEqual(item.has_expired, False)

    @patch('resources.client.signup_email_password.ClientModel.send_verification_email')
    def test_confirmation_forced_to_expire(self, mock_send_verification_email):
        with self.app() as test_client:
            with self.app_context():
                mock_send_verification_email.return_value = Response()
                sample_client = client
                test_client.post('/client/signup/email', json=sample_client)
                loaded_client = ClientModel.find_client_by_email(sample_client['email'])
                mock_send_verification_email.assert_called_once()
                confirmation = ConfirmationModel.find_by_client_id(loaded_client.id)
                for item in confirmation:
                    initial_expiration_time = item.expire_at
                    item.force_to_expire()
                    current_expiration_time = item.expire_at
                    self.assertGreater(initial_expiration_time, current_expiration_time)
