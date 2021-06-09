import typing
from typing import Union
from marshmallow import Schema, fields
from werkzeug.datastructures import FileStorage


class FileStorageField(fields.Field):
    default_error_messages = {
        "invalid": "Not a valid image."
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


class AvatarSchema(Schema):
    image = FileStorageField(required=True)
