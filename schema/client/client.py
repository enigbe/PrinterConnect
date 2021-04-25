import re

from marshmallow import validates_schema, ValidationError
from models.client.client import ClientModel
from ma import ma


class ClientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ClientModel
        load_instance = True
        load_only = ('password',)  # do not include when dumping data
        dump_only = ('id',)        # do not include when loading data

    @validates_schema
    def validate_username(self, data, **kwargs):
        username = data['username']
        username_length = len(username)
        if username_length < 3 or username_length > 10:
            raise ValidationError('Username must have between 3 and 10 characters.')

    @validates_schema
    def validate_password(self, data, **kwargs):
        password = data['password']
        password_length = len(password)
        if password_length < 8 or password_length > 25:
            raise ValidationError('Password must be between 8 and 25 characters long.')

    @validates_schema
    def validate_email(self, data, **kwargs):
        email = data['email']
        if not re.match('[^@]+@[^@]+\.[^@]', email):
            raise ValidationError('Please enter a valid email address.')

    @validates_schema  # change to validate empty fields using any() 
    def validate_empty_fields(self, data, **kwargs):
        value = all(data.values())

        if value is False:
            raise ValidationError('One (or more) field(s) is (are) empty.')
