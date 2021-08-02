from data_base import db


class TokenBlockListModel(db.Model):
    """Model of a valid user token rendered invalid when they sign out"""
    __tablename__ = 'blocked_tokens'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(50), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=True)
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'), nullable=True)

    client = db.relationship('ClientModel', back_populates='token_blocklist')
    business = db.relationship('BusinessModel', back_populates='token_blocklist')

    def __repr__(self):
        return '<TokenBlockList: {}: {}>'.format(self.id, self.jti)

    @classmethod
    def find_token_by_jti(cls, jti: str) -> "TokenBlockListModel":
        return cls.query.filter_by(jti=jti).first()

    @classmethod
    def find_tokens_by_id(cls, _id: int):
        return cls.query.filter_by(client_id=_id).all()

    def save_token_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
