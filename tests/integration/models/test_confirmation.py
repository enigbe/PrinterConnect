from unittest.mock import patch
from requests import Response

from tests.base_test import BaseTest
from models.client.client import ClientModel
from models.client.confirmation import ConfirmationModel


class ConfirmationTest(BaseTest):
    def test_save_confirmation_to_db(self):
        with self.app_context():
            client_details = {
                'email': 'janedoe@enc.com',
                'username': 'jane_d',
                'first_name': 'Jane',
                'last_name': 'Doe',
                'password': '0123456789'
            }
            client = ClientModel(**client_details)
            client.save_client_to_db()
            self.assertIsNone(client.most_recent_confirmation)

            confirmation = ConfirmationModel(1)
            confirmation.save_to_db()
            self.assertIsNotNone(client.most_recent_confirmation)

    def test_delete_confirmation_from_db(self):
        with self.app_context():
            client_details = {
                'email': 'janedoe@enc.com',
                'username': 'jane_d',
                'first_name': 'Jane',
                'last_name': 'Doe',
                'password': '0123456789'
            }
            client = ClientModel(**client_details)
            client.save_client_to_db()
            confirmation = ConfirmationModel(1)
            confirmation.save_to_db()
            self.assertIsNotNone(client.most_recent_confirmation)

            confirmation.delete_from_db()
            self.assertIsNone(client.most_recent_confirmation)

    def test_find_confirmation_by_id(self):
        # 1. With a test client and in an application context, create a client and confirmation
        # (mock the send_verification_email method)
        # 2. The client.most_recent_confirmation.id == ConfirmationModel.find_by_id().id
        with self.app() as test_client:
            with self.app_context():
                with patch('models.client.client.ClientModel.send_verification_email') as mock_send_verification_email:
                    mock_send_verification_email.return_value = Response()

                    client_request = {
                        'email': 'janedoe@enc.com',
                        'username': 'jane_d',
                        'first_name': 'Jane',
                        'last_name': 'Doe',
                        'password': '0123456789'
                    }
                    test_client.post('/client/signup/email', json=client_request)
                    client = ClientModel.find_client_by_email('janedoe@enc.com')

                    confirmation = ConfirmationModel.find_by_id(client.most_recent_confirmation.id)
                    self.assertIsInstance(confirmation, ConfirmationModel)
                    self.assertEqual(client.id, confirmation.client_id)

    def test_confirmation_has_expired(self):
        with self.app() as test_client:
            with self.app_context():
                with patch('models.client.client.ClientModel.send_verification_email') as mock_send_verification_email:
                    mock_send_verification_email.return_value = Response()
                    client_request = {
                        'email': 'janedoe@enc.com',
                        'username': 'jane_d',
                        'first_name': 'Jane',
                        'last_name': 'Doe',
                        'password': '0123456789'
                    }
                    test_client.post('/client/signup/email', json=client_request)
                    client = ClientModel.find_client_by_email('janedoe@enc.com')
                    confirmation = ConfirmationModel.find_by_id(client.most_recent_confirmation.id)

                    self.assertEqual(confirmation.has_expired, False)

    def test_confirmation_forced_to_expire(self):
        with self.app() as test_client:
            with self.app_context():
                with patch('models.client.client.ClientModel.send_verification_email') as mock_send_verification_email:
                    mock_send_verification_email.return_value = Response()
                    client_request = {
                        'email': 'janedoe@enc.com',
                        'username': 'jane_d',
                        'first_name': 'Jane',
                        'last_name': 'Doe',
                        'password': '0123456789'
                    }
                    test_client.post('/client/signup/email', json=client_request)
                    client = ClientModel.find_client_by_email('janedoe@enc.com')

                    confirmation = ConfirmationModel.find_by_id(client.most_recent_confirmation.id)
                    initial_expiration_time = confirmation.expire_at

                    confirmation.force_to_expire()
                    current_expiration_time = confirmation.expire_at

                    self.assertGreater(initial_expiration_time, current_expiration_time)