from marshmallow import fields, validate, pre_dump

from models.client.client import ClientModel
from ma import ma


class ClientSchema(ma.SQLAlchemyAutoSchema):
    # Field Validation
    email = fields.Email(
        required=True,
        validate=validate.Email(error='Enter a valid email address.')
    )
    username = fields.String(
        validate=validate.Length(min=2, max=20, error='Username must be between 2 and 15 characters.')
    )
    first_name = fields.String(
        validate=validate.Length(min=2, max=20, error='First name must be between 2 and 20 characters.')
    )
    last_name = fields.String(
        validate=validate.Length(min=2, max=20, error='Last name must be between 2 and 20 characters.')
    )
    password = fields.String(
        validate=validate.Length(min=8, error='Password must be between 8 and 20 characters.')
    )
    is_activated = fields.Boolean(required=False)

    # Schema
    class Meta:
        model = ClientModel
        # load_instance = True
        load_only = ('password',)  # do not include when dumping data
        dump_only = ('id', 'confirmation')  # do not include when loading data

    @pre_dump
    def _pre_dump(self, client: ClientModel, **kwargs):
        client.confirmation = [client.most_recent_confirmation]
        return client
