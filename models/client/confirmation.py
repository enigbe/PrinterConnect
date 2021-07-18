from time import time
from uuid import uuid4
from typing import List

from data_base import db

EXPIRATION_DELTA = 30 * 60  # 30 minutes in seconds


class ConfirmationModel(db.Model):
    __tablename__ = 'confirmations'

    id = db.Column(db.String(50), primary_key=True)
    expire_at = db.Column(db.Integer, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)

    client = db.relationship('ClientModel', back_populates='confirmation')

    def __init__(self, client_id: int, **kwargs):
        super().__init__(**kwargs)
        self.client_id = client_id
        self.id = uuid4().hex
        self.expire_at = int(time()) + EXPIRATION_DELTA
        self.confirmed = False

    @classmethod
    def find_by_client_id(cls, client_id: str) -> List['ConfirmationModel']:
        return cls.query.filter_by(client_id=client_id).all()

    @classmethod
    def find_by_id(cls, _id: str) -> 'ConfirmationModel':
        return cls.query.filter_by(id=_id).first()

    @property
    def has_expired(self) -> bool:
        return time() > self.expire_at

    def force_to_expire(self) -> None:
        # expire a link that hasn't expired yet
        if not self.has_expired:
            self.expire_at = int(time())
            self.save_to_db()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
