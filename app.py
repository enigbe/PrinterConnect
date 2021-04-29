import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from ma import ma
from resources.client.signup_email_password import ClientEmailSignUp
from resources.client.confirmation import Confirmation, ConfirmationByUser
from resources.client.signin_email_password import ClientEmailSignIn

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///pc_test.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('PRINTERCONNECT_SECRET_KEY')

api = Api(app)
jwt = JWTManager(app)


@app.before_first_request
def create_db_tables():
    from db import db
    db.create_all()


api.add_resource(ClientEmailSignUp, '/client/signup/email')
api.add_resource(Confirmation, '/client/confirmation/<string:confirmation_id>')
api.add_resource(ConfirmationByUser, '/client/resend_confirmation/<string:email>')
api.add_resource(ClientEmailSignIn, '/client/signin/email')

if __name__ == '__main__':
    from db import db

    db.init_app(app)
    ma.init_app(app)

    app.run(port=5000, debug=True)
