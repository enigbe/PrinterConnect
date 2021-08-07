import unittest
from marshmallow import ValidationError

from schema.client.client import ClientSchema
from tests.base_test import BaseTest
from models.client.client import ClientModel
from models.shared_user.confirmation import ConfirmationModel
from tests.test_data import client, exp_client


# @unittest.skip("Skipping ClientSchemaTest")
class ClientSchemaTest(BaseTest):
    def test_load_and_dump(self):
        with self.app_context():
            client_schema = ClientSchema()
            data = client_schema.load(client.copy())

            # Test Client
            sample_client = ClientModel(**data)
            sample_client.save_user_to_db()

            confirmation = ConfirmationModel(sample_client)
            confirmation.save_to_db()

            loaded_client = ClientModel.find_user_by_email(sample_client.email)

            # Assertion
            dumped_client = client_schema.dump(loaded_client)
            self.assertEqual(dumped_client['first_name'], client['first_name'])
            self.assertEqual(dumped_client['last_name'], client['last_name'])
            self.assertEqual(dumped_client['email'], client['email'])
            self.assertEqual(dumped_client['username'], client['username'])

    def test_validate_username_field(self):
        client_schema = ClientSchema()
        # Matching responses
        expected = {'username': ['Username must be between 2 and 15 characters.']}

        # Assertion tests for each category
        try:
            # Client with empty username
            sample_client = client.copy()
            sample_client['username'] = ''
            client_schema.load(sample_client)
        except ValidationError as err:
            self.assertEqual(err.messages, expected)

        try:
            # Client with username with < 2 characters
            sample_client = client.copy()
            sample_client['username'] = 'x'
            client_schema.load(sample_client)
        except ValidationError as err:
            self.assertEqual(err.messages, expected)

        try:
            # Client with username with > 15 characters
            sample_client = client.copy()
            sample_client['username'] = 'millicent_bystander_flushed_away'
            client_schema.load(sample_client)
        except ValidationError as err:
            self.assertEqual(err.messages, expected)

    def test_validate_password_field(self):
        client_schema = ClientSchema()
        # Expected response
        expected = {'password': ['Password must be between 8 and 20 characters.']}
        try:
            # Client user with empty password
            sample_client = client.copy()
            sample_client['password'] = ''
            client_schema.load(sample_client)
        except ValidationError as err:
            self.assertEqual(err.messages, expected)

        try:
            # Client user with password < 8 characters
            sample_client = client.copy()
            sample_client['password'] = '1234567'
            client_schema.load(sample_client)
        except ValidationError as err:
            self.assertEqual(err.messages, expected)

        try:
            # Client user with password > 20 characters
            sample_client = client.copy()
            sample_client['password'] = '012345678901234567890123456789'
            client_schema.load(sample_client)
        except ValidationError as err:
            self.assertEqual(err.messages, expected)

    def test_validate_empty_fields(self):
        client_schema = ClientSchema()
        first_name_response = {'first_name': ['First name must be between 2 and 20 characters.']}
        last_name_response = {'last_name': ['Last name must be between 2 and 20 characters.']}

        try:
            # First name empty
            sample_client = client.copy()
            sample_client['first_name'] = ''
            client_schema.load(sample_client)
        except ValidationError as err:
            self.assertEqual(err.messages, first_name_response)

        try:
            # Last name empty
            sample_client = client.copy()
            sample_client['last_name'] = ''
            client_schema.load(sample_client)
        except ValidationError as err:
            self.assertEqual(err.messages, last_name_response)
