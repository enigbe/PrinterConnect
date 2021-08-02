from flask_restful import Resource
from flask import g, request, url_for
from flask_jwt_extended import create_access_token, create_refresh_token

from o_auth import github
from models.client.client import ClientModel
from libs.strings import gettext, split_name
from libs.user_helper import save_and_confirm_user


class GithubSignIn(Resource):
    @classmethod
    def get(cls):
        response = github.authorize(callback=url_for('github.auth', _external=True))
        return response


class GithubAuth(Resource):
    @classmethod
    def get(cls):
        response = github.authorized_response()

        if response is None or response.get('access_token') is None:
            error_response = {
                'error': request.args['error'],
                'error_description': request.args['error_description']
            }

            return error_response

        g.access_token = response['access_token']
        github_user = github.get('user')

        github_username = github_user.data['login']
        github_email = github_user.data['email']
        name = github_user.data['name']
        fullname = split_name(name)

        if not github_email:
            return {'msg': gettext('github_authorization_rejected')}

        client = ClientModel.find_user_by_email(github_email)
        if not client:
            try:
                # 1. create new client
                client = ClientModel(
                    email=github_email,
                    username=github_username,
                    first_name=fullname[0],
                    last_name=fullname[1],
                    password=None,
                    oauth_token=g.access_token
                )
                save_and_confirm_user(client)
            except Exception as e:
                client.delete_user_from_db()

                return {'msg': str(e)}, 400

        access_token = create_access_token(identity=client.id, fresh=True)
        refresh_token = create_refresh_token(identity=client.id)

        return {"access_token": access_token, "refresh_token": refresh_token}, 200
