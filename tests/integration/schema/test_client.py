from marshmallow import ValidationError
from schema.client.client import ClientSchema
from tests.base_test import BaseTest
from models.client.client import ClientModel


class ClientSchemaTest(BaseTest):
    def test_load_and_dump(self):
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
                'first_name': 'jane',
                'last_name': 'doe'
            }
            data = client_schema.load(client_user)
            client = ClientModel(**data)
            client.save_client_to_db()

            loaded_client = ClientModel.find_client_by_email('janedoe@email.com')
            self.assertEqual(client_schema.dump(loaded_client), expected_client)

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
        client_user_less_than_two = {
            'email': 'janedoe@email.com',
            'username': 'x',
            'first_name': 'jane',
            'last_name': 'doe',
            'password': '12345678'
        }
        client_user_more_than_15 = {
            'email': 'janedoe@email.com',
            'username': 'millicent_bystander_flushed_away',
            'first_name': 'jane',
            'last_name': 'doe',
            'password': '12345678'
        }
        # Matching responses
        expected = {'username': ['Username must be between 2 and 15 characters.']}

        # Assertion tests for each category
        try:
            client_schema.load(client_user_empty_username)
        except ValidationError as err:
            self.assertEqual(err.messages, expected)

        try:
            client_schema.load(client_user_less_than_two)
        except ValidationError as err:
            self.assertEqual(err.messages, expected)

        try:
            client_schema.load(client_user_more_than_15)
        except ValidationError as err:
            self.assertEqual(err.messages, expected)

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
        client_user_8 = {
            'email': 'janedoe@email.com',
            'username': 'jane_d',
            'first_name': 'jane',
            'last_name': 'doe',
            'password': '1234567'
        }
        client_user_20 = {
            'email': 'janedoe@email.com',
            'username': 'jane_d',
            'first_name': 'jane',
            'last_name': 'doe',
            'password': '012345678901234567890123456789'
        }
        # Matching responses
        expected = {'password': ['Password must be between 8 and 20 characters.']}
        try:
            client_schema.load(client_user_empty_password)
        except ValidationError as err:
            self.assertEqual(err.messages, expected)

        try:
            client_schema.load(client_user_8)
        except ValidationError as err:
            self.assertEqual(err.messages, expected)

        try:
            client_schema.load(client_user_20)
        except ValidationError as err:
            self.assertEqual(err.messages, expected)

    def test_validate_empty_fields(self):
        client_schema = ClientSchema()
        # Possible bad client user request entries
        client_user_empty = {
            'email': '',
            'username': '',
            'first_name': '',
            'last_name': '',
            'password': ''
        }
        expected_response = {
            'password': ['Password must be between 8 and 20 characters.'],
            'last_name': ['Last name must be between 2 and 20 characters.'],
            'first_name': ['First name must be between 2 and 20 characters.'],
            'email': ['Not a valid email address.', 'Enter a valid email address.'],
            'username': ['Username must be between 2 and 15 characters.']
        }
        try:
            client_schema.load(client_user_empty)
        except ValidationError as err:
            self.assertEqual(err.messages, expected_response)
