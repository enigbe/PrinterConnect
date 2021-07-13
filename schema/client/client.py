from marshmallow import fields, validate, pre_dump

from models.client.client import ClientModel
from marsh_mallow import ma
from libs import upload_helper
from libs.upload_helper import IMAGE_SET
from libs.strings import gettext


class ClientSchema(ma.SQLAlchemyAutoSchema):
    # Field Validation
    email = fields.Email(
        required=True,
        validate=validate.Email()
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
        load_only = ('password', 'oauth_token', 'oauth_token_secret')  # do not include when dumping data
        dump_only = (
            'id',
            'confirmation',
            # 'oauth_token',
            'oauth_token_secret',
            'cad_model',
            'token_blocklist'
            'avatar_filename',
        )  # do not include when loading data

    avatar_url = fields.Method(serialize='dump_avatar_url')

    @staticmethod
    def dump_avatar_url(client: ClientModel):
        # Default avatar config
        avatar_filename = 'default-avatar'
        folder = 'assets'
        default_avatar_path = upload_helper.find_upload_any_format(IMAGE_SET, avatar_filename, folder)
        # Uploaded avatar config
        if client.avatar_filename and client.avatar_uploaded is True:
            folder = 'avatars'
            avatar_path = upload_helper.find_upload_any_format(IMAGE_SET, client.avatar_filename, folder)
            if avatar_path is None:
                return gettext('base_url') + default_avatar_path
            return gettext('base_url') + avatar_path

        return gettext('base_url') + default_avatar_path

    @pre_dump
    def _pre_dump(self, client: ClientModel, **kwargs):
        client.confirmation = [client.most_recent_confirmation]
        return client
