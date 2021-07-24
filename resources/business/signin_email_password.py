from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from schema.business.business import BusinessSchema
from models.business.business import BusinessModel

from libs.user_helper import signin_user_with_email

business_schema = BusinessSchema(only=('email', 'password',))


class BusinessEmailSignIn(Resource):
    @classmethod
    def post(cls):
        try:
            # 1. Collect data from request
            request_data = request.get_json()
            # 2. Validate data against schema
            data = business_schema.load(request_data, partial=True)
        except ValidationError as err:
            return err.messages, err.valid_data

        return signin_user_with_email(BusinessModel, data)
