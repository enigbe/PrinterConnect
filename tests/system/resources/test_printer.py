from unittest.mock import patch
from requests import Response

from models.business.business import BusinessModel
from models.business.printer import PrinterModel

from tests.base_test import BaseTest
from tests.test_data import business_data, printer_data, printer_update_data


class PrinterTest(BaseTest):
    @patch.object(BusinessModel, 'send_verification_email')
    def test_create_printer(self, mock_send_verification_email):
        with self.app() as test_client, self.app_context():
            # 1. Create new business account
            mock_send_verification_email.return_value = Response()
            signup_resp = test_client.post('/business/signup/email', json=business_data)
            mock_send_verification_email.assert_called_once()
            self.assertEqual(signup_resp.status_code, 201)
            expected_resp = {'msg': 'Client account created successfully. Check your email to activate your account'}
            self.assertEqual(signup_resp.json, expected_resp)
            # 2. Confirm created account
            business_account = BusinessModel.find_user_by_email(business_data['email'])
            business_confirmation = business_account.most_recent_confirmation.id
            confirmation_resp = test_client.get(f'/business/confirmation/{business_confirmation}')
            self.assertEqual(confirmation_resp.status_code, 200)
            expected_conf_resp = {'msg': f'{business_data["email"]} activated successfully. You can now sign in.'}
            self.assertEqual(confirmation_resp.json, expected_conf_resp)
            # 3. Sign in to account
            signin_data = {'email': business_data['email'], 'password': business_data['password']}
            signin_resp = test_client.post('/business/signin/email', json=signin_data)
            self.assertIn('access_token', signin_resp.json)
            self.assertIn('refresh_token', signin_resp.json)
            self.assertEqual(signin_resp.json['msg'], 'Sign in successful.')
            # 4. Create new printer
            self.assertIsNone(PrinterModel.find_printer_by_name(printer_data['name']))
            access_token = signin_resp.json['access_token']
            header = {'Authorization': f'Bearer {access_token}'}
            printer_resp = test_client.post(f'/business/{business_data["username"]}/printer/{printer_data["name"]}',
                                            json=printer_data,
                                            headers=header)
            self.assertEqual(printer_resp.status_code, 201)
            self.assertIsNotNone(PrinterModel.find_printer_by_name(printer_data['name']))
            expected_printer_resp = {'msg': 'Printer successfully created'}
            self.assertEqual(printer_resp.json, expected_printer_resp)

    @patch.object(BusinessModel, 'send_verification_email')
    def test_printer_already_exist(self, mock_send_verification_email):
        with self.app() as test_client, self.app_context():
            # 1. Create new business account
            mock_send_verification_email.return_value = Response()
            signup_resp = test_client.post('/business/signup/email', json=business_data)
            # 2. Confirm created account
            business_account = BusinessModel.find_user_by_email(business_data['email'])
            business_confirmation = business_account.most_recent_confirmation.id
            confirmation_resp = test_client.get(f'/business/confirmation/{business_confirmation}')
            # 3. Sign in to account
            signin_data = {'email': business_data['email'], 'password': business_data['password']}
            signin_resp = test_client.post('/business/signin/email', json=signin_data)
            # 4. Create new printer
            access_token = signin_resp.json['access_token']
            header = {'Authorization': f'Bearer {access_token}'}
            # Create first printer
            test_client.post(
                f'/business/{business_data["username"]}/printer/{printer_data["name"]}',
                json=printer_data,
                headers=header
            )
            # Attempt to create same printer
            sp_resp = test_client.post(
                f'/business/{business_data["username"]}/printer/{printer_data["name"]}',
                json=printer_data,
                headers=header
            )
            printer_exist = {'msg': f"Printer with name '{printer_data['name']}' already exists on your account"}
            self.assertEqual(sp_resp.json, printer_exist)
            self.assertEqual(sp_resp.status_code, 400)

    @patch.object(BusinessModel, 'send_verification_email')
    def test_read_printer(self, mock_send_verification_email):
        with self.app() as test_client, self.app_context():
            # 1. Create new business account
            mock_send_verification_email.return_value = Response()
            signup_resp = test_client.post('/business/signup/email', json=business_data)
            mock_send_verification_email.assert_called_once()
            self.assertEqual(signup_resp.status_code, 201)
            expected_resp = {'msg': 'Client account created successfully. Check your email to activate your account'}
            self.assertEqual(signup_resp.json, expected_resp)
            # 2. Confirm created account
            business_account = BusinessModel.find_user_by_email(business_data['email'])
            business_confirmation = business_account.most_recent_confirmation.id
            confirmation_resp = test_client.get(f'/business/confirmation/{business_confirmation}')
            self.assertEqual(confirmation_resp.status_code, 200)
            expected_conf_resp = {'msg': f'{business_data["email"]} activated successfully. You can now sign in.'}
            self.assertEqual(confirmation_resp.json, expected_conf_resp)
            # 3. Sign in to account
            signin_data = {'email': business_data['email'], 'password': business_data['password']}
            signin_resp = test_client.post('/business/signin/email', json=signin_data)
            self.assertIn('access_token', signin_resp.json)
            self.assertIn('refresh_token', signin_resp.json)
            self.assertEqual(signin_resp.json['msg'], 'Sign in successful.')
            # 4. Create new printer
            self.assertIsNone(PrinterModel.find_printer_by_name(printer_data['name']))
            access_token = signin_resp.json['access_token']
            header = {'Authorization': f'Bearer {access_token}'}
            post_printer_resp = test_client.post(
                f'/business/{business_data["username"]}/printer/{printer_data["name"]}',
                json=printer_data,
                headers=header
            )
            self.assertEqual(post_printer_resp.status_code, 201)
            self.assertIsNotNone(PrinterModel.find_printer_by_name(printer_data['name']))
            expected_printer_resp = {'msg': 'Printer successfully created'}
            self.assertEqual(post_printer_resp.json, expected_printer_resp)
            # 5. Read created printer
            get_printer_resp = test_client.get(f'/business/{business_data["username"]}/printer/{printer_data["name"]}')
            self.assertEqual(get_printer_resp.status_code, 200)
            self.assertEqual(get_printer_resp.json['printer']['name'], printer_data['name'])
            self.assertEqual(get_printer_resp.json['printer']['material'], printer_data['material'])
            self.assertEqual(get_printer_resp.json['printer']['file_type'], printer_data['file_type'])
            self.assertEqual(get_printer_resp.json['printer']['height'], printer_data['height'])
            self.assertEqual(get_printer_resp.json['printer']['base_width'], printer_data['base_width'])
            self.assertEqual(get_printer_resp.json['printer']['base_length'], printer_data['base_length'])
            self.assertEqual(get_printer_resp.json['printer']['model'], printer_data['model'])

    @patch.object(BusinessModel, 'send_verification_email')
    def test_update_printer(self, mock_send_verification_email):
        with self.app() as test_client, self.app_context():
            # 1. Create new business account
            mock_send_verification_email.return_value = Response()
            signup_resp = test_client.post('/business/signup/email', json=business_data)
            mock_send_verification_email.assert_called_once()
            self.assertEqual(signup_resp.status_code, 201)
            expected_resp = {'msg': 'Client account created successfully. Check your email to activate your account'}
            self.assertEqual(signup_resp.json, expected_resp)
            # 2. Confirm created account
            business_account = BusinessModel.find_user_by_email(business_data['email'])
            business_confirmation = business_account.most_recent_confirmation.id
            confirmation_resp = test_client.get(f'/business/confirmation/{business_confirmation}')
            self.assertEqual(confirmation_resp.status_code, 200)
            expected_conf_resp = {'msg': f'{business_data["email"]} activated successfully. You can now sign in.'}
            self.assertEqual(confirmation_resp.json, expected_conf_resp)
            # 3. Sign in to account
            signin_data = {'email': business_data['email'], 'password': business_data['password']}
            signin_resp = test_client.post('/business/signin/email', json=signin_data)
            self.assertIn('access_token', signin_resp.json)
            self.assertIn('refresh_token', signin_resp.json)
            self.assertEqual(signin_resp.json['msg'], 'Sign in successful.')
            # 4. Create new printer
            self.assertIsNone(PrinterModel.find_printer_by_name(printer_data['name']))
            access_token = signin_resp.json['access_token']
            header = {'Authorization': f'Bearer {access_token}'}
            post_printer_resp = test_client.post(
                f'/business/{business_data["username"]}/printer/{printer_data["name"]}',
                json=printer_data,
                headers=header
            )
            self.assertEqual(post_printer_resp.status_code, 201)
            self.assertIsNotNone(PrinterModel.find_printer_by_name(printer_data['name']))
            expected_printer_resp = {'msg': 'Printer successfully created'}
            self.assertEqual(post_printer_resp.json, expected_printer_resp)
            # 5. Update created printer
            update_data = printer_update_data
            self.assertIsNone(PrinterModel.find_printer_by_name(update_data['name']))
            put_printer_resp = test_client.put(
                f'/business/{business_data["username"]}/printer/{printer_data["name"]}',
                json=update_data,
                headers=header
            )
            self.assertEqual(put_printer_resp.status_code, 200)
            self.assertEqual(put_printer_resp.json, {'msg': 'Printer update successful'})
            self.assertIsNotNone(PrinterModel.find_printer_by_name(update_data['name']))

    @patch.object(BusinessModel, 'send_verification_email')
    def test_delete_printer(self, mock_send_verification_email):
        with self.app() as test_client, self.app_context():
            # 1. Create new business account
            mock_send_verification_email.return_value = Response()
            signup_resp = test_client.post('/business/signup/email', json=business_data)
            mock_send_verification_email.assert_called_once()
            self.assertEqual(signup_resp.status_code, 201)
            expected_resp = {'msg': 'Client account created successfully. Check your email to activate your account'}
            self.assertEqual(signup_resp.json, expected_resp)
            # 2. Confirm created account
            business_account = BusinessModel.find_user_by_email(business_data['email'])
            business_confirmation = business_account.most_recent_confirmation.id
            confirmation_resp = test_client.get(f'/business/confirmation/{business_confirmation}')
            self.assertEqual(confirmation_resp.status_code, 200)
            expected_conf_resp = {'msg': f'{business_data["email"]} activated successfully. You can now sign in.'}
            self.assertEqual(confirmation_resp.json, expected_conf_resp)
            # 3. Sign in to account
            signin_data = {'email': business_data['email'], 'password': business_data['password']}
            signin_resp = test_client.post('/business/signin/email', json=signin_data)
            self.assertIn('access_token', signin_resp.json)
            self.assertIn('refresh_token', signin_resp.json)
            self.assertEqual(signin_resp.json['msg'], 'Sign in successful.')
            # 4. Create new printer
            self.assertIsNone(PrinterModel.find_printer_by_name(printer_data['name']))
            access_token = signin_resp.json['access_token']
            header = {'Authorization': f'Bearer {access_token}'}
            post_printer_resp = test_client.post(
                f'/business/{business_data["username"]}/printer/{printer_data["name"]}',
                json=printer_data,
                headers=header
            )
            self.assertEqual(post_printer_resp.status_code, 201)
            self.assertIsNotNone(PrinterModel.find_printer_by_name(printer_data['name']))
            expected_printer_resp = {'msg': 'Printer successfully created'}
            self.assertEqual(post_printer_resp.json, expected_printer_resp)
            # 5. Delete created printer
            delete_printer_resp = test_client.delete(
                f'/business/{business_data["username"]}/printer/{printer_data["name"]}',
                headers=header
            )
            self.assertIsNone(PrinterModel.find_printer_by_name(printer_data['name']))
            self.assertEqual(delete_printer_resp.json, {'msg': 'Printer successfully deleted'})
            self.assertEqual(delete_printer_resp.status_code, 200)

    @patch.object(BusinessModel, 'send_verification_email')
    def test_read_saved_printers(self, mock_send_verification_email):
        with self.app() as test_client, self.app_context():
            # 1. Create new business account
            mock_send_verification_email.return_value = Response()
            signup_resp = test_client.post('/business/signup/email', json=business_data)
            mock_send_verification_email.assert_called_once()
            self.assertEqual(signup_resp.status_code, 201)
            expected_resp = {'msg': 'Client account created successfully. Check your email to activate your account'}
            self.assertEqual(signup_resp.json, expected_resp)
            # 2. Confirm created account
            business_account = BusinessModel.find_user_by_email(business_data['email'])
            business_confirmation = business_account.most_recent_confirmation.id
            confirmation_resp = test_client.get(f'/business/confirmation/{business_confirmation}')
            self.assertEqual(confirmation_resp.status_code, 200)
            expected_conf_resp = {'msg': f'{business_data["email"]} activated successfully. You can now sign in.'}
            self.assertEqual(confirmation_resp.json, expected_conf_resp)
            # 3. Sign in to account
            signin_data = {'email': business_data['email'], 'password': business_data['password']}
            signin_resp = test_client.post('/business/signin/email', json=signin_data)
            self.assertIn('access_token', signin_resp.json)
            self.assertIn('refresh_token', signin_resp.json)
            self.assertEqual(signin_resp.json['msg'], 'Sign in successful.')
            # 4. Create new printer
            self.assertIsNone(PrinterModel.find_printer_by_name(printer_data['name']))
            access_token = signin_resp.json['access_token']
            header = {'Authorization': f'Bearer {access_token}'}
            post_printer_resp = test_client.post(
                f'/business/{business_data["username"]}/printer/{printer_data["name"]}',
                json=printer_data,
                headers=header
            )
            self.assertEqual(post_printer_resp.status_code, 201)
            self.assertIsNotNone(PrinterModel.find_printer_by_name(printer_data['name']))
            expected_printer_resp = {'msg': 'Printer successfully created'}
            self.assertEqual(post_printer_resp.json, expected_printer_resp)
            # 5. Read all printers
            all_printers = test_client.get(f'/business/{business_data["username"]}/printers')
            self.assertEqual(all_printers.status_code, 200)
            self.assertIn('printers', all_printers.json)
