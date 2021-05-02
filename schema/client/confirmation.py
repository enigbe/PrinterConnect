from ma import ma
from models.client.confirmation import ConfirmationModel


class ConfirmationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ConfirmationModel
        load_only = ('client',)
        dump_only = ('id', 'expire_at', 'confirmed')
        include_fk = True
