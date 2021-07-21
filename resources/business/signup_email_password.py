from flask_restful import Resource
from flask import request
from marshmallow import ValidationError

from schema.business.business import BusinessSchema
from libs.user_helper import signup_user_with_email
from models.business.business import BusinessModel


class BusinessEmailSignUp(Resource):
    @classmethod
    def post(cls):
        try:
            schema = BusinessSchema()
            signup_data = schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400

        return signup_user_with_email(BusinessModel, signup_data)
