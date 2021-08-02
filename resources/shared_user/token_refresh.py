from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from libs.strings import gettext
from libs.user_helper import blocked_tokens
from models.client.client import ClientModel
from schema.client.client import ClientSchema
from models.business.business import BusinessModel
from schema.business.business import BusinessSchema
from models.shared_user.token_blocklist import TokenBlockListModel
from schema.client.token_blocklist import TokenBlockListSchema

blocked_token_schema = TokenBlockListSchema(many=True)
client_schema = ClientSchema(only=('email',))
business_schema = BusinessSchema(only=('email',))


class TokenRefresh(Resource):
    """Refresh access JWT for endpoints that require a token refreshing"""
    @classmethod
    @jwt_required(refresh=True)
    def post(cls):
        identity = get_jwt_identity()
        new_access_token = create_access_token(identity=identity, fresh=False)
        return {'access_token': new_access_token}, 200


class BlockedTokens(Resource):
    @classmethod
    def post(cls, user_type):
        """
        View all the tokens blocked by a user by developer
        :return: List of blocked tokens
        """
        user_schema = client_schema if user_type == 'client' else business_schema
        email_dict = user_schema.load(request.get_json())  # {"email": "email@inc.com"}

        return blocked_tokens(user_type, email_dict['email'], blocked_token_schema)
