import os
from flask import Flask
from flask_restful import Api

from ma import ma
from resources.client.client_email_signup import ClientEmailSignUp
from resources.client.activate_client import ActivateClient

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///pc_test.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('PRINTERCONNECT_SECRET_KEY')

api = Api(app)


@app.before_first_request
def create_db_tables():
    from db import db
    db.create_all()


api.add_resource(ClientEmailSignUp, '/client/signup/email')
api.add_resource(ActivateClient, '/client/activate/<string:username>')

if __name__ == '__main__':
    from db import db

    db.init_app(app)
    ma.init_app(app)

    app.run(port=5000, debug=True)
