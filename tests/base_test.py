"""
BaseTest

This is the parent of all non-unit, i.e. system and integration, tests.
This BaseTest class allows the creation of (set up) new empty databases
each time and clearing out (tear down) of these databases
"""
import os
from unittest import TestCase
from app import app
from data_base import db
from dotenv import load_dotenv


class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Create new database
        load_dotenv('.env')

        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        app.config['SECRET_KEY'] = os.urandom(16)
        app.config['JWT_SECRET_KEY'] = os.urandom(16)
        app.config['GITHUB'] = {
            'consumer_key': os.getenv('GITHUB_CLIENT_ID'),
            'consumer_secret': os.getenv('GITHUB_CLIENT_SECRET'),
        }
        app.config['TWITTER'] = {
            'consumer_key': os.getenv('TWITTER_API_KEY'),
            'consumer_secret': os.getenv('TWITTER_SECRET_KEY'),
            'signature_method': 'HMAC-SHA1'
        }
        app.config['GOOGLE'] = {
            'consumer_key': os.getenv('GOOGLE_CLIENT_ID'),
            'consumer_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
        }

        with app.app_context():  # Creates application context and installs app in it
            db.init_app(app)

    def setUp(self) -> None:
        with app.app_context():  # Creates application context and installs app in it
            db.create_all()

        # Get a test client
        self.app = app.test_client
        self.app_context = app.app_context

    def tearDown(self) -> None:
        # Make sure database is blank
        with app.app_context():
            db.session.remove()  # clear the data in current session
            db.drop_all()        # drop all tables
