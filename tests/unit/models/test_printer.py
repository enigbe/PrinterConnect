from unittest import TestCase

from models.business.printer import PrinterModel
from schema.business.printer import PrinterSchema
from tests.test_data import printer_data


printer_schema = PrinterSchema()


class PrinterTest(TestCase):
    def test_create_printers(self):
        printer = PrinterModel(business_id=1, **printer_data)
        printer_dict = printer_schema.dump(printer)
        self.assertEqual(printer_dict, printer_data)

    def test_printer_repr(self):
        printer = PrinterModel(business_id=1, **printer_data)
        expected_repr = f'<PrinterModel name: {printer_data["name"]}, model: {printer_data["model"]}, ' \
                        f'width: {printer_data["base_width"]}, length: {printer_data["base_length"]}, ' \
                        f'height: {printer_data["height"]}, file_type: {printer_data["file_type"]}, material:' \
                        f' {printer_data["material"]}>'
        self.assertEqual(printer.__repr__(), expected_repr)

    def test_printer_build_volume(self):
        printer = PrinterModel(business_id=1, **printer_data)
        computed_bv = printer.printer_build_volume
        expected_bv = printer_data['base_width'] * printer_data['base_length'] * printer_data['height']
        self.assertEqual(computed_bv, expected_bv)
