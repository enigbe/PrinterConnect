from flask_jwt_extended import create_access_token

from models.client.client import ClientModel
from tests.base_test import BaseTest
from tests.test_data import client, searched_client
from libs.user_helper import save_and_confirm_user


class ClientSearchTest(BaseTest):
    def test_search_client_no_jwt(self):
        with self.app() as test_client:
            with self.app_context():
                sample_client = ClientModel(**client)
                save_and_confirm_user(sample_client)
                username = client['username']
                resp = test_client.get(f'/client/profile/search/{username}')
                self.assertEqual(resp.json, {'bio': None, 'username': client['username']})

    def test_search_client_with_jwt(self):
        with self.app() as test_client:
            with self.app_context():
                sample_client = ClientModel(**client)
                save_and_confirm_user(sample_client)

                access_token = create_access_token(identity=sample_client.id)
                header = {'Authorization': f'Bearer {access_token}'}
                username = client['username']
                resp = test_client.get(f'/client/profile/search/{username}', headers=header)
                self.assertEqual(resp.status_code, 200)

    def test_search_nonexistent_client(self):
        with self.app() as test_client:
            with self.app_context():
                sample_client = ClientModel(**client)
                save_and_confirm_user(sample_client)
                username = 'john_d'
                resp = test_client.get(f'/client/profile/search/{username}')
                self.assertEqual(resp.json, {'msg': 'Client does not exist.'})
