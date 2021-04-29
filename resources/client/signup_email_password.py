import traceback

from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from schema.client.client import ClientSchema
from models.client.client import ClientModel
from models.client.confirmation import ConfirmationModel
from libs.mailgun import MailgunException

client_schema = ClientSchema()

EMAIL_ALREADY_EXISTS = 'A user with email \'{}\' already exists.'
USERNAME_ALREADY_EXISTS = 'A user with username \'{}\' already exists.'
CLIENT_CREATION_SUCCESSFUL = 'Client account created successfully. Check your email to activate your account'
ACCOUNT_CREATION_FAILED = 'Account creation failed. Please try again.'


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

        # 2. Check if username or email fields already exist in db
        if ClientModel.find_client_by_email(data['email']):
            return {'msg': EMAIL_ALREADY_EXISTS.format(data['email'])}, 400

        elif ClientModel.find_client_by_username(data['username']):
            return {'msg': USERNAME_ALREADY_EXISTS.format(data['username'])}, 400
            # 3. If 2 above is false, create a new client and save to db

        else:
            try:
                # create client
                client = ClientModel(**data)

                # hash password and save client to db
                client.hash_password(client.password)
                client.save_client_to_db()

                # create a confirmation property for the client just created
                confirmation = ConfirmationModel(client.id)
                confirmation.save_to_db()

                # send verification email
                client.send_verification_email()

                # 4. Return successful creation message with 200 OK status code
                return {'msg': CLIENT_CREATION_SUCCESSFUL}, 201
            except MailgunException as err:
                client.delete_client_from_db()  # Roll back all changes
                return {'msg': str(err)}, 500
            except:
                traceback.print_exc()
                client.delete_client_from_db()
                return {'msg': ACCOUNT_CREATION_FAILED}, 500
