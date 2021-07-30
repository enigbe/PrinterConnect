from flask import url_for, g
from flask_restful import Resource
from flask_jwt_extended import create_refresh_token, create_access_token

from o_auth import facebook
from libs.strings import gettext
from models.client.client import ClientModel
from models.confirmation import ConfirmationModel
from libs.user_helper import save_and_confirm_user


class FacebookSignIn(Resource):
    @classmethod
    def get(cls):
        return facebook.authorize(callback=url_for('facebook.auth', _external=True))


class FacebookAuth(Resource):
    @classmethod
    def get(cls):
        response = facebook.authorized_response()
        if response is None or response.get('access_token') is None:
            error_message = {
                'msg': gettext('facebook_redirect_url_error')
            }
            return error_message

        g.access_token = response['access_token']

        facebook_user = facebook.get('/me?fields=email,first_name,last_name,picture,short_name').data
        facebook_user_email = facebook_user['email']

        if not facebook_user_email:
            return {'msg': gettext('facebook_authorization_rejected')}

        client = ClientModel.find_user_by_email(facebook_user_email)
        if not client:
            try:
                client = ClientModel(
                    email=facebook_user_email,
                    first_name=facebook_user['first_name'],
                    last_name=facebook_user['last_name'],
                    username=facebook_user['short_name'],
                    oauth_token=g.access_token,
                    password=None
                )
                save_and_confirm_user(client)

            except Exception as e:
                client.delete_user_from_db()
                return {'msg': str(e)}, 400

        access_token = create_access_token(identity=client.id, fresh=True)
        refresh_token = create_refresh_token(identity=client.id)

        return {"access_token": access_token, "refresh_token": refresh_token}, 200
