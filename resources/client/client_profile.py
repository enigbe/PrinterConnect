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
    def get(cls):
        # 1. Check if client exists in database
        client_id = get_jwt_identity()
        client = ClientModel.find_client_by_id(client_id)

        if not client:
            return {'msg': gettext('client_profile_client_does_not_exist')}, 400

        return {'client': complete_client_schema.dump(client)}, 200

    @classmethod
    @jwt_required(fresh=True)
    def delete(cls):
        client_id = get_jwt_identity()
        client = ClientModel.find_client_by_id(client_id)
        if client:
            try:
                client.delete_client_from_db()
                return {'msg': gettext('client_profile_client_deleted').format(client.username)}, 200
            except Exception as e:
                client.rollback()
                return {'msg': str(e)}, 500
        return {'msg': gettext('client_profile_deletion_unauthorized')}

    @classmethod
    @jwt_required()
    def patch(cls):
        """
        Update client profile data
        :return: None
        """
        # 1. Deserialize client request data
        data = complete_client_schema.load(request.get_json(), partial=True)
        # 2. Get client identity of logged in client via JWT
        client_id = get_jwt_identity()
        client = ClientModel.find_client_by_id(client_id)

        try:
            if 'email' in data and ClientModel.find_client_by_email(data['email']) is None:
                try:
                    client.email = data['email']
                    client.update_client_in_db()
                    client.send_update_email_notification(client.email)
                except MailgunException as e:
                    return {'msg': str(e)}, 500
                except Exception as e:
                    # rollback update
                    return {'msg': str(e)}, 500

            if 'username' in data and ClientModel.find_client_by_username(data["username"]) is None:
                client.username = data['username']

            if 'first_name' in data:
                client.first_name = data['first_name']

            if 'last_name' in data:
                client.last_name = data['last_name']

            if 'bio' in data:
                client.bio = data['bio']

            client.update_client_in_db()
            return {'msg': gettext('client_profile_update_successful')}, 200
        except Exception as e:
            return {'msg': str(e)}, 500
