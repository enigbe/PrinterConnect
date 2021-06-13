from marsh_mallow import ma
from models.client.cad_model import CADModel


class CADModelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CADModel
        load_only = ('client_id',)  # Do not include when dumping
