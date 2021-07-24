from typing import List

from flask import request, url_for
from requests import Response
from werkzeug.security import generate_password_hash, check_password_hash

from data_base import db
from libs.mailgun import Mailgun
from libs.strings import gettext
from models.confirmation import ConfirmationModel
from models.client.token_blocklist import TokenBlockListModel
from models.client.cad_model import CADModel
from models.user import UserModel, DBModelUserModel


class ClientModel(db.Model, UserModel, metaclass=DBModelUserModel):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, index=True)
    username = db.Column(db.String(120), unique=True, index=True)
    first_name = db.Column(db.String(120), nullable=True)
    last_name = db.Column(db.String(120), nullable=True)
    password = db.Column(db.String(120), nullable=True)
    oauth_token = db.Column(db.String(200), nullable=True, default=None)
    oauth_token_secret = db.Column(db.String(200), nullable=True, default=None)
    bio = db.Column(db.String(250), nullable=True, default=None)
    avatar_filename = db.Column(db.String(100), default=None)
    avatar_uploaded = db.Column(db.Boolean, default=False, nullable=True)

    confirmation = db.relationship(
        'ConfirmationModel',
        lazy='dynamic',
        cascade='all, delete-orphan',
        back_populates='client'
    )
    token_blocklist = db.relationship(
        'TokenBlockListModel',
        lazy='dynamic',
        cascade='all, delete-orphan',
        back_populates='client'
    )

    cad_model = db.relationship(
        'CADModel',
        lazy='dynamic',
        cascade='all, delete-orphan',
        back_populates='client'
    )

    def __repr__(self) -> str:
        return '<Client => {} {}: [@{} - ({})]>'.format(self.first_name, self.last_name, self.username, self.email)

    @property
    def most_recent_confirmation(self) -> "ConfirmationModel":
        return self.confirmation.order_by(db.desc(ConfirmationModel.expire_at)).first()

    @property
    def cad_models_list(self) -> List["CADModel"]:
        return self.cad_model.order_by(db.desc(CADModel.cad_model_creation_time)).all()

    @classmethod
    def find_user_by_id(cls, _id: int) -> "ClientModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_user_by_email(cls, email: str) -> "ClientModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_user_by_username(cls, username: str) -> "ClientModel":
        return cls.query.filter_by(username=username).first()

    def hash_password(self, password: str):
        self.password = generate_password_hash(password)

    def verify_password(self, password: str):
        try:
            return check_password_hash(self.password, password)
        except AttributeError:
            return False

    def send_verification_email(self) -> Response:
        # http://127.0.0.1:5000 + /client/confirmation/<string:confirmation_id>
        link = request.url_root[:-1] + url_for('confirmation', user_model_type='client',
                                               confirmation_id=self.most_recent_confirmation.id)
        client_name = self.first_name

        subject = gettext('clientmodel_verification_email_subject')
        text = gettext('clientmodel_verification_email_text').format(client_name, link)

        return Mailgun.send_email([self.email], subject, text)

    def send_update_email_notification(self, new_email) -> Response:
        client_name = self.first_name
        subject = gettext('client_profile_email_update_subject')
        text_content = gettext('client_profile_email_update_text').format(client_name, new_email)
        return Mailgun.send_email([self.email], subject, text_content)
