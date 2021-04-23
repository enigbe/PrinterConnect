from sqlite3 import IntegrityError
from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from schema.client.client import ClientSchema
from models.client.client import ClientModel

client_schema = ClientSchema()

EMAIL_ALREADY_EXISTS = 'A user with email \'{}\' already exists.'
USERNAME_ALREADY_EXISTS = 'A user with username \'{}\' already exists.'
CLIENT_CREATION_SUCCESSFUL = 'Client account created successfully. Check email to verify account'


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
            client = client_schema.load(data_received)  # Basically creates a ClientModel object
        except ValidationError as err:
            return err.messages, 400

        # 2. Check if username or email fields already exist in db
        if ClientModel.find_client_by_email(client.email):
            return {'msg': EMAIL_ALREADY_EXISTS.format(client.email)}, 400

        elif ClientModel.find_client_by_username(client.username):
            return {'msg': USERNAME_ALREADY_EXISTS.format(client.username)}, 400
            # 3. If 2 above is false, create a new client and save to db

        else:
            client.save_client_to_db()
            # 4. Return successful creation message with 200 OK status code
            return {'msg': CLIENT_CREATION_SUCCESSFUL}, 201
