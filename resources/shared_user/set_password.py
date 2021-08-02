from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from schema.client.client import ClientSchema
from schema.business.business import BusinessSchema
from models.client.client import ClientModel
from models.business.business import BusinessModel
from libs.user_helper import set_password, reset_password_link, reset_password

client_schema = ClientSchema(only=('email', 'password',), partial=True)
business_schema = BusinessSchema(only=('email', 'password',), partial=True)


class SetPassword(Resource):
    """
    Allows signed in client users to set a new password for their accounts. It takes a
    POST request data with user email and new password
    """
    @classmethod
    @jwt_required(fresh=True)
    def post(cls, user_type, username):
        user_schema = client_schema if user_type == 'client' else business_schema
        user_data = user_schema.load(request.get_json())  # new password
        user_id = get_jwt_identity()
        user = ClientModel.find_user_by_username(username) if user_type == 'client' else \
            BusinessModel.find_user_by_username(username)

        return set_password(user_data, user, user_id)


class PasswordResetLink(Resource):
    """Send a password reset link to an existing user's email"""
    @classmethod
    def post(cls, user_type):
        user_schema = client_schema if user_type == 'client' else business_schema
        submitted_email = user_schema.load(request.get_json())  # email
        user_models_dict = {'client': ClientModel, 'business': BusinessModel}
        user_model = user_models_dict['client'] if user_type == 'client' else user_models_dict['business']
        return reset_password_link(user_model, submitted_email['email'])


class ResetPassword(Resource):
    @classmethod
    def post(cls, user_type):
        user_schema = client_schema if user_type == 'client' else business_schema
        user_data = user_schema.load(request.get_json())  # email and password
        user_model = BusinessModel if user_type == 'business' else ClientModel
        return reset_password(user_model, user_data)
