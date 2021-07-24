from marsh_mallow import ma
from models.confirmation import ConfirmationModel


class ConfirmationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ConfirmationModel
        load_only = ('client',)
        dump_only = ('id', 'expire_at', 'confirmed')
        include_fk = True
