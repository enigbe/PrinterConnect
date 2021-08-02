from marsh_mallow import ma
from models.shared_user.token_blocklist import TokenBlockListModel


class TokenBlockListSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TokenBlockListModel
        include_fk = True
