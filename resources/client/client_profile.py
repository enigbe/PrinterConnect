from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.client.client import ClientModel
from schema.client.client import ClientSchema
from libs.strings import gettext
from libs.mailgun import MailgunException

complete_client_schema = ClientSchema(
    only=('email', 'username', 'first_name', 'last_name', 'bio', 'avatar_url',)
)
partial_client_schema = ClientSchema(only=('username', 'bio'))


class ClientProfile(Resource):
    @classmethod
    @jwt_required()
    def get(cls, username):
        # 1. Check if client exists in database
        client = ClientModel.find_user_by_username(username)

        if not client:
            return {'msg': gettext('client_profile_client_does_not_exist')}, 400

        return {'client': complete_client_schema.dump(client)}, 200

    @classmethod
    @jwt_required(fresh=True)
    def delete(cls, username):
        client = ClientModel.find_user_by_username(username)

        if client is not ClientModel.find_client_by_id(get_jwt_identity()):
            return {'msg': gettext('client_profile_deletion_unauthorized')}, 403

        if client:
            try:
                client.delete_user_from_db()
                return {'msg': gettext('client_profile_client_deleted').format(client.username)}, 200
            except Exception as e:
                client.rollback()
                return {'msg': str(e)}, 500
        return {'msg': gettext('client_profile_client_does_not_exist')}, 400

    @classmethod
    @jwt_required()
    def patch(cls, username):
        """
        Update client profile data
        :return: None
        """
        # 1. Deserialize client request data
        data = complete_client_schema.load(request.get_json(), partial=True)
        # 2. Get client identity of logged in client via JWT
        client = ClientModel.find_user_by_username(username)

        if not client:
            return {'msg': gettext('client_profile_client_does_not_exist')}, 400

        if client is not ClientModel.find_user_by_id(get_jwt_identity()):
            return {'msg': gettext('client_profile_deletion_unauthorized')}, 403

        try:
            if 'email' in data and ClientModel.find_user_by_email(data['email']) is None:
                try:
                    client.email = data['email']
                    client.update_user_in_db()
                    client.send_update_email_notification(client.email)
                except MailgunException as e:
                    return {'msg': str(e)}, 500
                except Exception as e:
                    # rollback update
                    return {'msg': str(e)}, 500

            if 'username' in data and ClientModel.find_user_by_username(data["username"]) is None:
                client.username = data['username']

            if 'first_name' in data:
                client.first_name = data['first_name']

            if 'last_name' in data:
                client.last_name = data['last_name']

            if 'bio' in data:
                client.bio = data['bio']

            client.update_user_in_db()
            return {'msg': gettext('client_profile_update_successful')}, 200
        except Exception as e:
            return {'msg': str(e)}, 500
