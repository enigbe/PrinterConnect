from marsh_mallow import ma
from models.business.printer import PrinterModel


class PrinterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PrinterModel
        dump_only = ('business_id',)
