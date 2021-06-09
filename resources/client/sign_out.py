import traceback
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from libs.strings import gettext
from models.client.token_blocklist import TokenBlockListModel
from models.client.client import ClientModel


class SignOut(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        jti = get_jwt()['jti']
        client = ClientModel.find_client_by_id(get_jwt_identity())
        revoked_token = TokenBlockListModel(jti=jti, client_id=client.id)
        try:
            revoked_token.save_token_to_db()
            return {'msg': 'Sign out successful'}, 200
        except Exception as e:
            traceback.print_exc(e)
            return {'msg': gettext('sign_out_token_addition_failed')}
