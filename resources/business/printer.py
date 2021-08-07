from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.business.business import BusinessModel
from models.business.printer import PrinterModel
from schema.business.printer import PrinterSchema
from libs.strings import gettext

printer_schema = PrinterSchema()


class Printer(Resource):
    @classmethod
    @jwt_required(fresh=True)
    def post(cls, username, printer_name):
        business_account = BusinessModel.find_user_by_username(username)
        if business_account is None:
            return {'msg': gettext('user_does_not_exist')}, 400

        business_id = get_jwt_identity()
        if business_account.id != business_id:
            return {'msg': gettext('printer_unauthorized_to_post')}, 403

        if PrinterModel.find_printer_by_name_and_business_id(printer_name, business_account.id):
            return {'msg': gettext('printer_already_exist').format(printer_name)}, 400

        printer_data = printer_schema.load(request.get_json())
        if printer_name == printer_data['name']:
            try:
                printer = PrinterModel(business_id=business_id, **printer_data)
                printer.save_printer_to_db()
            except Exception as e:
                return {'msg': str(e)}, 500
            else:
                return {'msg': gettext('printer_successfully_created')}, 201
        return {'msg': 'printer_name_mismatch'}, 400

    @classmethod
    def get(cls, username, printer_name):
        business_account = BusinessModel.find_user_by_username(username)
        if business_account is None:
            return {'msg': gettext('user_does_not_exist')}, 400
        printer = PrinterModel.find_printer_by_name(printer_name)
        if printer is None:
            return {'msg': gettext('printer_does_not_exist')}, 400

        serialized_printer = printer_schema.dump(printer)
        return {'printer': serialized_printer}, 200

    @classmethod
    @jwt_required(fresh=True)
    def delete(cls, username, printer_name):
        business_account = BusinessModel.find_user_by_username(username)
        if business_account is None:
            return {'msg': gettext('user_does_not_exist')}, 400
        printer = PrinterModel.find_printer_by_name(printer_name)
        if printer is None:
            return {'msg': gettext('printer_does_not_exist')}, 400
        try:
            printer.delete_printer_from_db()
        except Exception as e:
            return {'msg': str(e)}, 500
        else:
            return {'msg': gettext('printer_successfully_deleted')}, 200

    @classmethod
    @jwt_required(fresh=True)
    def put(cls, username, printer_name):
        business_account = BusinessModel.find_user_by_username(username)
        if business_account is None:
            return {'msg': gettext('user_does_not_exist')}, 400
        printer = PrinterModel.find_printer_by_name(printer_name)
        update_data = printer_schema.load(request.get_json())
        if printer is None:
            business_id = get_jwt_identity()
            if business_account.id == business_id:
                # Create new printer if business.id == business_id
                try:
                    printer = PrinterModel(business_id=business_id, **update_data)
                    printer.save_printer_to_db()
                except Exception as e:
                    return {'msg': str(e)}, 500
                else:
                    return {'msg': gettext('printer_successfully_created')}, 201

            return {'msg': gettext('printer_does_not_exist')}, 400

        # Update provided properties
        try:
            if 'name' in update_data:
                printer.name = update_data['name']
            if 'model' in update_data:
                printer.model = update_data['model']
            if 'nozzle_diameter' in update_data:
                printer.nozzle_diameter = update_data['nozzle_diameter']
            if 'height' in update_data:
                printer.height = update_data['height']
            if 'base_width' in update_data:
                printer.base_width = update_data['base_width']
            if 'base_length' in update_data:
                printer.base_length = update_data['base_length']
            if 'material' in update_data:
                printer.material = update_data['material']
            if 'file_type' in update_data:
                printer.file_type = update_data['file_type']
            printer.update_printer_in_db()
        except Exception as e:
            printer.rollback_printer_changes()
            return {'msg': str(e)}, 500
        else:
            return {'msg': gettext('printer_update_successful')}


class PrinterList(Resource):
    @classmethod
    def get(cls, username):
        business_account = BusinessModel.find_user_by_username(username)
        if business_account is None:
            return {'msg': gettext('user_does_not_exist')}, 400

        printers = PrinterModel.list_printers_by_business_id(business_account.id)
        return {'printers': [printer_schema.dump(x) for x in printers]}, 200
