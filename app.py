import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from marsh_mallow import ma
from o_auth import oauth
from resources.client.signup_email_password import ClientEmailSignUp
from resources.client.confirmation import Confirmation, ConfirmationByUser
from resources.client.signin_email_password import ClientEmailSignIn
from resources.client.signin_github import GithubSignIn, GithubAuth
from resources.client.signin_twitter import TwitterSignIn, TwitterAuth
from resources.client.signin_google import GoogleSignIn, GoogleAuth
from resources.client.signin_facebook import FacebookSignIn, FacebookAuth
from resources.homepage.home import Home
from resources.client.set_password import SetPassword

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///pc_test.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('PRINTERCONNECT_SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.environ.get('PRINTERCONNECT_JWT_SECRET_KEY')
app.config['TWITTER_SIGNATURE_METHOD'] = 'HMAC-SHA1'


api = Api(app)
jwt = JWTManager(app)


@app.before_first_request
def create_db_tables():
    from data_base import db
    db.create_all()


api.add_resource(ClientEmailSignUp, '/client/signup/email')
api.add_resource(Confirmation, '/client/confirmation/<string:confirmation_id>')
api.add_resource(ConfirmationByUser, '/client/resend_confirmation/<string:email>')
api.add_resource(ClientEmailSignIn, '/client/signin/email')
api.add_resource(GithubSignIn, '/client/signin/github')
api.add_resource(GithubAuth, '/client/github/auth', endpoint='github.auth')
api.add_resource(TwitterSignIn, '/client/signin/twitter')
api.add_resource(TwitterAuth, '/client/twitter/auth', endpoint='twitter.auth')
api.add_resource(GoogleSignIn, '/client/signin/google')
api.add_resource(GoogleAuth, '/client/google/auth', endpoint='google.auth')
api.add_resource(FacebookSignIn, '/client/signin/facebook')
api.add_resource(FacebookAuth, '/client/facebook/auth', endpoint='facebook.auth')
api.add_resource(Home, '/')
api.add_resource(SetPassword, '/client/password')


if __name__ == '__main__':
    from data_base import db

    db.init_app(app)
    ma.init_app(app)
    oauth.init_app(app)

    app.run(port=5001, debug=True)
