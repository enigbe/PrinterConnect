from marshmallow import ValidationError
from schema.client.client import ClientSchema
from tests.base_test import BaseTest
from models.client.client import ClientModel


class ClientSchemaTest(BaseTest):
    def test_load_and_dump_only(self):
        with self.app_context():
            client_schema = ClientSchema()

            client_user = {
                'email': 'janedoe@email.com',
                'username': 'jane_d',
                'first_name': 'jane',
                'last_name': 'doe',
                'password': '12345678'
            }
            expected_client = {
                'id': 1,
                'email': 'janedoe@email.com',
                'username': 'jane_d',
                'first_name': 'Jane',
                'last_name': 'Doe'
            }
            client_schema.load(client_user).save_client_to_db()
            loaded_client = ClientModel.find_client_by_email(client_user['email'])

            self.assertDictEqual(expected_client, client_schema.dump(loaded_client))

    def test_validate_username_field(self):
        client_schema = ClientSchema()
        # Possible bad client user request entries
        client_user_empty_username = {
            'email': 'janedoe@email.com',
            'username': '',
            'first_name': 'jane',
            'last_name': 'doe',
            'password': '12345678'
        }
        client_user_less_than_three = {
            'email': 'janedoe@email.com',
            'username': 'xu',
            'first_name': 'jane',
            'last_name': 'doe',
            'password': '12345678'
        }
        client_user_more_than_ten = {
            'email': 'janedoe@email.com',
            'username': 'millicent_bystander',
            'first_name': 'jane',
            'last_name': 'doe',
            'password': '12345678'
        }
        # Matching responses
        expected_empty = {
            '_schema': [
                'One (or more) field(s) is (are) empty.',
                'Username must have between 3 and 10 characters.'
            ]
        }
        expected_otherwise = {
            '_schema': [
                'Username must have between 3 and 10 characters.'
            ]
        }

        # Assertion tests for each category
        try:
            client_schema.load(client_user_empty_username)
        except ValidationError as err:
            self.assertEqual(err.messages, expected_empty)

        try:
            client_schema.load(client_user_less_than_three)
        except ValidationError as err:
            self.assertEqual(err.messages, expected_otherwise)

        try:
            client_schema.load(client_user_more_than_ten)
        except ValidationError as err:
            self.assertEqual(err.messages, expected_otherwise)

    def test_validate_password_field(self):
        client_schema = ClientSchema()
        # Possible bad client user request entries
        client_user_empty_password = {
            'email': 'janedoe@email.com',
            'username': 'jane_d',
            'first_name': 'jane',
            'last_name': 'doe',
            'password': ''
        }
        client_user_8= {
            'email': 'janedoe@email.com',
            'username': 'jane_d',
            'first_name': 'jane',
            'last_name': 'doe',
            'password': '1234567'
        }
        client_user_25 = {
            'email': 'janedoe@email.com',
            'username': 'jane_d',
            'first_name': 'jane',
            'last_name': 'doe',
            'password': '01234567890123456789012345'
        }
        # Matching responses
        expected_empty = {
            '_schema': [
                'One (or more) field(s) is (are) empty.',
                'Password must be between 8 and 25 characters long.'
            ]
        }
        expected_otherwise = {
            '_schema': [
                'Password must be between 8 and 25 characters long.'
            ]
        }
        try:
            client_schema.load(client_user_empty_password)
        except ValidationError as err:
            self.assertEqual(err.messages, expected_empty)

        try:
            client_schema.load(client_user_8)
        except ValidationError as err:
            self.assertEqual(err.messages, expected_otherwise)

        try:
            client_schema.load(client_user_25)
        except ValidationError as err:
            self.assertEqual(err.messages, expected_otherwise)

    def test_validate_empty_fields(self):
        client_schema = ClientSchema()
        # Possible bad client user request entries
        client_user_empty= {
            'email': '',
            'username': '',
            'first_name': '',
            'last_name': '',
            'password': ''
        }
        expected_response = {
            '_schema': [
                'Please enter a valid email address.',
                'One (or more) field(s) is (are) empty.',
                'Password must be between 8 and 25 characters long.',
                'Username must have between 3 and 10 characters.'
            ]
        }
        try:
            client_schema.load(client_user_empty)
        except ValidationError as err:
            self.assertEqual(err.messages, expected_response)
