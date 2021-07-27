from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_uploads import configure_uploads, patch_request_class
from flask_migrate import Migrate

from data_base import db
from marsh_mallow import ma
from o_auth import oauth
# Client
from resources.client.signup_email_password import ClientEmailSignUp
from resources.confirmation import Confirmation, ConfirmationByUser
from resources.client.signin_email_password import ClientEmailSignIn
from resources.client.signin_github import GithubSignIn, GithubAuth
from resources.client.signin_twitter import TwitterSignIn, TwitterAuth
from resources.client.signin_google import GoogleSignIn, GoogleAuth
from resources.client.signin_facebook import FacebookSignIn, FacebookAuth
from resources.client.set_password import SetPassword
from resources.client.avatar import Avatar
from resources.client.sign_out import SignOut
from resources.client.client_profile import ClientProfile
from resources.client.token_refresh import TokenRefresh, BlockedTokens
from resources.client.client_search import ClientSearch
from resources.client.cad_model import CADModelResource, CADModelList
# Business
from resources.business.signup_email_password import BusinessEmailSignUp
from resources.business.signin_email_password import BusinessEmailSignIn
from resources.business.business_profile import BusinessProfile
# General
from resources.homepage.home import Home

from libs.upload_helper import IMAGE_SET, CAD_MODEL_SET
from libs.aws_helper import s3_client, initialize_bucket, bucket_name
from dotenv import load_dotenv

from models.client.token_blocklist import TokenBlockListModel

app = Flask(__name__)
load_dotenv()
app.config.from_object("default_config")
app.config.from_envvar("APPLICATION_SETTINGS")
# Flask-Upload Specification
patch_request_class(app, 5 * 1024 * 1024)  # 5 MB
configure_uploads(app, IMAGE_SET)
configure_uploads(app, CAD_MODEL_SET, )

api = Api(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

db.init_app(app)


@app.before_first_request
def create_db_tables():
    # Create all tables in DB
    db.create_all()
    # AWS S3 bucket
    initialize_bucket(bucket_name, s3_client)


@jwt.token_in_blocklist_loader
def block_jwt(jwt_header, jwt_data):
    jti = jwt_data['jti']
    saved_jti = TokenBlockListModel.find_token_by_jti(jti)
    return saved_jti is not None


# Client Resources
api.add_resource(ClientEmailSignUp, '/client/signup/email')
api.add_resource(SetPassword, '/client/password')
api.add_resource(Confirmation, '/<string:user_model_type>/confirmation/<string:confirmation_id>')
api.add_resource(ConfirmationByUser,
                 '/<string:user_model_type>/re_confirmation/<string:email>')
api.add_resource(ClientEmailSignIn, '/client/signin/email')
api.add_resource(GithubSignIn, '/client/signin/github')
api.add_resource(GithubAuth, '/client/github/auth', endpoint='github.auth')
api.add_resource(TwitterSignIn, '/client/signin/twitter')
api.add_resource(TwitterAuth, '/client/twitter/auth', endpoint='twitter.auth')
api.add_resource(GoogleSignIn, '/client/signin/google')
api.add_resource(GoogleAuth, '/client/google/auth', endpoint='google.auth')
api.add_resource(FacebookSignIn, '/client/signin/facebook')
api.add_resource(FacebookAuth, '/client/facebook/auth',
                 endpoint='facebook.auth')
api.add_resource(Avatar, '/client/avatar')
api.add_resource(SignOut, '/client/signout')
api.add_resource(BlockedTokens, '/token/blocked/<string:email>')
api.add_resource(ClientProfile, '/client/<string:username>/profile')
api.add_resource(TokenRefresh, '/token/refresh')
api.add_resource(ClientSearch, '/client/profile/search/<string:username>')
api.add_resource(CADModelResource, '/client/<string:username>/cad_model/<string:cad_model_name>')
api.add_resource(CADModelList, '/client/<string:username>/cad_models')
# Business Resources
api.add_resource(BusinessEmailSignUp, '/business/signup/email')
api.add_resource(BusinessEmailSignIn, '/business/signin/email')
api.add_resource(BusinessProfile, '/business/<string:username>/profile')
# General Resources
api.add_resource(Home, '/')


if __name__ == '__main__':
    ma.init_app(app)
    oauth.init_app(app)

    app.run(port=5001)
