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


class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with app.app_context():  # Creates application context and installs app in it
            # Create new database
            db.init_app(app)

    def setUp(self) -> None:
        with app.app_context():  # Creates application context and installs app in it
            # Create new database tables
            db.create_all()

        # Get a test client
        self.app = app.test_client
        self.app_context = app.app_context

    def tearDown(self) -> None:
        # Make sure database is blank
        with app.app_context():
            db.session.remove()  # clear the data in current session
            db.drop_all()        # drop all tables
