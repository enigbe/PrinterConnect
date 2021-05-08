from unittest.mock import patch
from urllib.parse import unquote

from tests.base_test import BaseTest
from oa import github
from tests.test_data import github_authorized_response, github_user_data


class GithubTest(BaseTest):

    AUTHORIZED_RESPONSE_DATA = github_authorized_response.copy()

    def test_github_redirect(self):
        with self.app() as test_client:
            with self.app_context():

                response = test_client.get('/client/signin/github')

                self.assertEqual(response.status_code, 302)

                base_url = 'https://github.com/login/oauth/authorize'
                query = '?response_type=code&client_id=None&redirect_uri=http://localhost/client/github/auth&'
                scope = 'scope=read:user,user'
                expected_url = base_url + query + scope
                url = unquote(response.headers['Location'])

                self.assertEqual(expected_url, url)

    @patch.object(github, 'get')
    @patch.object(github, 'authorized_response', return_value=AUTHORIZED_RESPONSE_DATA)
    def test_github_callback_successful(self, mock_github_authorized_response, mock_github_get):
        with self.app() as test_client:
            with self.app_context():
                mock_github_get.return_value.data = github_user_data.copy()

                response = test_client.get('http://localhost:5001/client/github/auth')

                mock_github_authorized_response.assert_called_once()
                mock_github_get.assert_called_once()

                self.assertIn('access_token', response.json)
                self.assertIn('refresh_token', response.json)
