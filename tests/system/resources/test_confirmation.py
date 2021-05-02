from unittest.mock import patch
from requests import Response

from models.client.client import ClientModel
from models.client.confirmation import ConfirmationModel
from tests.base_test import BaseTest
from tests.test_data import client


class ConfirmationTest(BaseTest):
    def test_confirmation_successfully_created(self):
        with self.app() as test_client:
            with self.app_context():
                # # 1. Create a client with confirmation
                # # 2. Get the confirmation
                # # 3. Assert
                sample_client = ClientModel(**client.copy())
                sample_client.save_client_to_db()

                confirmation = ConfirmationModel(1)
                confirmation.save_to_db()
                confirmation_id = sample_client.most_recent_confirmation.id
                url = '/client/confirmation/' + confirmation_id
                response_confirmation = test_client.get(url)

                expected_response = {'msg': 'janedoe@email.com activated successfully. You can now sign in.'}
                self.assertEqual(response_confirmation.status_code, 200)
                self.assertEqual(response_confirmation.get_json(), expected_response)

    @patch('models.client.client.ClientModel.send_verification_email')
    def test_confirmation_successfully_resent(self, mock_send_verification_email):
        with self.app() as test_client:
            with self.app_context():
                mock_send_verification_email.return_value = Response()

                sample_client = ClientModel(**client.copy())
                sample_client.save_client_to_db()

                confirmation = ConfirmationModel(1)
                confirmation.save_to_db()

                response = test_client.post('/client/resend_confirmation/janedoe@email.com')
                self.assertEqual(response.status_code, 201)
                expected = {'msg': 'Verification email resent successfully.'}
                self.assertEqual(response.get_json(), expected)

    def test_get_client_confirmations(self):
        with self.app() as test_client:
            with self.app_context():

                sample_client = ClientModel(**client.copy())
                sample_client.save_client_to_db()

                confirmation = ConfirmationModel(1)
                confirmation.save_to_db()

                response = test_client.get('/client/resend_confirmation/janedoe@email.com')
                print(response.get_json())
                self.assertEqual(response.status_code, 200)
                self.assertIn('current_time', response.get_json())
                self.assertIn('confirmation', response.get_json())
                self.assertIn('id', response.get_json()['confirmation'][0])
