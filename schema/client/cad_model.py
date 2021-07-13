import typing
from typing import Union
from marshmallow import fields, Schema
from werkzeug.datastructures import FileStorage

from marsh_mallow import ma
from models.client.cad_model import CADModel


class FileStorageField(fields.Field):
    default_error_messages = {
        "invalid": "Not a valid CAD file."
    }

    def _deserialize(
        self,
        value: typing.Any,
        attr: typing.Optional[str],
        data: typing.Optional[typing.Mapping[str, typing.Any]],
        **kwargs
    ) -> Union[FileStorage, None]:
        if value is None:
            return None

        if not isinstance(value, FileStorage):
            self.fail("invalid")  # raises a ValidationError

        return value


class CADModelSchema(Schema):
    cad = FileStorageField(required=True)


class CADSpecificationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CADModel
        include_fk = True
        # Do not include when dumping
        load_only = ('client_id', 'cad_object_key', 'id')
