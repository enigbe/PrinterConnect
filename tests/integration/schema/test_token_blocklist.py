from tests.base_test import BaseTest
from schema.client.token_blocklist import TokenBlockListSchema
from models.client.token_blocklist import TokenBlockListModel
from tests.test_data import blocked_token

blocked_token_schema = TokenBlockListSchema()


class TokenBlockListSchemaTest(BaseTest):
    def test_load_token_blocklist(self):
        with self.app_context():
            valid_token = blocked_token_schema.load(blocked_token)
            self.assertDictEqual(valid_token, blocked_token)

    def test_dump_token_blocklist(self):
        with self.app_context():
            blocked_token_object = TokenBlockListModel(**blocked_token.copy())
            valid_token = blocked_token_schema.dump(blocked_token_object)
            self.assertDictEqual(valid_token, blocked_token)