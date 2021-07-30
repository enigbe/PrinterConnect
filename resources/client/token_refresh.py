from flask_restful import Resource
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from libs.strings import gettext
from models.client.client import ClientModel
from models.token_blocklist import TokenBlockListModel
from schema.client.token_blocklist import TokenBlockListSchema

blocked_token_schema = TokenBlockListSchema(many=True)


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
    def get(cls, email):
        """
        View all the tokens blocked by a client
        :return: List of blocked tokens
        """
        client = ClientModel.find_client_by_email(email)
        if client is None:
            return {'msg': gettext('client_profile_client_does_not_exist')}, 400
        blocked_tokens_jti = [
            token
            for token in TokenBlockListModel.find_tokens_by_id(client.id)
        ]

        if len(blocked_tokens_jti) == 0:
            return {'msg': gettext('token_refresh_token_blocklist_empty')}, 200
        return {'msg': blocked_token_schema.dump(blocked_tokens_jti)}, 200
