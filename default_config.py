import os

DEBUG = False
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True
SECRET_KEY = os.environ['PRINTERCONNECT_SECRET_KEY']
JWT_SECRET_KEY = os.environ['PRINTERCONNECT_JWT_SECRET_KEY']
TWITTER_SIGNATURE_METHOD = 'HMAC-SHA1'
UPLOADED_IMAGES_DEST = os.path.join("static", "images")
UPLOADS_DEFAULT_DEST = os.path.join("static")
aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
MAX_CONTENT_LENGTH = 5 * 1024 * 1024
AWS_S3_BUCKET_NAME = os.environ['AWS_S3_BUCKET_NAME']
