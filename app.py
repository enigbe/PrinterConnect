from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_uploads import configure_uploads, patch_request_class
from flask_migrate import Migrate

from data_base import db
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
from resources.client.avatar import AvatarUpload, Avatar
from resources.client.sign_out import SignOut
# from resources.client.client_profile import ClientProfile
from resources.client.token_refresh import TokenRefresh, BlockedTokens
# from resources.client.client_search import ClientSearch
from libs.image_helper import IMAGE_SET
from dotenv import load_dotenv

from models.client.token_blocklist import TokenBlockListModel

app = Flask(__name__)
load_dotenv()
app.config.from_object("default_config")
app.config.from_envvar("APPLICATION_SETTINGS")
patch_request_class(app, 10 * 1024 * 1024)  # 10 MB
configure_uploads(app, IMAGE_SET)
api = Api(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

db.init_app(app)


@app.before_first_request
def create_db_tables():
    db.create_all()


@jwt.token_in_blocklist_loader
def block_jwt(jwt_header, jwt_data):
    jti = jwt_data['jti']
    saved_jti = TokenBlockListModel.find_token_by_jti(jti)
    return saved_jti is not None


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
api.add_resource(AvatarUpload, '/client/avatar/upload')
api.add_resource(Avatar, '/client/avatar')
api.add_resource(SignOut, '/client/signout')
api.add_resource(BlockedTokens, '/token/blocked/<string:email>')
# api.add_resource(ClientProfile, '/client/profile')
api.add_resource(TokenRefresh, '/token/refresh')
# api.add_resource(ClientSearch, '/client/profile/search/<string:username>')
api.add_resource(Home, '/')
api.add_resource(SetPassword, '/client/password')


if __name__ == '__main__':
    ma.init_app(app)
    oauth.init_app(app)

    app.run(port=5001)
