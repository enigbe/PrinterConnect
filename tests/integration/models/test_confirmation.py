from unittest.mock import patch
from requests import Response

from tests.base_test import BaseTest
from models.client.client import ClientModel
from models.client.confirmation import ConfirmationModel
from libs.test_objects import client


class ConfirmationTest(BaseTest):
    def test_save_confirmation_to_db(self):
        with self.app_context():
            sample_client = ClientModel(**client.copy())
            sample_client.save_client_to_db()

            self.assertIsNone(sample_client.most_recent_confirmation)

            confirmation = ConfirmationModel(1)
            confirmation.save_to_db()

            self.assertIsNotNone(sample_client.most_recent_confirmation)

    def test_delete_confirmation_from_db(self):
        with self.app_context():
            sample_client = ClientModel(**client.copy())
            sample_client.save_client_to_db()
            sample_client.save_client_to_db()

            confirmation = ConfirmationModel(1)
            confirmation.save_to_db()

            self.assertIsNotNone(sample_client.most_recent_confirmation)

            confirmation.delete_from_db()
            self.assertIsNone(sample_client.most_recent_confirmation)

    @patch('models.client.client.ClientModel.send_verification_email')
    def test_find_confirmation_by_id(self, mock_send_verification_email):
        # 1. With a test client and in an application context, create a client and confirmation
        # (mock the send_verification_email method)
        # 2. The client.most_recent_confirmation.id == ConfirmationModel.find_by_id().id
        with self.app() as test_client:
            with self.app_context():
                mock_send_verification_email.return_value = Response()

                sample_client = client.copy()
                print(sample_client)
                test_client.post('/client/signup/email', json=sample_client)
                loaded_client = ClientModel.find_client_by_email('janedoe@email.com')
                confirmation = ConfirmationModel.find_by_id(loaded_client.most_recent_confirmation.id)
                self.assertIsInstance(confirmation, ConfirmationModel)
                self.assertEqual(loaded_client.id, confirmation.client_id)

    @patch('models.client.client.ClientModel.send_verification_email')
    def test_confirmation_has_expired(self, mock_send_verification_email):
        with self.app() as test_client:
            with self.app_context():
                mock_send_verification_email.return_value = Response()
                sample_client = client.copy()
                test_client.post('/client/signup/email', json=sample_client)
                loaded_client = ClientModel.find_client_by_email('janedoe@email.com')
                confirmation = ConfirmationModel.find_by_id(loaded_client.most_recent_confirmation.id)

                self.assertEqual(confirmation.has_expired, False)

    @patch('models.client.client.ClientModel.send_verification_email')
    def test_confirmation_forced_to_expire(self, mock_send_verification_email):
        with self.app() as test_client:
            with self.app_context():
                mock_send_verification_email.return_value = Response()
                sample_client = client.copy()
                test_client.post('/client/signup/email', json=sample_client)
                loaded_client = ClientModel.find_client_by_email('janedoe@email.com')

                confirmation = ConfirmationModel.find_by_id(loaded_client.most_recent_confirmation.id)
                initial_expiration_time = confirmation.expire_at

                confirmation.force_to_expire()
                current_expiration_time = confirmation.expire_at

                self.assertGreater(initial_expiration_time, current_expiration_time)
