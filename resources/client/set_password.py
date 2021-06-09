from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from schema.client.client import ClientSchema
from models.client.client import ClientModel
from libs.strings import gettext

client_schema = ClientSchema()


class SetPassword(Resource):
    """
    Allows signed in users to set a new password for their accounts. It takes a
    POST request data with user email and new password
    """
    @classmethod
    @jwt_required(fresh=True)
    def post(cls):
        client_json = request.get_json()  # email and new password
        client_data = client_schema.load(client_json)

        client = ClientModel.find_client_by_email(client_data['email'])

        if not client:
            return {'msg': gettext('set_password_client_not_found')}, 401

        # 1. Check if new password matches old password
        if client.verify_password(client_data['password']):
            return {'msg': gettext('set_password_new_cannot_be_old')}

        client.hash_password(client_data['password'])
        client.save_client_to_db()

        return {'msg': gettext('set_password_updated_successfully')}, 201
