from unittest.mock import patch
from flask_jwt_extended import create_access_token

from tests.base_test import BaseTest
from resources.client import sign_out
from models.client.client import ClientModel
from resources.client.sign_out import TokenBlockListModel
from tests.test_data import client
from libs.user_helper import save_and_confirm_user


class SignOutTest(BaseTest):
    @patch.object(sign_out, 'get_jwt_identity', autospec=True)
    @patch.object(sign_out, 'get_jwt', autospec=True)
    def test_sign_out_successful(self, mock_get_jwt, mock_get_jwt_identity):
        """Test client sign in successful"""
        with self.app() as test_client:
            with self.app_context():
                # 1. Save a client to the db
                new_client = ClientModel(**client.copy())
                save_and_confirm_user(new_client)
                # 2. Mock jwt_required, get_jwt, get_jwt_identity
                mock_get_jwt.return_value = {'jti': 'JWTIdentity'}
                mock_get_jwt_identity.return_value = 1
                header = {
                    'Authorization': f'Bearer {create_access_token(identity=new_client.id)}'
                }
                resp = test_client.post('/client/signout', headers=header)
                # 3. Assert
                self.assertEqual(resp.json, {'msg': 'Sign out successful'})
                mock_get_jwt.assert_called_once()
                mock_get_jwt_identity.assert_called_once()

    @patch.object(TokenBlockListModel, 'save_token_to_db', autospec=True)
    @patch.object(sign_out, 'get_jwt_identity', autospec=True)
    @patch.object(sign_out, 'get_jwt', autospec=True)
    def test_sign_out_unsuccessful(self, mock_get_jwt, mock_get_jwt_identity, mock_save_to_be_db):
        """Test sign out not successful"""
        with self.app() as test_client:
            with self.app_context():
                # 1. Save a client to the db
                new_client = ClientModel(**client.copy())
                save_and_confirm_user(new_client)
                # 2. Mock jwt_required, get_jwt, get_jwt_identity
                mock_get_jwt.return_value = {'jti': 'JWTIdentity'}
                mock_get_jwt_identity.return_value = 'janedoe@email.com'
                mock_save_to_be_db.side_effect = Exception
                header = {
                    'Authorization': f'Bearer {create_access_token(identity=new_client.id)}'
                }
                with self.assertRaises(Exception, msg=''):
                    test_client.post('/client/signout', headers=header)
