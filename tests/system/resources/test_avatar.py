import os
import builtins
from unittest.mock import patch
from flask_jwt_extended import create_access_token
from werkzeug.datastructures import FileStorage

from tests.base_test import BaseTest
from tests.test_data import client
from models.client.client import ClientModel
from resources.client.avatar import upload_helper


class AvatarTest(BaseTest):
    @patch('resources.client.avatar.send_file', autospec=True)
    def test_get_default_avatar_with_jwt(self, mock_send_file):
        with self.app() as test_client:
            with self.app_context():
                new_client = ClientModel(**client.copy())
                new_client.save_client_to_db()

                access_token = create_access_token(identity=new_client.id)
                header = {'Authorization': 'Bearer {}'.format(access_token)}

                mock_send_file.return_value = 'default-avatar.png'
                resp = test_client.get('/client/avatar', headers=header)

                mock_send_file.assert_called_once()
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(resp.json, 'default-avatar.png')

    @patch('resources.client.avatar.send_file', autospec=True)
    @patch.object(upload_helper, 'find_image_any_format', autospec=True)
    @patch.object(upload_helper, 'save_upload', autospec=True)
    @patch.object(builtins, 'open', autospec=True)
    def test_get_uploaded_avatar_with_jwt(self, mock_open, mock_save_image, mock_find_image_any_format, mock_send_file):
        with self.app() as test_client:
            with self.app_context():
                # 1. Upload an image
                new_client = ClientModel(**client.copy())
                new_client.save_client_to_db()

                access_token = create_access_token(identity=new_client.id, fresh=True)
                header = {
                    'Authorization': 'Bearer {}'.format(access_token),
                    'Content-Type': 'multipart/form-data'
                }
                file_pointer = '/home/enigbe/Pictures/james_.jpg'

                mock_open.return_value = FileStorage(filename='james_.jpg')
                mock_save_image.return_value = 'avatars/client_1.jpg'
                mock_find_image_any_format.return_value = None

                data = {'image': (open(file_pointer, 'rb'),)}
                put_response = test_client.put('/client/avatar/upload', data=data, headers=header)

                mock_open.assert_called_once()
                mock_save_image.assert_called_once()
                self.assertEqual(put_response.status_code, 200)
                self.assertEqual(put_response.json, {'msg': "Avatar 'client_1.jpg' uploaded."})

                mock_find_image_any_format.return_value = 'static/images/avatars/client_1.jpg'
                mock_send_file.return_value = 'client_1.jpg'
                get_resp = test_client.get('/client/avatar', headers=header)

                self.assertEqual(get_resp.status_code, 200)
                self.assertEqual(get_resp.json, 'client_1.jpg')
                mock_send_file.assert_called_once()
                mock_find_image_any_format.call_count = 2

    @patch.object(upload_helper, 'save_upload', autospec=True)
    @patch.object(builtins, 'open', autospec=True)
    def test_upload_avatar(self, mock_open, mock_save_image):
        with self.app() as test_client:
            with self.app_context():
                new_client = ClientModel(**client.copy())
                new_client.save_client_to_db()

                access_token = create_access_token(identity=new_client.id, fresh=True)
                header = {
                    'Authorization': 'Bearer {}'.format(access_token),
                    'Content-Type': 'multipart/form-data'
                }
                file_pointer = '/home/enigbe/Pictures/james_.jpg'

                mock_open.return_value = FileStorage(filename='james_.jpg')
                mock_save_image.return_value = 'avatars/client_1.jpg'

                data = {'image': (open(file_pointer, 'rb'),)}
                resp = test_client.put('/client/avatar/upload', data=data, headers=header)

                mock_open.assert_called_once()
                mock_save_image.assert_called_once()
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(resp.json, {'msg': "Avatar 'client_1.jpg' uploaded."})

    @patch.object(os, 'remove', autospec=True)
    @patch.object(upload_helper, 'find_upload_any_format', autospec=True)
    @patch.object(upload_helper, 'save_upload', autospec=True)
    @patch.object(builtins, 'open', autospec=True)
    def test_delete_avatar(self, mock_open, mock_save_image, mock_find_image_any_format, mock_remove):
        with self.app() as test_client:
            with self.app_context():
                # 1. Upload an avatar (assert that it was uploaded)
                new_client = ClientModel(**client.copy())
                new_client.save_client_to_db()

                access_token = create_access_token(identity=new_client.id, fresh=True)
                header = {
                    'Authorization': 'Bearer {}'.format(access_token),
                    'Content-Type': 'multipart/form-data'
                }
                file_pointer = '/home/enigbe/Pictures/james_.jpg'

                mock_open.return_value = FileStorage(filename='james_.jpg')
                mock_save_image.return_value = 'avatars/client_1.jpg'
                mock_find_image_any_format.return_value = None

                data = {'image': (open(file_pointer, 'rb'),)}
                resp = test_client.put('/client/avatar/upload', data=data, headers=header)

                self.assertIsNotNone(new_client.avatar_filename)
                self.assertEqual(resp.json, {'msg': "Avatar 'client_1.jpg' uploaded."})

                # 2. Delete uploaded avatar (assert avatar is None)
                mock_find_image_any_format.return_value = 'static/images/avatars/client_1'
                mock_remove.side_effect = self.delete_avatar
                resp = test_client.delete('/client/avatar', headers=header)

                mock_open.assert_called_once()
                mock_save_image.assert_called_once()
                mock_find_image_any_format.call_count = 2
                mock_remove.assert_called_with('static/images/avatars/client_1')
                mock_remove.assert_called_once()
                self.assertIsNone(new_client.avatar_filename)
                self.assertEqual(resp.status_code, 200)

    @staticmethod
    def delete_avatar(avatar):
        """Side effect helper function for os.remove(avatar)"""
        avatar = None
        return avatar
