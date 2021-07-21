from marsh_mallow import ma
from models.business.business import BusinessModel


class BusinessSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BusinessModel
        dump_only = ('creation_date',)
        load_only = ('password', 'id',)
