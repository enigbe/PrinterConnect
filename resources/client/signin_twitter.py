from flask_restful import Resource
from flask import url_for, g
from flask_jwt_extended import create_refresh_token, create_access_token

from o_auth import twitter
from libs.strings import split_name, gettext
from models.client.client import ClientModel
from libs.user_helper import save_and_confirm_user


class TwitterSignIn(Resource):
    @classmethod
    def get(cls):
        response = twitter.authorize(callback=url_for('twitter.auth', _external=True))
        return response


class TwitterAuth(Resource):
    @classmethod
    def get(cls):
        response = twitter.authorized_response()
        if response is None or response.get('oauth_token') is None:
            error_response = {
                'msg': gettext('twitter_authorized_response_error')
            }

            return error_response

        g.oauth_token = response['oauth_token']
        g.oauth_token_secret = response['oauth_token_secret']
        g.access_token = (g.oauth_token, g.oauth_token_secret,)

        verified_user = twitter.get(
            'account/verify_credentials.json',
            data={'include_email': 'true'}
        )

        if not verified_user.data['email']:
            return {'msg': gettext('twitter_authorization_rejected')}, 401

        if verified_user.status == 200:
            verified_client = {
                'email': verified_user.data['email'],
                'username': verified_user.data['screen_name'],
                'first_name': split_name(verified_user.data['name'])[0],
                'last_name': split_name(verified_user.data['name'])[1],
                'oauth_token': g.oauth_token,
                'oauth_token_secret': g.oauth_token_secret,
                'password': None
            }

            pc_client = ClientModel.find_client_by_email(verified_client['email'])

            if not pc_client:
                # Create new client and grant access to protected endpoints
                try:
                    pc_client = ClientModel(**verified_client)
                    save_and_confirm_user(pc_client)
                except Exception as e:
                    pc_client.delete_client_from_db()
                    return {'msg': str(e)}, 400

            access_token = create_access_token(identity=pc_client.id, fresh=True)
            refresh_token = create_refresh_token(identity=pc_client.id)

            return {"access_token": access_token, "refresh_token": refresh_token}, 200
