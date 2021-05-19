from unittest.mock import patch

from tests.base_test import BaseTest
from resources.client.signin_twitter import twitter
from tests.test_data import twitter_user_data


class TwitterSignInTest(BaseTest):
    def test_twitter_redirect(self):
        with self.app() as test_client:
            with self.app_context():
                with patch.object(twitter, 'authorize', return_value='Redirect to Twitter') as mock_twitter_authorize:
                    url = '/client/signin/twitter'
                    response = test_client.get(url)
                    mock_twitter_authorize.assert_called_once()
                    self.assertEqual(response.status_code, 200)

    @patch.object(twitter, 'get')
    @patch.object(twitter, 'authorized_response')
    def test_twitter_callback_successful(self, mock_twitter_authorized_response, mock_twitter_get):
        with self.app() as test_client:
            with self.app_context():
                mock_twitter_authorized_response.return_value = {
                    'oauth_token': 'oauth_token',
                    'oauth_token_secret': 'oauth_token_secret'
                }

                mock_twitter_get.return_value.data = twitter_user_data.copy()
                mock_twitter_get.return_value.status = 200

                response = test_client.get('/client/twitter/auth')

                mock_twitter_authorized_response.assert_called_once()
                mock_twitter_get.assert_called_once()

                self.assertIn('access_token', response.json)
                self.assertIn('refresh_token', response.json)
