from unittest.mock import patch
from requests import Response

from models.client.client import ClientModel
from models.shared_user.confirmation import ConfirmationModel
from tests.base_test import BaseTest
from tests.test_data import client


class ConfirmationResourceTest(BaseTest):
    def test_confirmation_successfully_created(self):
        with self.app() as test_client:
            with self.app_context():
                sample_client = ClientModel(**client)
                self.assertIsNone(ClientModel.find_user_by_email(sample_client.email))
                sample_client.save_user_to_db()
                self.assertIsNotNone(ClientModel.find_user_by_email(sample_client.email))
                confirmation = ConfirmationModel(sample_client)
                confirmation.save_to_db()
                confirmation_id = sample_client.most_recent_confirmation.id
                self.assertIsNotNone(ConfirmationModel.find_by_client_id(sample_client.id))
                url = '/client/confirmation/' + confirmation_id
                response_confirmation = test_client.get(url)
                expected_response = {'msg': f'{sample_client.email} activated successfully. You can now sign in.'}
                self.assertEqual(response_confirmation.status_code, 200)
                self.assertEqual(response_confirmation.get_json(), expected_response)

    @patch.object(ClientModel, 'send_verification_email')
    def test_confirmation_successfully_resent(self, mock_send_verification_email):
        with self.app() as test_client:
            with self.app_context():
                mock_send_verification_email.return_value = Response()
                sample_client = ClientModel(**client)
                sample_client.save_user_to_db()
                confirmation = ConfirmationModel(sample_client)
                confirmation.save_to_db()
                response = test_client.post(f'/client/re_confirmation/{sample_client.email}')
                mock_send_verification_email.assert_called_once()
                self.assertEqual(response.status_code, 201)
                expected = {'msg': 'Verification email resent successfully.'}
                self.assertEqual(response.get_json(), expected)

    def test_get_client_confirmations(self):
        with self.app() as test_client:
            with self.app_context():
                sample_client = ClientModel(**client)
                sample_client.save_user_to_db()
                confirmation = ConfirmationModel(sample_client)
                confirmation.save_to_db()
                response = test_client.get(f'/client/re_confirmation/{sample_client.email}')
                self.assertEqual(response.status_code, 200)
                self.assertIn('current_time', response.get_json())
                self.assertIn('confirmation', response.get_json())
                self.assertIn('id', response.get_json()['confirmation'][0])
