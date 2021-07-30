from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from models.client.client import ClientModel
from libs.user_helper import sign_out_user


class SignOut(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        jti = get_jwt()['jti']
        client_id = get_jwt_identity()
        return sign_out_user(ClientModel, jti, client_id)
