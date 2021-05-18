import os
from dotenv import load_dotenv

from flask import g
from flask_oauthlib.client import OAuth

load_dotenv('.env')

oauth = OAuth()

# GITHUB CLIENT
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


# TWITTER CLIENT
twitter = oauth.remote_app(
    'twitter',
    consumer_key=os.getenv('TWITTER_API_KEY'),
    consumer_secret=os.getenv('TWITTER_SECRET_KEY'),
    base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_method='POST',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authorize',
    app_key='TWITTER'
)


@twitter.tokengetter
def twitter_token():
    if 'oauth_token' in g:
        return g.access_token


# GOOGLE CLIENT
google = oauth.remote_app(
    'google',
    consumer_key=os.getenv('GOOGLE_CLIENT_ID'),
    consumer_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    request_token_params={'scope': ['email', 'profile', 'openid']},
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    app_key='GOOGLE'
)


@google.tokengetter
def google_token():
    if 'access_token' in g:
        return g.access_token


# FACEBOOK CLIENT
facebook = oauth.remote_app(
    'facebook',
    consumer_key=os.getenv('FACEBOOK_CLIENT_ID'),
    consumer_secret=os.getenv('FACEBOOK_CLIENT_SECRET'),
    request_token_params={'scope': 'email'},
    base_url='https://graph.facebook.com',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    access_token_method='GET',
    authorize_url='https://www.facebook.com/dialog/oauth',
    app_key='FACEBOOK'
)


@facebook.tokengetter
def facebook_token():
    if 'access_token' in g:
        return g.access_token
