from unittest.mock import patch
from requests import Response
from flask_jwt_extended import create_access_token

from tests.base_test import BaseTest
from tests.test_data import business_data
from models.business.business import BusinessModel


class BusinessProfileTest(BaseTest):
    @patch.object(BusinessModel, 'send_verification_email')
    def test_read_business_profile_no_jwt(self, mock_send_verification_email):
        with self.app() as test_client, self.app_context():
            # 1. Create new business account
            mock_send_verification_email.return_value = Response()
            resp = test_client.post('/business/signup/email', json=business_data)
            self.assertEqual(resp.status_code, 201)
            mock_send_verification_email.assert_called_once()
            expected_resp = {'msg': 'Client account created successfully. Check your email to activate your account'}
            self.assertEqual(resp.json, expected_resp)
            # 2. Read business profile
            read_resp = test_client.get(f'/business/{business_data["username"]}/profile')
            self.assertEqual(read_resp.status_code, 200)
            self.assertEqual(read_resp.json['business']['business_name'], business_data['business_name'])
            self.assertEqual(read_resp.json['business']['bio'], business_data['bio'])
            self.assertEqual(read_resp.json['business']['username'], business_data['username'])

    @patch.object(BusinessModel, 'send_verification_email')
    def test_read_business_profile_with_jwt(self, mock_send_verification_email):
        with self.app() as test_client, self.app_context():
            # 1. Create new business account
            mock_send_verification_email.return_value = Response()
            resp = test_client.post('/business/signup/email', json=business_data)
            self.assertEqual(resp.status_code, 201)
            mock_send_verification_email.assert_called_once()
            expected_resp = {'msg': 'Client account created successfully. Check your email to activate your account'}
            self.assertEqual(resp.json, expected_resp)
            # 2. Read business profile
            access_token = create_access_token(identity=business_data['id'], fresh=True)
            header = {'Authorization': f'Bearer {access_token}'}
            read_resp = test_client.get(f'/business/{business_data["username"]}/profile', headers=header)
            self.assertEqual(read_resp.status_code, 200)
            self.assertEqual(read_resp.json['business']['business_name'], business_data['business_name'])
            self.assertEqual(read_resp.json['business']['bio'], business_data['bio'])
            self.assertEqual(read_resp.json['business']['username'], business_data['username'])
            self.assertEqual(read_resp.json['business']['email'], business_data['email'])
            self.assertIn('creation_date', read_resp.json['business'])

    def test_update_business_profile(self):
        pass

    @patch.object(BusinessModel, 'send_verification_email')
    def test_delete_business_profile(self, mock_send_verification_email):
        with self.app() as test_client, self.app_context():
            # 1. Create new business account
            mock_send_verification_email.return_value = Response()
            resp = test_client.post('/business/signup/email', json=business_data)
            self.assertEqual(resp.status_code, 201)
            mock_send_verification_email.assert_called_once()
            expected_resp = {'msg': 'Client account created successfully. Check your email to activate your account'}
            self.assertEqual(resp.json, expected_resp)
            # 2. Assert business account exist
            self.assertIsNotNone(BusinessModel.find_user_by_username(business_data['username']))
            # 3. Delete business account, assert it does not exists
            access_token = create_access_token(identity=business_data['id'], fresh=True)
            header = {'Authorization': f'Bearer {access_token}'}
            delete_resp = test_client.delete(f'/business/{business_data["username"]}/profile', headers=header)
            self.assertIsNone(BusinessModel.find_user_by_username(business_data['username']))
            self.assertEqual(delete_resp.json, {'msg': f'User \'{business_data["username"]}\' successfully deleted.'})
