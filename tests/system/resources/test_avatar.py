import requests
from flask_jwt_extended import create_access_token

from tests.base_test import BaseTest
from tests.test_data import client
from models.client.client import ClientModel


class AvatarTest(BaseTest):
    def test_upload_and_get_avatar_with_jwt(self):
        with self.app() as test_client:
            with self.app_context():
                # Create new client and save to DB
                new_client = ClientModel(**client)
                new_client.save_user_to_db()
                # Get access token for new client user
                access_token = create_access_token(identity=new_client.id, fresh=True)
                header = {'Authorization': 'Bearer {}'.format(access_token)}
                # Send a PUT request for image upload URL
                upload_resp = test_client.put('/client/avatar', headers=header)
                self.assertIn('url', upload_resp.json)
                self.assertIn('fields', upload_resp.json)
                self.assertIn('key', upload_resp.json['fields'])
                self.assertIn('policy', upload_resp.json['fields'])
                self.assertIn('signature', upload_resp.json['fields'])
                self.assertIn('AWSAccessKeyId', upload_resp.json['fields'])
                self.assertIsNone(new_client.avatar_filename)
                # Upload to URL
                aws_url = upload_resp.json['url']
                test_avatar = '/home/enigbe/Pictures/james.jpg'
                object_name = upload_resp.json['fields']['key']

                with open(test_avatar, 'rb') as read_img:
                    aws_resp = requests.post(
                        aws_url,
                        data=upload_resp.json['fields'],
                        files={'file': (object_name, read_img)}
                    )

                json_data = {"status_code": aws_resp.status_code, "obj_key": object_name}
                post_resp = test_client.post(
                    f'/client/post_avatar',
                    headers=header,
                    json=json_data
                )
                self.assertEqual(post_resp.json, {'msg': 'Avatar uploaded successfully'})
                # Send a GET request to retrieve avatar filename
                get_resp = test_client.get('/client/avatar', headers=header)
                self.assertEqual(get_resp.status_code, 200)
                self.assertIn('msg', get_resp.json)

    def test_delete_avatar(self):
        with self.app() as test_client:
            with self.app_context():
                # Create new client and save to DB
                new_client = ClientModel(**client)
                new_client.save_user_to_db()
                # Get access token for new client user
                access_token = create_access_token(identity=new_client.id, fresh=True)
                header = {'Authorization': 'Bearer {}'.format(access_token)}
                # Send a PUT request for image upload URL
                upload_resp = test_client.put('/client/avatar', headers=header)
                self.assertIn('url', upload_resp.json)
                self.assertIn('fields', upload_resp.json)
                self.assertIn('key', upload_resp.json['fields'])
                self.assertIn('policy', upload_resp.json['fields'])
                self.assertIn('signature', upload_resp.json['fields'])
                self.assertIn('AWSAccessKeyId', upload_resp.json['fields'])
                self.assertIsNone(new_client.avatar_filename)
                # Upload to URL
                aws_url = upload_resp.json['url']
                test_avatar = '/home/enigbe/Pictures/james.jpg'
                object_name = upload_resp.json['fields']['key']

                with open(test_avatar, 'rb') as read_img:
                    aws_resp = requests.post(
                        aws_url,
                        data=upload_resp.json['fields'],
                        files={'file': (object_name, read_img)}
                    )

                json_data = {"status_code": aws_resp.status_code, "obj_key": object_name}
                post_resp = test_client.post(
                    f'/client/post_avatar',
                    headers=header,
                    json=json_data
                )
                self.assertEqual(post_resp.json, {'msg': 'Avatar uploaded successfully'})
                # Send a GET request to retrieve avatar filename
                get_resp = test_client.get('/client/avatar', headers=header)
                self.assertEqual(get_resp.status_code, 200)
                self.assertIn('msg', get_resp.json)

                # Delete uploaded avatar
                delete_resp = test_client.delete('/client/avatar', headers=header)
                self.assertEqual(delete_resp.json, {'msg': 'Avatar deleted successfully.'})
                self.assertIsNone(new_client.avatar_filename)
