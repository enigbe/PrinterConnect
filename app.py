from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint

from data_base import db
from marsh_mallow import ma
from o_auth import oauth
# Client
from resources.client.signup_email_password import ClientEmailSignUp
from resources.shared_user.confirmation import Confirmation, ConfirmationByUser
from resources.client.signin_email_password import ClientEmailSignIn
from resources.client.signin_github import GithubSignIn, GithubAuth
from resources.client.signin_twitter import TwitterSignIn, TwitterAuth
from resources.client.signin_google import GoogleSignIn, GoogleAuth
from resources.client.signin_facebook import FacebookSignIn, FacebookAuth
from resources.shared_user.set_password import SetPassword, PasswordResetLink, ResetPassword
from resources.client.avatar import Avatar, AvatarUploaded
from resources.client.client_sign_out import SignOut
from resources.client.client_profile import ClientProfile
from resources.shared_user.token_refresh import TokenRefresh, BlockedTokens
from resources.client.client_search import ClientSearch
from resources.client.cad_model import CADModelResource, CADModelList
# Business
from resources.business.signup_email_password import BusinessEmailSignUp
from resources.business.signin_email_password import BusinessEmailSignIn
from resources.business.business_sign_out import BusinessSignOut
from resources.business.business_profile import BusinessProfile
from resources.business.printer import Printer, PrinterList
# General
from resources.homepage.home import Home
from libs.aws_helper import s3_client, initialize_bucket, bucket_name
from dotenv import load_dotenv

from models.shared_user.token_blocklist import TokenBlockListModel
# Configurations
app = Flask(__name__)
load_dotenv()
app.config.from_object("default_config")
app.config.from_envvar("APPLICATION_SETTINGS")

# Swagger Configuration
SWAGGER_URL = '/doc'
SWAGGER_API_URL = '/static/swagger.yaml'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    SWAGGER_API_URL,
    config={
        'app_name': 'PrinterConnect'
    }
)

api = Api(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
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
api.add_resource(AvatarUploaded, '/client/post_avatar')
api.add_resource(SignOut, '/client/signout')
api.add_resource(ClientProfile, '/client/<string:username>/profile')
api.add_resource(ClientSearch, '/client/profile/search/<string:username>')
api.add_resource(CADModelResource, '/client/<string:username>/cad_model/<string:cad_model_name>')
api.add_resource(CADModelList, '/client/<string:username>/cad_models')
# Business Resources
api.add_resource(BusinessEmailSignUp, '/business/signup/email')
api.add_resource(BusinessEmailSignIn, '/business/signin/email')
api.add_resource(BusinessProfile, '/business/<string:username>/profile')
api.add_resource(BusinessSignOut, '/business/signout')
api.add_resource(Printer, '/business/<string:username>/printer/<string:printer_name>')
api.add_resource(PrinterList, '/business/<string:username>/printers')
# Shared Resources
api.add_resource(SetPassword, '/<string:user_type>/<string:username>/profile/password')
api.add_resource(PasswordResetLink, '/<string:user_type>/password/reset_link')
api.add_resource(ResetPassword, '/<string:user_type>/password/reset')
api.add_resource(TokenRefresh, '/token/refresh')
api.add_resource(BlockedTokens, '/token/blocked/<string:user_type>')
api.add_resource(Confirmation, '/<string:user_model_type>/confirmation/<string:confirmation_id>')
api.add_resource(ConfirmationByUser,
                 '/<string:user_model_type>/re_confirmation/<string:email>')
# General Resources
api.add_resource(Home, '/')


if __name__ == '__main__':
    ma.init_app(app)
    oauth.init_app(app)

    app.run(port=5001)
