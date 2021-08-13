from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from libs.strings import gettext
from models.client.client import ClientModel
from libs.aws_helper import (
    create_presigned_post_url,
    s3_client,
    bucket_name,
    create_presigned_url
)


class Avatar(Resource):
    @classmethod
    @jwt_required(fresh=True)
    def put(cls):
        """
        Get presigned post url to upload avatar to S3
        """
        jwt_id = get_jwt_identity()
        client = ClientModel.find_user_by_id(jwt_id)
        if client is None:
            return {'msg': gettext('client_profile_client_does_not_exist')}, 400

        # 1. Set object_name
        avatar_obj_name = f'client_{jwt_id}/avatar'

        # 2. Create S3 url and fields for upload
        presigned_resp = create_presigned_post_url(s3_client, bucket_name, avatar_obj_name)
        return presigned_resp, 200

    @classmethod
    @jwt_required()
    def get(cls):
        """
        Returns the link to image if it exists in S3 bucket
        """
        jwt_id = get_jwt_identity()
        client = ClientModel.find_user_by_id(jwt_id)
        if client is None:
            return {'msg': gettext('client_profile_client_does_not_exist')}, 400

        avatar_url = create_presigned_url(s3_client, bucket_name, client.avatar_filename)
        return {'msg': avatar_url}, 200

    @classmethod
    @jwt_required(fresh=True)
    def delete(cls):
        client = ClientModel.find_user_by_id(get_jwt_identity())
        if not client:
            return {'msg': gettext('client_profile_client_does_not_exist')}, 400
        if client.id != get_jwt_identity():
            return {'msg': gettext('client_profile_deletion_unauthorized')}, 403

        if client.avatar_uploaded:
            avatar_obj_name = client.avatar_filename
            try:
                delete_resp = s3_client.delete_object(bucket_name, avatar_obj_name)
            except Exception as e:
                return {'msg': str(e)}, 500
            else:
                return {'msg': gettext('avatar_deleted')}, 200


class AvatarUploaded(Resource):
    @classmethod
    @jwt_required()
    def post(cls, status_code, obj_key):
        """Update client record with successful S3 upload of avatar"""
        client = ClientModel.find_user_by_id(get_jwt_identity())
        if status_code == 204:
            try:
                client.avatar_uploaded = True
                client.avatar_filename = obj_key
                client.update_user_in_db()
            except Exception as e:
                return {'msg': str(e)}, 500
            else:
                return {'msg': gettext('avatar_uploaded')}
        return {'msg': gettext('avatar_upload_failed')}
