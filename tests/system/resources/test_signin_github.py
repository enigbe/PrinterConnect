from unittest.mock import patch

from tests.base_test import BaseTest
from tests.test_data import github_authorized_response, github_user_data
from resources.client.signin_github import github


class GithubSignInTest(BaseTest):

    AUTHORIZED_RESPONSE_DATA = github_authorized_response.copy()

    @patch.object(github, 'authorize')
    def test_github_redirect(self, mock_authorize):
        with self.app() as test_client:
            with self.app_context():
                mock_authorize.return_value = 'Redirect to Github'
                response = test_client.get('/client/signin/github')
                mock_authorize.assert_called_once()
                self.assertEqual(response.status_code, 200)

    @patch.object(github, 'get')
    @patch.object(github, 'authorized_response', return_value=AUTHORIZED_RESPONSE_DATA)
    def test_github_callback_successful(self, mock_github_authorized_response, mock_github_get):
        with self.app() as test_client:
            with self.app_context():
                mock_github_get.return_value.data = github_user_data.copy()

                response = test_client.get('/client/github/auth')

                mock_github_authorized_response.assert_called_once()
                mock_github_get.assert_called_once()

                self.assertIn('access_token', response.json)
                self.assertIn('refresh_token', response.json)
