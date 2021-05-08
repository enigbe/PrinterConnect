from typing import List
from flask_restful import Resource
from flask import g, request, url_for
from flask_jwt_extended import create_access_token, create_refresh_token

from oa import github
from models.client.client import ClientModel
from models.client.confirmation import ConfirmationModel
from libs.strings import gettext


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

        github_email = github_user.data['email']
        name = github_user.data['name']
        fullname = split_name(name)

        if not github_email:
            return {'msg': gettext('github_authorization_rejected')}

        client = ClientModel.find_client_by_email(github_email)
        if not client:
            try:
                # 1. create new client
                client = ClientModel(email=github_email, username=None, first_name=fullname[0],
                                     last_name=fullname[1], password=None, oauth_token=g.access_token
                                     )
                # 2. save client to db
                client.save_client_to_db()
                # 4. create confirmation with client's id
                confirmation = ConfirmationModel(client.id)
                # 5. make confirmation.confirmed true
                confirmation.confirmed = True
                # 6. save confirmation to db
                confirmation.save_to_db()
            except Exception as e:
                return {'msg': str(e)}, 400

        access_token = create_access_token(identity=client.email, fresh=True)
        refresh_token = create_refresh_token(identity=client.email)

        return {"access_token": access_token, "refresh_token": refresh_token}


def empty_email(email: str) -> bool:
    return True if email == '' else False


def split_name(name: str) -> List:
    return name.split(' ')
