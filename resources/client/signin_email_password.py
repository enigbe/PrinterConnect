from flask import request
from marshmallow import ValidationError
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token

from schema.client.client import ClientSchema
from models.client.client import ClientModel
from libs.strings import gettext

client_schema = ClientSchema()


class ClientEmailSignIn(Resource):
    @classmethod
    def post(cls):
        try:
            # 1. Collect data from request
            request_data = request.get_json()
            # 2. Validate data against schema
            data = client_schema.load(request_data, partial=True)
        except ValidationError as err:
            return err.messages, err.valid_data

        # 3. Check if email is in db
        client = ClientModel.find_client_by_email(data['email'])
        if client and client.verify_password(data['password']):
            confirmation = client.most_recent_confirmation
            if confirmation and confirmation.confirmed:
                # 4. If 3 above is true, generate an access and refresh token to access protected endpoints
                access_token = create_access_token(identity=client.id, fresh=True)
                refresh_token = create_refresh_token(identity=client.id)

                return {
                    'msg': gettext('signin_successful'),
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }, 200
            return {'msg': gettext('signin_account_not_confirmed')}, 401
        # 5. Return success message and tokens
        return {'msg': gettext('signin_invalid_credentials')}, 401
