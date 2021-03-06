from flask import request
from marshmallow import ValidationError
from flask_restful import Resource

from schema.client.client import ClientSchema
from libs.user_helper import signin_user_with_email
from models.client.client import ClientModel

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

        return signin_user_with_email(ClientModel, data)
