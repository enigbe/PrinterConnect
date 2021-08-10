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

                # Create and save a client to DB
                sample_client = ClientModel(**client)
                self.assertIsNone(ClientModel.find_user_by_id(sample_client.id))
                sample_client.save_user_to_db()
                self.assertIsNotNone(ClientModel.find_user_by_id(sample_client.id))

                # Create authorization header
                access_token = create_access_token(identity=sample_client.id, fresh=True)
                header = {'Authorization': f'Bearer {access_token}'}

                self.assertIsNone(CADModel.find_cad_model_by_name(cad_model_data['cad_model_name']))
                resp = test_client.post(
                    f'/client/{client["username"]}/cad_model/{cad_model_data["cad_model_name"]}', data=cad_model_data,
                    headers=header)
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
                # Create and save a client to DB
                sample_client = ClientModel(**client)
                self.assertIsNone(ClientModel.find_user_by_id(sample_client.id))
                sample_client.save_user_to_db()
                self.assertIsNotNone(ClientModel.find_user_by_id(sample_client.id))

                # Create authorization header
                access_token = create_access_token(identity=sample_client.id, fresh=True)
                header = {'Authorization': f'Bearer {access_token}'}

                post_resp = test_client.post(
                    f'/client/{client["username"]}/cad_model/{cad_model_data["cad_model_name"]}',
                    data=cad_model_data, headers=header)
                self.assertEqual(post_resp.status_code, 200)
                get_resp = test_client.get(
                    f'/client/{client["username"]}/cad_model/{cad_model_data["cad_model_name"]}', headers=header)
                self.assertEqual(get_resp.status_code, 200)

    @patch.object(s3_client, 'delete_object', autospec=True)
    def test_delete_cad_model(self, mock_delete_object):
        with self.app() as test_client:
            with self.app_context():
                # Create and save a client to DB
                sample_client = ClientModel(**client)
                self.assertIsNone(ClientModel.find_user_by_id(sample_client.id))
                sample_client.save_user_to_db()
                self.assertIsNotNone(ClientModel.find_user_by_id(sample_client.id))

                # Create authorization header
                access_token = create_access_token(identity=sample_client.id, fresh=True)
                header = {'Authorization': f'Bearer {access_token}'}

                post_resp = test_client.post(
                    f'/client/{client["username"]}/cad_model/{cad_model_data["cad_model_name"]}',
                    data=cad_model_data, headers=header)
                self.assertEqual(post_resp.status_code, 200)
                # Delete CAD model
                mock_delete_object.return_value = {
                    'ResponseMetadata': {
                        'HTTPStatusCode': 204
                    }
                }
                delete_resp = test_client.delete(
                    f'/client/{client["username"]}/cad_model/{cad_model_data["cad_model_name"]}', headers=header)
                mock_delete_object.assert_called_once()
                self.assertEqual(delete_resp.status_code, 200)

    def test_update_cad_model(self):
        with self.app() as test_client:
            with self.app_context():

                # Create and save a client to DB
                sample_client = ClientModel(**client)
                self.assertIsNone(ClientModel.find_user_by_id(sample_client.id))
                sample_client.save_user_to_db()
                self.assertIsNotNone(ClientModel.find_user_by_id(sample_client.id))

                # Create authorization header
                access_token = create_access_token(identity=sample_client.id, fresh=True)
                header = {'Authorization': f'Bearer {access_token}'}

                self.assertIsNone(CADModel.find_cad_model_by_name(cad_model_data['cad_model_name']))
                post_resp = test_client.post(
                    f'/client/{client["username"]}/cad_model/{cad_model_data["cad_model_name"]}',
                    data=cad_model_data, headers=header)
                self.assertEqual(post_resp.status_code, 200)
                patch_resp = test_client.patch(
                    f'/client/{client["username"]}/cad_model/{cad_model_data["cad_model_name"]}',
                    data=cad_model_update_data,
                    headers=header
                )
                self.assertEqual(patch_resp.status_code, 200)
                self.assertIn('url', patch_resp.json)
                self.assertIn('fields', patch_resp.json)
                self.assertIn('key', patch_resp.json['fields'])
                self.assertIn('policy', patch_resp.json['fields'])
                self.assertIn('signature', patch_resp.json['fields'])
                self.assertIn('AWSAccessKeyId', patch_resp.json['fields'])


class CADModelListTest(BaseTest):
    def test_get_cad_model_list(self):
        with self.app() as test_client:
            with self.app_context():

                # Create and save a client to DB
                sample_client = ClientModel(**client)
                self.assertIsNone(ClientModel.find_user_by_id(sample_client.id))
                sample_client.save_user_to_db()
                self.assertIsNotNone(ClientModel.find_user_by_id(sample_client.id))

                # Create authorization header
                access_token = create_access_token(identity=sample_client.id, fresh=True)
                header = {'Authorization': f'Bearer {access_token}'}

                self.assertIsNone(CADModel.find_cad_model_by_name(cad_model_data['cad_model_name']))
                post_resp = test_client.post(
                    f'/client/{sample_client.username}/cad_model/{cad_model_data["cad_model_name"]}',
                    data=cad_model_data,
                    headers=header
                )
                self.assertEqual(post_resp.status_code, 200)
                client_name = client['username']
                get_list_resp = test_client.get(
                    f'/client/{client_name}/cad_models')
                self.assertListEqual(get_list_resp.json['cad_models'], [cad_model_data])
