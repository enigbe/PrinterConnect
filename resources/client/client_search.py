from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.client.client import ClientModel
from schema.client.client import ClientSchema
from libs.strings import gettext


class ClientSearch(Resource):
    @classmethod
    @jwt_required(optional=True)
    def get(cls, username):
        partial_client_schema = ClientSchema(only=('username', 'bio',))
        complete_client_schema = ClientSchema(only=('email', 'username', 'first_name', 'last_name', 'avatar_url',
                                                    'bio'))
        client = ClientModel.find_client_by_id(get_jwt_identity())
        searched_client = ClientModel.find_client_by_username(username)

        if searched_client is None:
            return {'msg': gettext('client_profile_client_does_not_exist')}, 400

        if searched_client and client is None:
            return partial_client_schema.dump(searched_client), 200

        return complete_client_schema.dump(searched_client), 200
