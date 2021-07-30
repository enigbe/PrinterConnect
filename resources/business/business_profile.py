from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request

from models.business.business import BusinessModel
from schema.business.business import BusinessSchema
from libs.user_helper import read_user, delete_user, update_user

complete_business_schema = BusinessSchema(only=('business_name', 'username', 'bio', 'email', 'creation_date',
                                                'password',), partial=True)
partial_business_schema = BusinessSchema(only=('business_name', 'username', 'bio',))


class BusinessProfile(Resource):
    @classmethod
    @jwt_required(optional=True)
    def get(cls, username):
        business = BusinessModel.find_user_by_username(username)
        business_id = get_jwt_identity()
        return read_user(
            username=username,
            user_instance=business,
            full_user_schema=complete_business_schema,
            partial_user_schema=partial_business_schema,
            user_id=business_id
        )

    @classmethod
    @jwt_required(fresh=True)
    def patch(cls, username):
        update_data = complete_business_schema.load(request.get_json())
        logged_in_business_id = get_jwt_identity()
        business = BusinessModel.find_user_by_username(username)

        return update_user(username, update_data, business, logged_in_business_id)

    @classmethod
    @jwt_required(fresh=True)
    def delete(cls, username):
        business = BusinessModel.find_user_by_username(username)
        business_id = get_jwt_identity()
        return delete_user(
            username=username,
            user_instance=business,
            user_id=business_id
        )
