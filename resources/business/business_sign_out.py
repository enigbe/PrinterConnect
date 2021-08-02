from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from models.business.business import BusinessModel
from libs.user_helper import sign_out_user


class BusinessSignOut(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        jti = get_jwt()['jti']
        business_jwt_identity = get_jwt_identity()
        return sign_out_user(BusinessModel, jti, business_jwt_identity)
