from unittest.mock import patch

from tests.base_test import BaseTest
from tests.test_data import facebook_user_data
from resources.client.signin_facebook import facebook


class FacebookSignInTest(BaseTest):
    @patch.object(facebook, 'authorize')
    def test_facebook_redirect(self, mock_authorize):
        with self.app() as test_client:
            with self.app_context():
                mock_authorize.return_value = 'Redirect to Facebook'
                response = test_client.get('/client/signin/facebook')
                mock_authorize.assert_called_once()
                self.assertEqual(response.status_code, 200)

    @patch.object(facebook, 'get')
    @patch.object(facebook, 'authorized_response')
    def test_facebook_callback_successful(self, mock_authorized_response, mock_get):
        with self.app() as test_client:
            with self.app_context():
                mock_authorized_response.return_value = {
                    'access_token': 'access_token'
                }
                mock_get.return_value.data = facebook_user_data.copy()
                response = test_client.get('/client/facebook/auth')

                mock_authorized_response.assert_called_once()
                mock_get.assert_called_once()

                self.assertIn('access_token', response.json)
                self.assertIn('refresh_token', response.json)
