from unittest.mock import patch
from flask import Response
from flask_jwt_extended import create_access_token

from tests.base_test import BaseTest
from models.client.client import ClientModel
from libs.user_helper import save_and_confirm_user
from tests.test_data import client, searched_client


class ClientProfileTest(BaseTest):
    """Tests the read, update, and delete functionalities of the ClientProfile resource."""
    def test_read_client_exist_no_jwt(self):
        """Read existing client with no JWT"""
        with self.app() as test_client:
            with self.app_context():
                # 1. Save and confirm a client to db
                new_client = ClientModel(**client.copy())
                save_and_confirm_user(new_client)
                # 2. Check the client exist
                resp = test_client.get('/client/profile')
                self.assertEqual(resp.json, {'msg': 'Missing Authorization Header'})

    def test_read_client_exist_with_jwt(self):
        """Read existing client with JWT"""
        with self.app() as test_client:
            with self.app_context():
                # 1. Create client
                data = client.copy()
                new_client = ClientModel(**data)
                save_and_confirm_user(new_client)
                # 2. Get JWT linked to client's identity
                access_token = create_access_token(identity=new_client.id)
                header = {'Authorization': f'Bearer {access_token}'}
                # 3. Read client profile
                resp = test_client.get('/client/profile', headers=header)
                self.assertEqual(resp.json['client'], searched_client)

    def test_delete_client(self):
        """Test the delete client endpoint"""
        with self.app() as test_client:
            with self.app_context():
                # 1. Save and confirm a client to db
                new_client = ClientModel(**client.copy())
                save_and_confirm_user(new_client)
                # 2. Get JWT linked to client's identity
                access_token = create_access_token(identity=new_client.id, fresh=True)
                # 3. Check client is not None
                self.assertIsNotNone(ClientModel.find_client_by_username(client['username']))
                # 4. Delete client from database
                header = {'Authorization': f'Bearer {access_token}'}
                resp = test_client.delete('/client/profile', headers=header)
                self.assertIsNone(ClientModel.find_client_by_username(client['username']))
                self.assertDictEqual(resp.json, {'msg': "Client 'jane_d' successfully deleted."})

    @patch.object(ClientModel, 'send_update_email_notification', autospec=True)
    def test_update_email_provided(self, mock_send_update_email):
        with self.app() as test_client:
            with self.app_context():
                # 1. Create a client and save to db
                new_client = ClientModel(**client.copy())
                save_and_confirm_user(new_client)
                self.assertIsNotNone(ClientModel.find_client_by_email(client['email']))
                # 2. Mock send update email notification
                mock_send_update_email.return_value = Response()
                # 3. Check that email is changed
                update_email = 'johndoe@email.com'
                access_token = create_access_token(identity=new_client.id, fresh=True)
                header = {'Authorization': f'Bearer {access_token}'}
                resp = test_client.patch(
                    f'/client/profile',
                    json={'email': update_email},
                    headers=header
                )
                mock_send_update_email.assert_called_once()
                self.assertEqual(resp.json, {'msg': 'Profile update successful.'})
                self.assertIsNotNone(ClientModel.find_client_by_email(update_email))

    def test_update_username_provided(self):
        with self.app() as test_client:
            with self.app_context():
                # 1. Create a client and save to db
                new_client = ClientModel(**client.copy())
                save_and_confirm_user(new_client)
                self.assertIsNotNone(ClientModel.find_client_by_username(client['username']))
                # 3. Check that username is changed
                update_username = 'john_d'
                access_token = create_access_token(identity=new_client.id, fresh=True)
                header = {'Authorization': f'Bearer {access_token}'}
                resp = test_client.patch(
                    f'/client/profile',
                    json={'username': update_username},
                    headers=header
                )
                self.assertEqual(resp.json, {'msg': 'Profile update successful.'})
                self.assertIsNotNone(ClientModel.find_client_by_username(update_username))

    def test_update_first_name_provided(self):
        with self.app() as test_client:
            with self.app_context():
                # 1. Create a client and save to db
                new_client = ClientModel(**client.copy())
                save_and_confirm_user(new_client)
                self.assertIsNotNone(ClientModel.find_client_by_username(client['username']))
                # 3. Check that username is changed
                update_first_name = 'johnson'
                access_token = create_access_token(identity=new_client.id, fresh=True)
                header = {'Authorization': f'Bearer {access_token}'}
                resp = test_client.patch(
                    f'/client/profile',
                    json={'first_name': update_first_name},
                    headers=header
                )
                self.assertEqual(resp.json, {'msg': 'Profile update successful.'})
                self.assertEqual(new_client.first_name, update_first_name)

    def test_update_last_name_provided(self):
        with self.app() as test_client:
            with self.app_context():
                # 1. Create a client and save to db
                new_client = ClientModel(**client.copy())
                save_and_confirm_user(new_client)
                self.assertIsNotNone(ClientModel.find_client_by_username(client['username']))
                # 3. Check that username is changed
                update_last_name = 'swan'
                access_token = create_access_token(identity=new_client.id, fresh=True)
                header = {'Authorization': f'Bearer {access_token}'}
                resp = test_client.patch(
                    f'/client/profile',
                    json={'last_name': update_last_name},
                    headers=header
                )
                self.assertEqual(resp.json, {'msg': 'Profile update successful.'})
                self.assertEqual(new_client.last_name, update_last_name)

    def test_update_bio_provided(self):
        with self.app() as test_client:
            with self.app_context():
                # 1. Create a client and save to db
                new_client = ClientModel(**client.copy())
                save_and_confirm_user(new_client)
                self.assertIsNotNone(ClientModel.find_client_by_username(client['username']))
                # 3. Check that username is changed
                update_bio = 'bio updated'
                access_token = create_access_token(identity=new_client.id, fresh=True)
                header = {'Authorization': f'Bearer {access_token}'}
                resp = test_client.patch(
                    f'/client/profile',
                    json={'bio': update_bio},
                    headers=header
                )
                self.assertEqual(resp.json, {'msg': 'Profile update successful.'})
                self.assertEqual(new_client.bio, update_bio)
