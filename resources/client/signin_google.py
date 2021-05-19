from flask_restful import Resource
from flask import url_for, g
from flask_jwt_extended import create_access_token, create_refresh_token

from models.client.client import ClientModel
from models.client.confirmation import ConfirmationModel
from o_auth import google
from libs.strings import gettext


class GoogleSignIn(Resource):
    @classmethod
    def get(cls):
        return google.authorize(callback=url_for('google.auth', _external=True))


class GoogleAuth(Resource):
    @classmethod
    def get(cls):
        response = google.authorized_response()
        if response is None or response.get('access_token') is None:
            error_message = {
                'msg': gettext('google_redirect_url_error')
            }
            return error_message

        g.access_token = response['access_token']

        google_user = google.get('userinfo')
        # return google_user.data

        user_email = google_user.data['email']

        if not user_email:
            return {'msg': gettext('google_verification_failed')}

        client = ClientModel.find_client_by_email(user_email)

        if not client:
            try:
                client = ClientModel(
                    email=user_email,
                    oauth_token=g.access_token,
                    first_name=google_user.data['given_name'],
                    last_name=google_user.data['family_name'],
                    username=google_user.data['given_name']
                )
                client.save_client_to_db()

                confirmation = ConfirmationModel(client.id)
                confirmation.confirmed = True
                confirmation.save_to_db()

            except Exception as e:
                client.delete_client_from_db()
                return {'msg': str(e)}, 400

        access_token = create_access_token(identity=client.email, fresh=True)
        refresh_token = create_refresh_token(identity=client.email)

        return {'access_token': access_token, 'refresh_token': refresh_token}, 200
