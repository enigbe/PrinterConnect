import os
import traceback
from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask import request, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity

from libs import image_helper
from libs.strings import gettext
from schema.avatar import AvatarSchema
from schema.client.client import ClientSchema
from models.client.client import ClientModel

avatar_schema = AvatarSchema()
client_schema = ClientSchema(only=('avatar_url',))


class Avatar(Resource):
    @classmethod
    @jwt_required(fresh=True)
    def put(cls):
        """
        Upload an avatar (image) for user. Overwrites avatar if it exists.
        Uses JWT to extract user identity and save to user's folder. All
        avatars are named after the client's id: client_{id}.{ext}
        """
        # 1. Load FileStorage object/image from client request
        data = avatar_schema.load(request.files)  # {"image" : FileStorage}
        # 2. Create image name from current user token
        filename = f"client_{get_jwt_identity()}"  # client_{janedoe@email.com}
        # 3. Create destination folder for client avatar
        folder = "avatars"
        # 4. Search for image filename is folder
        avatar_path = image_helper.find_image_any_format(filename, folder)
        if avatar_path:
            try:
                os.remove(avatar_path)
            except UploadNotAllowed:
                return {'msg': gettext('avatar_delete_failed')}, 500

        try:
            # Get extension of uploaded image
            extension = image_helper.get_extension(data['image'].filename)
            # Create avatar name
            avatar = filename + extension
            # Save avatar to file system
            avatar_path = image_helper.save_image(
                data['image'], folder=folder, name=avatar
            )
            # Get client identity
            client_identity = get_jwt_identity()
            client = ClientModel.find_client_by_id(client_identity)
            # Set avatar upload and avatar filename
            client.avatar_uploaded = True
            client.avatar_filename = filename
            client.save_client_to_db()

            basename = image_helper.get_basename(avatar_path)
            return {'msg': gettext('avatar_uploaded').format(basename)}, 200
        except UploadNotAllowed:
            # client.rollback()
            extension = image_helper.get_extension(data['image'])
            return {'msg': gettext('avatar_extension_illegal').format(extension)}, 400

    @classmethod
    @jwt_required()
    def get(cls):
        """
        Returns the requested image if it exists in the logged in user's folder
        """
        filename = f"client_{get_jwt_identity()}"
        folder = "avatars"
        avatar = image_helper.find_image_any_format(filename, folder)
        if avatar:
            return send_file(avatar)

        default_filename = 'default-avatar'
        default_folder = 'assets'
        default_avatar = image_helper.find_image_any_format(default_filename, default_folder)
        # return {'msg': gettext('avatar_not_found').format(avatar)}, 404
        return send_file(default_avatar)

    @classmethod
    @jwt_required(fresh=True)
    def delete(cls):
        filename = f"client_{get_jwt_identity()}"
        folder = "avatars"
        avatar = image_helper.find_image_any_format(filename, folder)
        client = ClientModel.find_client_by_id(get_jwt_identity())
        if avatar:
            try:
                os.remove(avatar)
                client.avatar_uploaded = False
                client.avatar_filename = None
                client.update_client_in_db()
                return {'msg': gettext('avatar_deleted').format(filename)}, 200
            except FileNotFoundError:
                return {'msg': gettext('avatar_not_found').format(filename)}, 404
            except:
                client.rollback()
                traceback.print_exc()
                return {'msg': gettext('avatar_delete_failed')}, 500
