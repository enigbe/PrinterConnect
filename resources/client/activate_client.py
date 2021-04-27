from flask_restful import Resource

from models.client.client import ClientModel

USER_NOT_FOUND = 'Client user account not found.'
USER_CONFIRMED = 'Client user account activated successfully.'


class ActivateClient(Resource):
    @classmethod
    def get(cls, username: str):
        user = ClientModel.find_client_by_username(username)

        if not user:
            return {'msg': USER_NOT_FOUND}, 404

        user.is_activated = True
        user.save_client_to_db()
        return {'msg': USER_CONFIRMED}, 200


