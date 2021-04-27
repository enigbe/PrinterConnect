from flask import request, url_for
from requests import Response
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from libs.mailgun import Mailgun
# SUBJECT = 'Account Verification'
# TEXT = """
# Hello {},
#
# Welcome to PrinterConnect.
#
# To verify your identity, click on this link - ({})
#
# If this email was sent to you in error, please disregard.
#
# Warm regards.
# """


class ClientModel(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    username = db.Column(db.String(120), nullable=False, unique=True, index=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_activated = db.Column(db.Boolean, default=False)

    def __init__(self, email: str, username: str, first_name: str, last_name: str, password: str,
                 is_activated: bool = False) -> None:
        self.email = email
        self.username = username
        self.first_name = first_name[0].upper() + first_name[1:].lower()
        self.last_name = last_name[0].upper() + last_name[1:].lower()
        self.password = generate_password_hash(password)
        self.is_activated = is_activated

    def __repr__(self) -> str:
        return '<Client => {} {}: [@{} - ({})]>'.format(self.first_name, self.last_name, self.username, self.email)

    @classmethod
    def find_client_by_email(cls, email: str) -> "ClientModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_client_by_username(cls, username: str) -> "ClientModel":
        return cls.query.filter_by(username=username).first()

    def verify_password(self, password: str):
        return check_password_hash(self.password, password)

    def verify_email(self) -> Response:
        # http://127.0.0.1:5000 + /client/activate/<string:username>
        link = request.url_root[:-1] + url_for('activateclient', username=self.username)
        client = self.first_name

        subject = 'Account Verification'
        text = f"""
        Hello {client},

        Welcome to PrinterConnect. 

        To verify your identity, click on this link - ({link})

        If this email was sent to you in error, please disregard.

        Warm regards.
        """

        return Mailgun.send_email([self.email], subject, text)

    def save_client_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_client_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
