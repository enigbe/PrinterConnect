import requests

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.client.client import ClientModel
from schema.client.cad_model import CADModelSchema, CADSpecificationSchema
from models.client.cad_model import CADModel
from libs.strings import gettext
from libs.upload_helper import get_extension, CAD_MODELS
from libs.aws_helper import (
    s3_client,
    bucket_name,
    create_presigned_url,
    create_presigned_post_url
)

cad_spec_keys = (
    'cad_model_name', 'cad_model_height', 'cad_model_width', 'cad_model_length', 'cad_model_material',
    'cad_model_mesh_percent', 'cad_model_visibility'
)
cad_file_keys = ('cad',)


class CADModelResource(Resource):
    """CAD model resource"""
    @classmethod
    @jwt_required(fresh=True)
    def post(cls):
        """Pre-sign a POST url for file upload to S3 and post"""
        specifications = CADSpecificationSchema(
            only=cad_spec_keys).load(request.form)

        model_name = specifications['cad_model_name']
        if CADModel.find_cad_model_by_name(model_name):
            return {'msg': gettext('cad_model_files_already_exist').format(model_name)}, 400

        # Secure the CAD file
        cad_fileobject = CADModelSchema(
            only=cad_file_keys).load(request.files)

        folder = f"client_{get_jwt_identity()}"
        cad_object_key = cad_fileobject['cad'].filename
        if get_extension(cad_object_key)[1:] not in CAD_MODELS:
            return {'msg': gettext('cad_model_invalid_extension')}, 400

        object_key = f"{folder}/{cad_object_key}"
        # Get a presigned post URL
        presigned_resp = create_presigned_post_url(
            s3_client, bucket_name, object_key)
        url, fields = presigned_resp['url'], presigned_resp['fields']

        cad = cad_fileobject['cad'].read()
        aws_resp = requests.post(url, data=fields, files={'file': cad})
        if aws_resp.status_code == 204:
            try:
                client_id = get_jwt_identity()
                specifications['cad_object_key'] = object_key
                cad_model = CADModel(client_id=client_id, **specifications)
                cad_model.save_cad_model_to_db()
            except Exception as e:
                return {'msg': str(e)}, 400
            else:
                return {'msg': gettext('cad_model_saved_successfully')}, 200

    @classmethod
    def get(cls):
        """Retrieve a CAD model from the DB given a unique name passed in the body"""
        name = CADSpecificationSchema(only=cad_spec_keys, partial=True).load(
            request.get_json())
        cad_model = CADModel.find_cad_model_by_name(name['cad_model_name'])

        if cad_model is None:
            return {'msg': gettext('cad_model_does_not_exist')}, 400

        if cad_model.cad_model_visibility == False:
            return {'msg': gettext('cad_model_not_visible')}, 403

        valid_cad_model = CADSpecificationSchema().dump(cad_model)
        # Get link to S3
        cad_url = create_presigned_url(
            s3_client, bucket_name, cad_model.cad_object_key)

        return {'cad_details': valid_cad_model, 'cad_url': cad_url}, 200

    @classmethod
    @jwt_required(fresh=True)
    def delete(cls):
        """Deletes a CAD model from DB and S3"""
        name = CADSpecificationSchema(only=cad_spec_keys, partial=True).load(
            request.get_json())
        cad_model = CADModel.find_cad_model_by_name(name['cad_model_name'])
        if cad_model is None:
            return {'msg': gettext('cad_model_does_not_exist')}, 400
        try:
            # Find the S3 object and delete
            delete_resp = s3_client.delete_object(
                Bucket=bucket_name, Key=cad_model.cad_object_key)
        except Exception as e:
            return {'msg': str(e)}, 500
        else:
            # Delete from server
            if delete_resp['ResponseMetadata']['HTTPStatusCode'] == 204:
                cad_model.delete_cad_model_from_db()
                return {'msg': gettext('cad_model_delete_successful').format(name['cad_model_name'])}

    @classmethod
    @jwt_required(fresh=True)
    def patch(cls):
        """Update existing CAD model given update parameters"""
        spec_schema = CADSpecificationSchema(only=cad_spec_keys, partial=True)
        cad_schema = CADModelSchema(only=cad_file_keys, partial=True)
        update_specs = spec_schema.load(request.form)
        update_cad = cad_schema.load(request.files)
        count = 0

        if update_cad == {} and update_specs == {}:
            return {'msg': gettext('cad_model_update_info_empty')}

        cad_filename = update_cad['cad'].filename if 'cad' in update_cad else ''
        if update_specs['cad_model_name'] == '' and cad_filename == '':
            return {'msg': gettext('cad_model_name_cannot_be_empty')}

        client_folder = f'client_{get_jwt_identity()}'
        current_cad = CADModel.find_cad_model_by_name(
            update_specs['cad_model_name'])

        if current_cad is None:
            return {'msg': gettext('cad_model_does_not_exist')}, 400

        if 'cad' in update_cad:
            # 1. Delete object with cad_object_key
            delete_resp = s3_client.delete_object(
                Bucket=bucket_name, Key=current_cad.cad_object_key)
            if delete_resp['ResponseMetadata']['HTTPStatusCode'] == 204:
                # 2. Upload CAD model to bucket
                object_key = f'{client_folder}/{cad_filename}'
                ps_data = create_presigned_post_url(
                    s3_client, bucket_name, object_key)
                url, fields = ps_data['url'], ps_data['fields']
                if get_extension(cad_filename)[1:] not in CAD_MODELS:
                    return {'msg': gettext('cad_model_invalid_extension')}, 400

                cad = update_cad['cad'].read()  # CAD model file
                requests.post(url, data=fields, files={'file': cad})
                # 3. Update cad_model_key
                current_cad.cad_object_key = object_key
                count += 1

        if 'cad_model_length' in update_specs:
            current_cad.cad_model_length = update_specs['cad_model_length']
            count += 1

        if 'cad_model_height' in update_specs:
            current_cad.cad_model_height = update_specs['cad_model_height']
            count += 1

        if 'cad_model_width' in update_specs:
            current_cad.cad_model_width = update_specs['cad_model_width']
            count += 1

        if 'cad_model_material' in update_specs:
            current_cad.cad_model_material = update_specs['cad_model_material']
            count += 1

        if 'cad_model_visibility' in update_specs:
            current_cad.cad_model_visibility = update_specs['cad_model_visibility']
            count += 1

        if 'cad_model_mesh_percent' in update_specs:
            current_cad.cad_model_mesh_percent = update_specs['cad_model_mesh_percent']
            count += 1

        if count > 0:
            current_cad.save_cad_model_to_db()
            return {'msg': gettext('cad_model_updated_successfully').format(current_cad.cad_model_name)}, 200
        return {'msg': gettext('cad_model_update_info_empty')}
