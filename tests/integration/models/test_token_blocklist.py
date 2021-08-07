import unittest

from tests.base_test import BaseTest
from models.shared_user.token_blocklist import TokenBlockListModel
from models.client.client import ClientModel
from tests.test_data import blocked_token, client


# @unittest.skip('Skipping TokenBlockList')
class TokenBlockListTest(BaseTest):
    """Test TokenBlockList model"""
    def test_save_token_to_db(self):
        """Test the save_token_to_db() function"""
        with self.app_context():
            # Create and save a client to DB
            sample_client = ClientModel(**client)
            self.assertIsNone(ClientModel.find_user_by_id(client['id']))
            sample_client.save_user_to_db()

            blocked_token_object = TokenBlockListModel(**blocked_token)
            blocked_token_object.save_token_to_db()

            expected_token = TokenBlockListModel.find_tokens_by_client_id(sample_client.id)[0]
            self.assertIsNotNone(expected_token)
            self.assertEqual(expected_token, blocked_token_object)

    def test_delete_token_from_db(self):
        """Test the delete_token_from_db() function"""
        with self.app_context():
            # Create and save a client to DB
            sample_client = ClientModel(**client)
            self.assertIsNone(ClientModel.find_user_by_id(client['id']))
            sample_client.save_user_to_db()
            blocked_token['client_id'] = sample_client.id
            blocked_token_object = TokenBlockListModel(**blocked_token)
            blocked_token_object.save_token_to_db()

            expected_token = TokenBlockListModel.find_tokens_by_client_id(sample_client.id)[0]
            self.assertEqual(expected_token, blocked_token_object)

            expected_token.delete_from_db()
            self.assertEqual(len(TokenBlockListModel.find_tokens_by_client_id(sample_client.id)), 0)

    def test_token_constructor(self):
        """Test token creation"""
        blocked_token_object = TokenBlockListModel(**blocked_token.copy())
        self.assertEqual(str(blocked_token_object),
                         f'<TokenBlockList - id: {blocked_token["id"]} | jti: {blocked_token["jti"]} | client_id: '
                         f'{blocked_token["client_id"]} | '
                         f'business_id: {blocked_token["business_id"]}>')
