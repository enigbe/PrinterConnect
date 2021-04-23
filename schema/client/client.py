from models.client.client import ClientModel
from ma import ma


class ClientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ClientModel
        load_instance = True
        load_only = ('password',)  # do not include when dumping data
        dump_only = ('id',)        # do not include when loading data
