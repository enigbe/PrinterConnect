import os

DEBUG = True
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True
SECRET_KEY = os.environ['PRINTERCONNECT_SECRET_KEY']
JWT_SECRET_KEY = os.environ['PRINTERCONNECT_JWT_SECRET_KEY']
TWITTER_SIGNATURE_METHOD = 'HMAC-SHA1'
UPLOADED_IMAGES_DEST = os.path.join("static", "images")
