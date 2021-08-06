from requests import Response

from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, url_for

from datetime import datetime

from data_base import db
from libs.mailgun import Mailgun
from libs.strings import gettext

from models.shared_user.user import UserModel, DBModelUserModel
import models.shared_user.confirmation as conf
import models.shared_user.token_blocklist as tbl
import models.business.printer as prnt


class BusinessModel(db.Model, UserModel, metaclass=DBModelUserModel):
    __tablename__ = 'businesses'

    id = db.Column(db.Integer, primary_key=True)
    business_name = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(100), nullable=True)
    username = db.Column(db.String(20), nullable=False, index=True)
    bio = db.Column(db.String(200), nullable=True)
    creation_date = db.Column(db.DateTime, nullable=True)

    confirmation = db.relationship(
        'ConfirmationModel',
        lazy='dynamic',
        cascade='all, delete-orphan',
        back_populates='business'
    )
    token_blocklist = db.relationship(
        'TokenBlockListModel',
        lazy='dynamic',
        cascade='all, delete-orphan',
        back_populates='business'
    )

    printer = db.relationship(
        'PrinterModel',
        lazy='dynamic',
        cascade='all, delete-orphan',
        back_populates='business'
    )

    def __init__(self, **kwargs):
        super(BusinessModel, self).__init__(**kwargs)
        self.creation_date = datetime.utcnow()

    def __repr__(self):
        return f'<Business => @{self.username}: {self.business_name} - ({self.email})>'

    @property
    def most_recent_confirmation(self) -> 'mcc.ConfirmationModel':
        return self.confirmation.order_by(db.desc(conf.ConfirmationModel.expire_at)).first()

    @classmethod
    def find_user_by_username(cls, username) -> 'BusinessModel':
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_user_by_id(cls, _id) -> 'BusinessModel':
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_user_by_email(cls, email) -> 'BusinessModel':
        return cls.query.filter_by(email=email).first()

    def hash_password(self, password: str):
        self.password = generate_password_hash(password)

    def verify_password(self, password: str):
        try:
            return check_password_hash(self.password, password)
        except AttributeError:
            return False

    def send_verification_email(self) -> Response:
        # http://127.0.0.1:5000 + /client/confirmation/<string:confirmation_id>
        link = request.url_root[:-1] + url_for('confirmation', user_model_type='business',
                                               confirmation_id=self.most_recent_confirmation.id)
        business_name = self.business_name

        subject = gettext('businessmodel_verification_email_subject')
        text = gettext('businessmodel_verification_email_text').format(business_name, link)

        return Mailgun.send_email([self.email], subject, text)

    def send_update_email_notification(self, new_email) -> Response:
        business_name = self.business_name
        subject = gettext('business_profile_email_update_subject')
        text_content = gettext('business_profile_email_update_text').format(business_name, new_email)
        return Mailgun.send_email([self.email], subject, text_content)

    def send_password_reset_link(self) -> Response:
        # http://127.0.0.1:5001 + /password/reset
        reset_link = request.url_root[:-1] + url_for('resetpassword')
        business_name = self.business_name
        subject = gettext('user_model_reset_password_subject')
        text = gettext('user_model_reset_password_text').format(business_name, reset_link)

        return Mailgun.send_email([self.email], subject, text)

