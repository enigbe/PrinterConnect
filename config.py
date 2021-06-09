import os

DEBUG = False
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///printerconnect_prod.db')
TWITTER_SIGNATURE_METHOD = os.environ.get('TWITTER_SIGNATURE_METHOD')
