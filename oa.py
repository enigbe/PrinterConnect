import os
from flask import g
from flask_oauthlib.client import OAuth
from dotenv import load_dotenv

load_dotenv('.env')
oauth = OAuth()

github = oauth.remote_app(
    'github',
    consumer_key=os.getenv('GITHUB_CLIENT_ID'),
    consumer_secret=os.getenv('GITHUB_CLIENT_SECRET'),
    request_token_params={'scope': 'read:user,user'},
    base_url='https://api.github.com',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    app_key='GITHUB'
)


@github.tokengetter
def github_token():
    if 'access_token' in g:
        return g.access_token
