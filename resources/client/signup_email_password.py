from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from schema.client.client import ClientSchema
from models.client.client import ClientModel
from libs.user_helper import signup_user_with_email

client_schema = ClientSchema()


class ClientEmailSignUp(Resource):
    """
    Allows users to create a client account with a POST request given the following parameters:

    :param email: User's email in String format
    :param username: User's username in String format
    :param first_name: User's first name in String format
    :param last_name: User's last name in String format
    :param password: User's un-encrypted password in String format (Password hashing: Future implementation)

    :return A tuple where tuple[0] is dictionary of successful creation (or error) and tuple[1] is status code
    """

    @classmethod
    def post(cls):
        # 1. Deserialize and validate request body
        try:
            data_received = request.get_json()
            data = client_schema.load(data_received)
        except ValidationError as err:
            return err.messages, 400

        return signup_user_with_email(ClientModel, data)
