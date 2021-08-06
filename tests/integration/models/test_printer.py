from tests.base_test import BaseTest
from models.business.printer import PrinterModel
from models.business.business import BusinessModel
from tests.test_data import printer_data, business_data
from libs.user_helper import generate_random_username


class PrinterTest(BaseTest):
    def test_save_printer_to_db(self):
        with self.app_context():
            business = BusinessModel(**business_data)
            business.save_user_to_db()
            printer = PrinterModel(business_id=business.id, **printer_data)
            self.assertIsNone(PrinterModel.find_printer_by_name(printer_data['name']))
            printer.save_printer_to_db()
            self.assertIsNotNone(PrinterModel.find_printer_by_name(printer_data['name']))

    def test_delete_printer_from_db(self):
        with self.app_context():
            business = BusinessModel(**business_data)
            business.save_user_to_db()
            printer = PrinterModel(business_id=business.id, **printer_data)
            self.assertIsNone(PrinterModel.find_printer_by_name(printer_data['name']))
            printer.save_printer_to_db()
            self.assertIsNotNone(PrinterModel.find_printer_by_name(printer_data['name']))
            printer.delete_printer_from_db()
            self.assertIsNone(PrinterModel.find_printer_by_name(printer_data['name']))

    def test_update_printer_in_db(self):
        with self.app_context():
            business = BusinessModel(**business_data)
            business.save_user_to_db()
            printer = PrinterModel(business_id=business.id, **printer_data)
            self.assertIsNone(PrinterModel.find_printer_by_name(printer_data['name']))
            printer.save_printer_to_db()
            self.assertIsNotNone(PrinterModel.find_printer_by_name(printer_data['name']))
            updated_name = generate_random_username()
            printer.name = updated_name
            printer.update_printer_in_db()
            self.assertIsNotNone(PrinterModel.find_printer_by_name(updated_name))