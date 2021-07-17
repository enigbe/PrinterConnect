from unittest.mock import patch
from flask_jwt_extended import create_access_token

from models.client.cad_model import CADModel
from models.client.client import ClientModel
from tests.base_test import BaseTest
from tests.test_data import cad_model_data, client, cad_model_update_data
from libs.aws_helper import s3_client


class CADModelResourceTest(BaseTest):
    def test_post_cad_model(self):
        with self.app() as test_client:
            with self.app_context():
                # Create authorization header
                access_token = create_access_token(identity=1, fresh=True)
                header = {'Authorization': f'Bearer {access_token}'}
                self.assertIsNone(CADModel.find_cad_model_by_id(1))
                # Create and save a client to DB
                sample_client = ClientModel(**client)
                self.assertIsNone(ClientModel.find_client_by_id(1))
                sample_client.save_client_to_db()
                self.assertIsNotNone(ClientModel.find_client_by_id(1))

                resp = test_client.post(
                    f'/client/cad_model/{cad_model_data["cad_model_name"]}', data=cad_model_data, headers=header)
                self.assertEqual(resp.status_code, 200)
                self.assertIn('url', resp.json)
                self.assertIn('fields', resp.json)
                self.assertIn('policy', resp.json['fields'])
                self.assertIn('signature', resp.json['fields'])
                self.assertIn('key', resp.json['fields'])
                self.assertIn('AWSAccessKeyId', resp.json['fields'])

    def test_get_cad_model(self):
        with self.app() as test_client:
            with self.app_context():
                # Create authorization header
                access_token = create_access_token(identity=1, fresh=True)
                header = {'Authorization': f'Bearer {access_token}'}
                self.assertIsNone(CADModel.find_cad_model_by_id(1))
                # Create and save a client to DB
                sample_client = ClientModel(**client)
                self.assertIsNone(ClientModel.find_client_by_id(1))
                sample_client.save_client_to_db()
                self.assertIsNotNone(ClientModel.find_client_by_id(1))

                post_resp = test_client.post(
                    f'/client/cad_model/{cad_model_data["cad_model_name"]}', data=cad_model_data, headers=header)
                self.assertEqual(post_resp.status_code, 200)
                get_resp = test_client.get(
                    f'/client/cad_model/{cad_model_data["cad_model_name"]}')
                self.assertEqual(get_resp.status_code, 200)

    @patch.object(s3_client, 'delete_object', autospec=True)
    def test_delete_cad_model(self, mock_delete_object):
        with self.app() as test_client:
            with self.app_context():
                # Create authorization header
                access_token = create_access_token(identity=1, fresh=True)
                header = {'Authorization': f'Bearer {access_token}'}
                self.assertIsNone(CADModel.find_cad_model_by_id(1))
                # Create and save a client to DB
                sample_client = ClientModel(**client)
                self.assertIsNone(ClientModel.find_client_by_id(1))
                sample_client.save_client_to_db()
                self.assertIsNotNone(ClientModel.find_client_by_id(1))

                post_resp = test_client.post(
                    f'/client/cad_model/{cad_model_data["cad_model_name"]}', data=cad_model_data, headers=header)
                self.assertEqual(post_resp.status_code, 200)
                # Delete CAD model
                mock_delete_object.return_value = {
                    'ResponseMetadata': {
                        'HTTPStatusCode': 204
                    }
                }
                delete_resp = test_client.delete(
                    f'/client/cad_model/{cad_model_data["cad_model_name"]}', headers=header)
                mock_delete_object.assert_called_once()
                self.assertEqual(delete_resp.status_code, 200)

    def test_update_cad_model(self):
        with self.app() as test_client:
            with self.app_context():
                # Create authorization header
                access_token = create_access_token(identity=1, fresh=True)
                header = {'Authorization': f'Bearer {access_token}'}
                self.assertIsNone(CADModel.find_cad_model_by_id(1))
                # Create and save a client to DB
                sample_client = ClientModel(**client)
                self.assertIsNone(ClientModel.find_client_by_id(1))
                sample_client.save_client_to_db()
                self.assertIsNotNone(ClientModel.find_client_by_id(1))

                post_resp = test_client.post(
                    f'/client/cad_model/{cad_model_data["cad_model_name"]}', data=cad_model_data, headers=header)
                self.assertEqual(post_resp.status_code, 200)
                patch_resp = test_client.patch(
                    f'/client/cad_model/{cad_model_data["cad_model_name"]}', data=cad_model_update_data, headers=header)
                print(patch_resp)


class CADModelListTest(BaseTest):
    def test_get_cad_model_list(self):
        with self.app() as test_client:
            with self.app_context():
                # Create authorization header
                access_token = create_access_token(identity=1, fresh=True)
                header = {'Authorization': f'Bearer {access_token}'}
                self.assertIsNone(CADModel.find_cad_model_by_id(1))
                # Create and save a client to DB
                sample_client = ClientModel(**client)
                self.assertIsNone(ClientModel.find_client_by_id(1))
                sample_client.save_client_to_db()
                self.assertIsNotNone(ClientModel.find_client_by_id(1))

                post_resp = test_client.post(
                    f'/client/cad_model/{cad_model_data["cad_model_name"]}', data=cad_model_data, headers=header)
                self.assertEqual(post_resp.status_code, 200)
                client_name = client['username']
                get_list_resp = test_client.get(
                    f'/client/{client_name}/cad_model')
                self.assertListEqual(get_list_resp.json['cad_models'], [cad_model_data])
