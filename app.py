import os
from flask import Flask
from flask_restful import Api

from ma import ma
from resources.client.client_email_signup import ClientEmailSignUp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///printerconnect.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'enie'

api = Api(app)


@app.before_first_request
def create_db_tables():
    from db import db
    db.create_all()


api.add_resource(ClientEmailSignUp, '/client/signup/email')

if __name__ == '__main__':
    from db import db

    db.init_app(app)
    ma.init_app(app)

    app.run(port=5000, debug=True)