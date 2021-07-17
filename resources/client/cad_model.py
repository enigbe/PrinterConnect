from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.client.client import ClientModel
from schema.client.cad_model import CADSpecificationSchema
from models.client.cad_model import CADModel
from libs.strings import gettext
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
    def post(cls, name):
        """Pre-sign a POST url for file upload to S3 and post"""
        specifications = CADSpecificationSchema(
            only=cad_spec_keys).load(request.form)

        model_name = name
        if CADModel.find_cad_model_by_name(model_name):
            return {'msg': gettext('cad_model_files_already_exist').format(model_name)}, 400

        folder = f"client_{get_jwt_identity()}"
        cad_object_key = f'{folder}/{model_name}'
        # Get a presigned post URL
        presigned_resp = create_presigned_post_url(
            s3_client, bucket_name, cad_object_key)
        url, fields = presigned_resp['url'], presigned_resp['fields']
        # Save to DB
        specifications['cad_object_key'] = cad_object_key
        specifications['cad_model_name'] = name
        cad_model = CADModel(client_id=get_jwt_identity(), **specifications)
        cad_model.save_cad_model_to_db()

        return {
            'msg': gettext('cad_model_saved_successfully'),
            'url': url,
            'fields': fields
        }, 200

    @classmethod
    def get(cls, name):
        """Retrieve a CAD model from the DB given a unique name passed in the body"""
        cad_model = CADModel.find_cad_model_by_name(name)

        if cad_model is None:
            return {'msg': gettext('cad_model_does_not_exist')}, 400

        if not cad_model.cad_model_visibility:
            return {'msg': gettext('cad_model_not_visible')}, 403

        valid_cad_model = CADSpecificationSchema().dump(cad_model)
        # Get link to S3
        cad_url = create_presigned_url(
            s3_client, bucket_name, cad_model.cad_object_key)

        return {'cad_details': valid_cad_model, 'cad_url': cad_url}, 200

    @classmethod
    @jwt_required(fresh=True)
    def delete(cls, name):
        """Deletes a CAD model from DB and S3"""
        cad_model = CADModel.find_cad_model_by_name(name)
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
                return {'msg': gettext('cad_model_delete_successful').format(name)}, 200
            return {'msg': gettext('cad_model_failed_deletion')}, 400

    @classmethod
    @jwt_required(fresh=True)
    def patch(cls, name):
        """Update existing CAD model given update parameters"""

        # Validate form entries
        spec_schema = CADSpecificationSchema(only=cad_spec_keys, partial=True)
        update_specs = spec_schema.load(request.form)
        # Set up a counter to check property update counts
        count = 0

        if update_specs == {}:
            return {'msg': gettext('cad_model_update_info_empty')}
        # Defensive: Ensure a CAD model name is always submitted
        if update_specs['cad_model_name'] == '':
            return {'msg': gettext('cad_model_name_cannot_be_empty')}

        client_folder = f'client_{get_jwt_identity()}'
        current_cad = CADModel.find_cad_model_by_name(name)

        if current_cad is None:
            return {'msg': gettext('cad_model_does_not_exist')}, 400

        object_key = f'{client_folder}/{update_specs["cad_model_name"]}'
        # Get a presigned POST url
        ps_data = create_presigned_post_url(
            s3_client, bucket_name, object_key)
        url, fields = ps_data['url'], ps_data['fields']

        # Update cad_model_key
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
            return {
                'msg': gettext('cad_model_updated_successfully').format(current_cad.cad_model_name),
                'url': url,
                'fields': fields
            }, 200
        return {'msg': gettext('cad_model_update_info_empty')}, 400


class CADModelList(Resource):
    @classmethod
    @jwt_required(optional=True)
    def get(cls, username):
        """Return all the CAD models in a clients collection"""
        # 1. Find the client by given username
        client = ClientModel.find_client_by_username(username)
        if client is None:
            return {'msg': gettext('client_profile_client_does_not_exist')}, 400
        # 2. Return the list of models in found client's collection
        model_schema = CADSpecificationSchema(only=cad_spec_keys, partial=True)
        return {
            'cad_models': list(map(lambda x: model_schema.dump(x), client.cad_models_list))
        }, 200
