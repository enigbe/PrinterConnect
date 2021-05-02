from flask import request, url_for
from requests import Response
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from libs.mailgun import Mailgun
from libs.strings import gettext
from models.client.confirmation import ConfirmationModel


class ClientModel(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    username = db.Column(db.String(120), nullable=False, unique=True, index=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)

    confirmation = db.relationship(
        'ConfirmationModel',
        lazy='dynamic',
        cascade='all, delete-orphan',
        back_populates='client'
    )

    def __repr__(self) -> str:
        return '<Client => {} {}: [@{} - ({})]>'.format(self.first_name, self.last_name, self.username, self.email)

    @property
    def most_recent_confirmation(self) -> "ConfirmationModel":
        return self.confirmation.order_by(db.desc(ConfirmationModel.expire_at)).first()

    @classmethod
    def find_client_by_email(cls, email: str) -> "ClientModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_client_by_username(cls, username: str) -> "ClientModel":
        return cls.query.filter_by(username=username).first()

    def hash_password(self, password: str):
        self.password = generate_password_hash(password)

    def verify_password(self, password: str):
        return check_password_hash(self.password, password)

    def send_verification_email(self) -> Response:
        # http://127.0.0.1:5000 + /client/confirmation/<string:confirmation_id>
        link = request.url_root[:-1] + \
               url_for('confirmation', confirmation_id=self.most_recent_confirmation.id)
        client_name = self.first_name

        subject = gettext('clientmodel_verification_email_subject')
        text = gettext('clientmodel_verification_email_text').format(client_name, link)

        return Mailgun.send_email([self.email], subject, text)

    def save_client_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_client_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
